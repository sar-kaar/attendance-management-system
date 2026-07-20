"""Face recognition provider layer.

Two providers, selected by settings.FACE_PROVIDER:

- 'local' (default): dlib via the face_recognition library. Encodings are
  128-d vectors stored as JSON lists in Student.face_encoding. Matching runs
  in-process; no network calls, no API key.

- 'azure': Azure AI Face API using the PersonGroup + Identify workflow.
  Requires AZURE_FACE_ENDPOINT / AZURE_FACE_KEY, and Microsoft Limited
  Access approval for everything beyond bare detection - until the
  registration is approved, Identify/PersonGroup calls return 403.

The provider-specific seams live in views.py (_extract_probe,
_find_best_match, _persist_face); this module holds the Azure client and
shared error type so views.py stays free of HTTP plumbing.
"""

import json
import logging
import time

from django.conf import settings

logger = logging.getLogger(__name__)


class FaceProcessingError(Exception):
    """Raised when an image can't be processed due to a real error (missing
    library, corrupt upload, provider/service failure) as opposed to simply
    finding no face."""


def provider_name():
    return getattr(settings, 'FACE_PROVIDER', 'local')


class AzureFaceClient:
    """Minimal REST client for the Azure AI Face API PersonGroup workflow.

    Plain `requests` instead of the Azure SDK: the legacy Face SDK is
    deprecated and this needs only five endpoints.

    Students enrolled through this provider store
    {"azure_person_id": "<uuid>"} in Student.face_encoding - the same column
    the local provider uses for its JSON vector - so switching providers
    needs no migration; students just re-register their face with the new
    provider.
    """

    RECOGNITION_MODEL = 'recognition_04'
    DETECTION_MODEL = 'detection_03'
    TRAIN_WAIT_SECONDS = 15

    def __init__(self):
        import requests  # lazy: local-only deployments don't need it installed
        self._requests = requests
        self.endpoint = (getattr(settings, 'AZURE_FACE_ENDPOINT', '') or '').rstrip('/')
        self.key = getattr(settings, 'AZURE_FACE_KEY', '') or ''
        self.group_id = getattr(settings, 'AZURE_FACE_PERSON_GROUP', 'ams-students')
        if not self.endpoint or not self.key:
            raise FaceProcessingError(
                'FACE_PROVIDER is "azure" but AZURE_FACE_ENDPOINT/AZURE_FACE_KEY '
                'are not configured on the server.'
            )

    def _url(self, path):
        return f'{self.endpoint}/face/v1.0/{path}'

    def _call(self, method, path, *, json_body=None, data=None, params=None,
              ok_statuses=(200, 202)):
        headers = {'Ocp-Apim-Subscription-Key': self.key}
        if data is not None:
            headers['Content-Type'] = 'application/octet-stream'
        try:
            resp = self._requests.request(
                method, self._url(path), headers=headers,
                json=json_body, data=data, params=params, timeout=30,
            )
        except self._requests.RequestException as exc:
            logger.exception('Azure Face request failed: %s %s', method, path)
            raise FaceProcessingError(f'Could not reach the Azure Face API: {exc}')

        if resp.status_code in ok_statuses:
            return resp

        try:
            detail = resp.json().get('error', {}).get('message', resp.text)
        except ValueError:
            detail = resp.text
        logger.error('Azure Face %s %s -> %s: %s', method, path, resp.status_code, detail)
        if resp.status_code == 403:
            raise FaceProcessingError(
                'Azure Face rejected the call (403). Identify/PersonGroup require '
                'an approved Limited Access registration - detection alone does '
                f'not. Azure said: {detail}'
            )
        raise FaceProcessingError(f'Azure Face API error ({resp.status_code}): {detail}')

    def ensure_group(self):
        # PUT is create-only here: 200 on create, 409 if it already exists.
        self._call(
            'PUT', f'persongroups/{self.group_id}',
            json_body={'name': 'AMS registered students',
                       'recognitionModel': self.RECOGNITION_MODEL},
            ok_statuses=(200, 409),
        )

    def detect_face_id(self, image_bytes):
        """Return a transient faceId for the first detected face, or None."""
        resp = self._call('POST', 'detect', data=image_bytes, params={
            'returnFaceId': 'true',
            'recognitionModel': self.RECOGNITION_MODEL,
            'detectionModel': self.DETECTION_MODEL,
        })
        faces = resp.json()
        if not faces:
            return None
        return faces[0]['faceId']

    def register(self, student, image_bytes):
        """Enroll a face image and return the Azure personId.

        Re-registering a student who already has a person adds this image as
        an additional face on the same person instead of creating a duplicate.
        """
        self.ensure_group()

        person_id = None
        try:
            stored = json.loads(student.face_encoding or 'null')
            if isinstance(stored, dict):
                person_id = stored.get('azure_person_id')
        except ValueError:
            pass

        if not person_id:
            resp = self._call(
                'POST', f'persongroups/{self.group_id}/persons',
                json_body={'name': student.student_id},
            )
            person_id = resp.json()['personId']

        self._call(
            'POST',
            f'persongroups/{self.group_id}/persons/{person_id}/persistedFaces',
            data=image_bytes,
            params={'detectionModel': self.DETECTION_MODEL},
        )
        self._train()
        return person_id

    def _train(self):
        self._call('POST', f'persongroups/{self.group_id}/train')
        # Identify errors until training completes. Small groups train in a
        # couple of seconds, so block briefly instead of surfacing that error
        # to whoever registers next.
        deadline = time.monotonic() + self.TRAIN_WAIT_SECONDS
        while time.monotonic() < deadline:
            resp = self._call('GET', f'persongroups/{self.group_id}/training')
            train_status = resp.json().get('status')
            if train_status == 'succeeded':
                return
            if train_status == 'failed':
                raise FaceProcessingError('Azure Face person group training failed.')
            time.sleep(1)
        logger.warning('Azure Face training still running after %ss; identify '
                       'may fail briefly.', self.TRAIN_WAIT_SECONDS)

    def identify(self, face_id, confidence_threshold=0.6):
        """Match a detected faceId against the group.

        Returns (person_id, confidence) or (None, 0.0). Azure's
        confidenceThreshold is higher-is-stricter in [0, 1]; the views pass
        their `tolerance` param straight through, and the shared 0.6 default
        behaves sensibly for both providers.
        """
        resp = self._call('POST', 'identify', json_body={
            'personGroupId': self.group_id,
            'faceIds': [face_id],
            'maxNumOfCandidates': 1,
            'confidenceThreshold': confidence_threshold,
        })
        results = resp.json()
        if results and results[0].get('candidates'):
            candidate = results[0]['candidates'][0]
            return candidate['personId'], float(candidate['confidence'])
        return None, 0.0
