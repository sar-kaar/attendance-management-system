import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { attendanceAPI } from "../services/api";
import { FaSignOutAlt, FaUserCircle } from "react-icons/fa";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import "../styles/dashboard.css";
import "../styles/layout.css";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function StudentDashboard() {
  const { user, logout } = useAuth();
  const [attendance, setAttendance] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;
    const studentId = user.id;
    Promise.all([
      attendanceAPI.myAttendance(studentId),
      attendanceAPI.report({ student: studentId }),
    ])
      .then(([attRes, reportRes]) => {
        setAttendance(attRes.data || []);
        setStats(reportRes.data || null);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [user]);

  const statusColor = (status) => {
    switch (status) {
      case "present":
        return "#22c55e";
      case "absent":
        return "#ef4444";
      case "late":
      case "lp":
        return "#f59e0b";
      case "eca":
        return "#8b5cf6";
      default:
        return "#9ca3af";
    }
  };

  const doughnutData = stats
    ? {
        labels: ["Present", "Absent"],
        datasets: [
          {
            data: [stats.present, stats.absent],
            backgroundColor: ["#22c55e", "#ef4444"],
          },
        ],
      }
    : null;

  return (
    <div style={{ minHeight: "100vh", background: "#f0f2f5" }}>
      <header
        style={{
          background: "#1a1a2e",
          color: "white",
          padding: "16px 32px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h2>
          Attend<span style={{ color: "#4a90d9" }}>Pro</span> — My Attendance
        </h2>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <span>{user?.first_name || user?.username}</span>
          <button
            onClick={logout}
            style={{
              background: "none",
              border: "none",
              color: "#a0a0b0",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: 8,
              fontSize: 14,
            }}
          >
            <FaSignOutAlt /> Logout
          </button>
        </div>
      </header>

      <div style={{ padding: 32 }}>
        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <>
            {stats && (
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-label">Total Records</div>
                  <div className="stat-value">{stats.total_records}</div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Present</div>
                  <div className="stat-value" style={{ color: "#22c55e" }}>
                    {stats.present}
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Absent</div>
                  <div className="stat-value" style={{ color: "#ef4444" }}>
                    {stats.absent}
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Attendance %</div>
                  <div className="stat-value">{stats.attendance_percentage}%</div>
                </div>
              </div>
            )}

            <div className="charts-grid">
              <div className="panel">
                <h3>My Attendance</h3>
                {doughnutData && (
                  <Doughnut
                    data={doughnutData}
                    options={{ responsive: true, plugins: { legend: { position: "bottom" } } }}
                  />
                )}
              </div>
              <div className="panel">
                <h3>Recent Records</h3>
                <table className="recent-table">
                  <thead>
                    <tr>
                      <th>Course</th>
                      <th>Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {attendance.slice(0, 10).map((a) => (
                      <tr key={a.id}>
                        <td>{a.course_name}</td>
                        <td>{a.date}</td>
                        <td>
                          <span
                            className="badge"
                            style={{
                              background: statusColor(a.status) + "22",
                              color: statusColor(a.status),
                            }}
                          >
                            {a.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                    {attendance.length === 0 && (
                      <tr>
                        <td colSpan={3} style={{ textAlign: "center", padding: 32 }}>
                          No attendance records yet
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
