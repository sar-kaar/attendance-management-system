import { useState, useEffect, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { FaEnvelope, FaKeyboard } from "react-icons/fa";
import { otpAPI } from "../services/api";
import "../styles/login.css";
import logo from "../assets/MIT LOGO.png";

const RESEND_COOLDOWN = 60;

function VerifyEmail() {
  const navigate = useNavigate();
  const location = useLocation();
  // Register hands the address over in router state so it is never put in the
  // URL, where it would end up in history and server logs.
  const email = location.state?.email || "";

  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [secondsLeft, setSecondsLeft] = useState(RESEND_COOLDOWN);
  const sentOnce = useRef(false);

  useEffect(() => {
    if (!email) {
      navigate("/register", { replace: true });
      return;
    }
    // Register already triggered the first send; StrictMode double-invokes
    // effects in dev, and a second send here would trip the server cooldown
    // and show a spurious error on a screen the user just opened.
    if (sentOnce.current) return;
    sentOnce.current = true;
    setNotice(`We sent a 6-digit code to ${email}. It expires in 10 minutes.`);
  }, [email, navigate]);

  useEffect(() => {
    if (secondsLeft <= 0) return undefined;
    const t = setTimeout(() => setSecondsLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
  }, [secondsLeft]);

  const readError = (err, fallback) =>
    err.response?.data?.error || err.response?.data?.detail || fallback;

  const handleVerify = async (e) => {
    e.preventDefault();
    setError("");
    setNotice("");
    setSubmitting(true);
    try {
      await otpAPI.verify(email, code);
      navigate("/login", {
        replace: true,
        state: { message: "Email verified. You can sign in now." },
      });
    } catch (err) {
      setError(readError(err, "Verification failed. Please try again."));
    } finally {
      setSubmitting(false);
    }
  };

  const handleResend = async () => {
    setError("");
    setNotice("");
    try {
      await otpAPI.send(email);
      setNotice("A new code is on its way.");
      setSecondsLeft(RESEND_COOLDOWN);
    } catch (err) {
      setError(readError(err, "Could not resend the code."));
      // A 429 means the server's own cooldown is still running; keep the
      // button disabled rather than inviting another rejected attempt.
      if (err.response?.status === 429) setSecondsLeft(RESEND_COOLDOWN);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <img src={logo} alt="MIT Logo" className="college-logo" />
          <h1>Verify your email</h1>
          <p>Model Institute of Technology</p>
        </div>

        {error && <div className="error-msg">{error}</div>}
        {notice && (
          <div className="error-msg" style={{ background: "#eff6ff", color: "#1d4ed8" }}>
            {notice}
          </div>
        )}

        <form onSubmit={handleVerify}>
          <div className="input-box">
            <FaEnvelope className="icon" />
            <input type="email" value={email} readOnly disabled />
          </div>

          <div className="input-box">
            <FaKeyboard className="icon" />
            <input
              type="text"
              inputMode="numeric"
              autoComplete="one-time-code"
              placeholder="6-digit code"
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
              required
              minLength={6}
              maxLength={6}
              autoFocus
            />
          </div>

          <button
            className="login-btn"
            type="submit"
            disabled={submitting || code.length !== 6}
          >
            {submitting ? "Verifying..." : "Verify Email"}
          </button>
        </form>

        <div className="options" style={{ marginTop: "1rem" }}>
          <button
            type="button"
            className="link-btn"
            onClick={handleResend}
            disabled={secondsLeft > 0}
          >
            {secondsLeft > 0 ? `Resend code in ${secondsLeft}s` : "Resend code"}
          </button>
          <button type="button" className="link-btn" onClick={() => navigate("/login")}>
            Back to login
          </button>
        </div>
      </div>
    </div>
  );
}

export default VerifyEmail;
