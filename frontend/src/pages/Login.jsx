import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaUser, FaLock } from "react-icons/fa";
import { useAuth } from "../context/AuthContext";
import "../styles/login.css";
import logo from "../assets/MIT LOGO.png";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [showResetInfo, setShowResetInfo] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const user = await login(username, password);
      if (user.role === "student") {
        navigate("/student");
      } else {
        navigate("/dashboard");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid credentials");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <img src={logo} alt="MIT Logo" className="college-logo" />
          <h1>Attendance Management System</h1>
          <h3>Face Recognition Based Attendance System</h3>
          <p>Model Institute of Technology</p>
        </div>

        {error && <div className="error-msg">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="input-box">
            <FaUser className="icon" />
            <input
              type="text"
              placeholder="Enter Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-box">
            <FaLock className="icon" />
            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="options">
            <label>
              <input type="checkbox" />&nbsp;&nbsp;Remember Me
            </label>
            <button
              type="button"
              className="link-btn"
              onClick={() => setShowResetInfo((v) => !v)}
            >
              Forgot Password?
            </button>
          </div>

          {showResetInfo && (
            <div className="error-msg" style={{ background: "#eff6ff", color: "#1d4ed8" }}>
              Self-service password reset isn't available yet — contact your administrator to
              have your password reset.
            </div>
          )}

          <button className="login-btn" type="submit" disabled={submitting}>
            {submitting ? "Signing In..." : "Login"}
          </button>
        </form>

        <div className="register">
          Don't have an account?<a href="/register"> Register</a>
        </div>
      </div>
    </div>
  );
}

export default Login;
