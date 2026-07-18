import { useState, useEffect } from "react";
import { attendanceAPI, dashboardAPI } from "../services/api";
import { FaUsers, FaBook, FaCheckCircle, FaUserTie } from "react-icons/fa";
import { Bar, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "../styles/dashboard.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [atRisk, setAtRisk] = useState([]);

  useEffect(() => {
    attendanceAPI
      .dashboard()
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));

    dashboardAPI
      .atRisk()
      .then((res) => setAtRisk(res.data))
      .catch(console.error);
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (!data) return <div className="loading">Failed to load dashboard</div>;

  const statCards = [
    { label: "Total Students", value: data.total_students, icon: <FaUsers />, color: "#4a90d9" },
    { label: "Active Courses", value: data.total_courses, icon: <FaBook />, color: "#22c55e" },
    {
      label: "Attendance Today",
      value: `${data.today.percentage}%`,
      icon: <FaCheckCircle />,
      color: "#f59e0b",
    },
    {
      label: "Overall Attendance",
      value: `${data.overall.percentage}%`,
      icon: <FaUserTie />,
      color: "#8b5cf6",
    },
  ];

  const barData = {
    labels: ["Present", "Absent"],
    datasets: [
      {
        label: "Today",
        data: [data.today.present, data.today.absent],
        backgroundColor: ["#22c55e", "#ef4444"],
      },
      {
        label: "Overall",
        data: [data.overall.present, data.overall.absent],
        backgroundColor: ["#86efac", "#fca5a5"],
      },
    ],
  };

  const doughnutData = {
    labels: ["Present", "Absent"],
    datasets: [
      {
        data: [data.overall.present, data.overall.absent],
        backgroundColor: ["#22c55e", "#ef4444"],
      },
    ],
  };

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

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        {statCards.map((card) => (
          <div key={card.label} className="stat-card">
            <div className="stat-icon" style={{ background: card.color }}>
              {card.icon}
            </div>
            <div>
              <div className="stat-label">{card.label}</div>
              <div className="stat-value">{card.value}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="charts-grid">
        <div className="panel">
          <h3>Attendance Comparison</h3>
          <div className="chart-wrap">
            <Bar
              data={barData}
              options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }}
            />
          </div>
        </div>
        <div className="panel">
          <h3>Overall Distribution</h3>
          <div className="chart-wrap">
            <Doughnut
              data={doughnutData}
              options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }}
            />
          </div>
        </div>
      </div>

      <div className="panel recent-panel">
        <h3>At-Risk Students <span className="panel-subtitle">(below 60% attendance)</span></h3>
        <table className="recent-table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Course</th>
              <th>Classes</th>
              <th>Attendance %</th>
            </tr>
          </thead>
          <tbody>
            {atRisk.slice(0, 8).map((item, i) => (
              <tr key={i}>
                <td>{item.student_name} <span className="muted">({item.student_code})</span></td>
                <td>{item.course_code}</td>
                <td>{item.present_count}/{item.total_classes}</td>
                <td>
                  <span
                    className="badge"
                    style={{
                      background: (item.attendance_percentage <= 40 ? "#ef4444" : "#f59e0b") + "22",
                      color: item.attendance_percentage <= 40 ? "#ef4444" : "#f59e0b",
                    }}
                  >
                    {item.attendance_percentage}%
                  </span>
                </td>
              </tr>
            ))}
            {atRisk.length === 0 && (
              <tr>
                <td colSpan={4} style={{ textAlign: "center", padding: 24 }}>
                  No at-risk students
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="panel recent-panel">
        <h3>Recent Attendance</h3>
        <table className="recent-table">
          <thead>
            <tr>
              <th>Student</th>
              <th>Course</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.recent_attendance.map((item, i) => (
              <tr key={i}>
                <td>{item.student}</td>
                <td>{item.course}</td>
                <td>{item.date}</td>
                <td>
                  <span className="badge" style={{ background: statusColor(item.status) + "22", color: statusColor(item.status) }}>
                    {item.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
