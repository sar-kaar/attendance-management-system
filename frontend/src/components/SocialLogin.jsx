import { useEffect, useRef, useState } from "react";
import { FaGoogle, FaFacebookF } from "react-icons/fa";
import { socialAPI } from "../services/api";

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "";
const FACEBOOK_APP_ID = import.meta.env.VITE_FACEBOOK_APP_ID || "";

/** Load a third-party SDK once, reusing the in-flight promise on re-renders. */
const loaded = {};
function loadScript(src, id) {
  if (loaded[id]) return loaded[id];
  loaded[id] = new Promise((resolve, reject) => {
    if (document.getElementById(id)) return resolve();
    const s = document.createElement("script");
    s.src = src;
    s.id = id;
    s.async = true;
    s.defer = true;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error(`Failed to load ${id}`));
    document.head.appendChild(s);
  });
  return loaded[id];
}

/**
 * Google and Facebook sign-in buttons.
 *
 * These SDKs only obtain a provider token in the browser; that token is posted
 * to our backend, which verifies it with the provider before issuing any of our
 * own credentials. Only the public client/app IDs live here - the Google client
 * secret and Facebook app secret never leave the server.
 */
function SocialLogin({ onSuccess, onError }) {
  const [busy, setBusy] = useState("");
  const googleBtn = useRef(null);

  const configured = Boolean(GOOGLE_CLIENT_ID || FACEBOOK_APP_ID);

  const exchange = async (provider, token) => {
    setBusy(provider);
    try {
      const res = await socialAPI[provider](token);
      onSuccess(res.data);
    } catch (err) {
      onError(
        err.response?.data?.error ||
          `${provider === "google" ? "Google" : "Facebook"} sign-in failed.`
      );
    } finally {
      setBusy("");
    }
  };

  useEffect(() => {
    if (!GOOGLE_CLIENT_ID) return;
    let cancelled = false;
    loadScript("https://accounts.google.com/gsi/client", "google-gsi")
      .then(() => {
        if (cancelled || !window.google?.accounts?.id) return;
        window.google.accounts.id.initialize({
          client_id: GOOGLE_CLIENT_ID,
          // credential is a signed ID token; our backend checks the signature
          // and that the audience is this client id before trusting it.
          callback: (resp) => exchange("google", resp.credential),
        });
        if (googleBtn.current) {
          // type "icon" keeps Google's required branding while staying a
          // compact square, so the two providers sit on one row instead of
          // adding two full-width blocks that push the card off-screen.
          // "medium" is 32px: the Facebook button below is hard-matched to
          // that number, and Google only exposes these three preset sizes.
          window.google.accounts.id.renderButton(googleBtn.current, {
            type: "icon",
            shape: "circle",
            theme: "outline",
            size: "medium",
          });
        }
      })
      .catch(() => onError("Could not load Google sign-in."));
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleFacebook = async () => {
    if (!FACEBOOK_APP_ID) return;
    try {
      await loadScript("https://connect.facebook.net/en_US/sdk.js", "facebook-sdk");
      window.FB.init({ appId: FACEBOOK_APP_ID, cookie: false, xfbml: false, version: "v21.0" });
      window.FB.login(
        (resp) => {
          if (resp.authResponse?.accessToken) {
            exchange("facebook", resp.authResponse.accessToken);
          } else {
            onError("Facebook sign-in was cancelled.");
          }
        },
        { scope: "email" }
      );
    } catch {
      onError("Could not load Facebook sign-in.");
    }
  };

  if (!configured) return null;

  return (
    <div className="social-login">
      <div className="social-divider">
        <span>or</span>
      </div>

      <div className="social-row">
        {GOOGLE_CLIENT_ID && (
          /* Google renders its own branded icon button into this node. */
          <div ref={googleBtn} className="social-icon-slot" title="Sign in with Google" />
        )}

        {FACEBOOK_APP_ID && (
          <button
            type="button"
            className="social-icon-btn facebook"
            onClick={handleFacebook}
            disabled={busy !== ""}
            aria-label="Sign in with Facebook"
            title="Sign in with Facebook"
          >
            <FaFacebookF />
          </button>
        )}
      </div>

      {busy && (
        <p className="social-busy">
          Signing in with {busy === "google" ? "Google" : "Facebook"}...
        </p>
      )}

      {!GOOGLE_CLIENT_ID && (
        <p className="social-note">
          <FaGoogle /> Google sign-in is not configured.
        </p>
      )}
    </div>
  );
}

export default SocialLogin;
