import { useState } from "react";
import { FaEnvelope, FaLock } from "react-icons/fa";
import "../styles/login.css";
import logo from "../assets/MIT LOGO.png";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    alert("Login Successful");
  };

  return (
    <div className="login-container">

      <div className="login-card">

        <div className="logo-section">

          <img
            src={logo}
            alt="MIT Logo"
            className="college-logo"
          />

          <h1>Attendance Management System</h1>

          <h3>Face Recognition Based Attendance System</h3>

          <p>Model Institute of Technology</p>

        </div>

        <form onSubmit={handleSubmit}>

          <div className="input-box">

            <FaEnvelope className="icon"/>

            <input
              type="email"
              placeholder="Enter Email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              required
            />

          </div>

          <div className="input-box">

            <FaLock className="icon"/>

            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
              required
            />

          </div>

          <div className="options">

            <label>
  <input type="checkbox" />&nbsp;&nbsp;
  Remember Me
</label>

            <a href="#">Forgot Password?</a>

          </div>

          <button className="login-btn" type="submit">

            Login

          </button>

        </form>

        <div className="register">

          Don't have an account?

          <a href="#"> Register</a>

        </div>

      </div>

    </div>
  );
}

export default Login;