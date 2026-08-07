# Frontend

React + Vite + MUI frontend for the Attendance Management System. Also ships as a
native Android app via [Capacitor](https://capacitorjs.com/) (see
[`capacitor.config.json`](capacitor.config.json), native project in `android/`).

## Setup

```bash
npm install
npm run dev
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```
VITE_API_URL=https://your-backend.azurewebsites.net/api
```

## Mobile app (Android)

The mobile build uses the deployed backend via `.env.mobile`:

```
VITE_API_URL=https://ams-backend.azurewebsites.net/api
```

Build the web bundle, copy it into the native project, and compile an APK:

```bash
npm run cap:sync    # vite build --mode mobile + cap sync android
npm run cap:apk     # gradlew assembleDebug
```

Debug APK output: `android/app/build/outputs/apk/debug/app-debug.apk`.

To open the native project in Android Studio (for signing, testing on a device,
or a release build) instead:

```bash
npm run cap:open
```

Notes:

- Requires the Android SDK (compileSdk 36) and JDK 21.
- The app runs the existing responsive web UI in a WebView, switching to
  `HashRouter` automatically when running natively.
- Camera use (face recognition) needs the `CAMERA` permission, already declared
  in `android/app/src/main/AndroidManifest.xml`.
- After cloning fresh, run `npm run cap:sync` once — the copied web assets under
  `android/app/src/main/assets/public` are gitignored.
