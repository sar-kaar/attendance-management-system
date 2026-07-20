import { useEffect, useState } from "react";
import { NavLink, Outlet, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  FaTachometerAlt,
  FaUsers,
  FaBook,
  FaClipboardCheck,
  FaCamera,
  FaSignOutAlt,
  FaUserCircle,
  FaUserPlus,
  FaTags,
  FaChartBar,
  FaBars,
  FaTimes,
} from "react-icons/fa";
import "../styles/layout.css";

const navItems = [
  { to: "/dashboard", icon: <FaTachometerAlt />, label: "Dashboard", end: true },
  { to: "/dashboard/students", icon: <FaUsers />, label: "Students" },
  { to: "/dashboard/courses", icon: <FaBook />, label: "Courses" },
  { to: "/dashboard/enrollments", icon: <FaUserPlus />, label: "Enrollments" },
  { to: "/dashboard/attendance", icon: <FaClipboardCheck />, label: "Attendance" },
  { to: "/dashboard/attendance-codes", icon: <FaTags />, label: "Attendance Codes" },
  { to: "/dashboard/reports", icon: <FaChartBar />, label: "Reports" },
  { to: "/dashboard/face-recognition", icon: <FaCamera />, label: "Face Recognition" },
];

export default function DashboardLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [drawerOpen, setDrawerOpen] = useState(false);

  // Navigating must not leave the mobile drawer covering the page the user
  // just asked for.
  useEffect(() => {
    setDrawerOpen(false);
  }, [location.pathname]);

  // Escape closes the drawer. It is a modal overlay on mobile, and leaving a
  // keyboard user stuck behind it with no way out is an accessibility failure.
  useEffect(() => {
    if (!drawerOpen) return undefined;
    const onKey = (e) => e.key === "Escape" && setDrawerOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [drawerOpen]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className={`layout${drawerOpen ? " drawer-open" : ""}`}>
      {/* Click-catcher behind the mobile drawer. aria-hidden because the same
          action is reachable from the labelled close button. */}
      <div
        className="sidebar-backdrop"
        onClick={() => setDrawerOpen(false)}
        aria-hidden="true"
      />

      <aside className="sidebar">
        <div className="sidebar-logo">
          <h2>
            Attend<span>Pro</span>
          </h2>
          <button
            type="button"
            className="drawer-close"
            onClick={() => setDrawerOpen(false)}
            aria-label="Close navigation"
          >
            <FaTimes />
          </button>
        </div>

        <nav>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-btn">
            <span className="nav-icon">
              <FaSignOutAlt />
            </span>
            <span className="nav-label">Logout</span>
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <button
            type="button"
            className="drawer-toggle"
            onClick={() => setDrawerOpen(true)}
            aria-label="Open navigation"
            aria-expanded={drawerOpen}
          >
            <FaBars />
          </button>
          <div className="user-info">
            <span>
              {user?.first_name || user?.username} ({user?.role})
            </span>
            <FaUserCircle className="user-icon" />
          </div>
        </header>

        {/* Keyed on the path so each route remounts and replays the enter
            animation; the animation itself is only opacity and transform. */}
        <div className="page-content" key={location.pathname}>
          <Outlet />
        </div>
      </main>
    </div>
  );
}
