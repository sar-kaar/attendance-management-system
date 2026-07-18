import { NavLink, Outlet, useNavigate } from "react-router-dom";
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

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-logo">
          <h2>
            Attend<span>Pro</span>
          </h2>
        </div>
        <nav>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              {item.icon}
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-btn">
            <FaSignOutAlt /> Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div />
          <div className="user-info">
            <span>
              {user?.first_name || user?.username} ({user?.role})
            </span>
            <FaUserCircle className="user-icon" />
          </div>
        </header>
        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
