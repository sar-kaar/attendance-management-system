import { useState, useEffect, Fragment } from "react";
import { dashboardAPI } from "../services/api";
import { useAuth } from "../context/AuthContext";
import "../styles/table.css";
import "../styles/dashboard.css";
import "../styles/reports.css";

const TABS = [
  { key: "stats", label: "Attendance Stats" },
  { key: "faculty", label: "Faculty Performance" },
  { key: "latecomers", label: "Chronic Latecomers" },
  { key: "incomplete", label: "Incomplete Records" },
  { key: "import", label: "Bulk Import", adminOnly: true },
];

function statusColor(status) {
  switch (status) {
    case "good":
      return "#22c55e";
    case "warning":
      return "#f59e0b";
    case "critical":
      return "#ef4444";
    default:
      return "#9ca3af";
  }
}

function AttendanceStatsTab() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardAPI
      .attendanceStats()
      .then((res) => setRows(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Course</th>
            <th>Faculty</th>
            <th>Classes Run</th>
            <th>Enrolled</th>
            <th>Avg Headcount</th>
            <th>Overall %</th>
            <th>Worst Day</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.course_id}>
              <td>
                {r.course_code} - {r.course_name}
              </td>
              <td>{r.faculty_name || "-"}</td>
              <td>{r.classes_run}</td>
              <td>{r.enrolled_count}</td>
              <td>{r.avg_headcount}</td>
              <td>{r.overall_percentage}%</td>
              <td>{r.worst_day || "-"}</td>
              <td>
                <span
                  className="badge"
                  style={{ background: statusColor(r.status) + "22", color: statusColor(r.status) }}
                >
                  {r.status}
                </span>
              </td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={8} style={{ textAlign: "center", padding: 32 }}>
                No data
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function FacultyPerformanceTab() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(null);

  useEffect(() => {
    dashboardAPI
      .facultyPerformance()
      .then((res) => setRows(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Faculty</th>
            <th>Subjects</th>
            <th>Students Managed</th>
            <th>Overall %</th>
            <th>Worst Subject</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {rows.map((f) => (
            <Fragment key={f.user_id}>
              <tr>
                <td>{f.faculty_name}</td>
                <td>{f.subjects_count}</td>
                <td>{f.students_managed}</td>
                <td>{f.overall_percentage}%</td>
                <td>{f.worst_subject || "-"}</td>
                <td>
                  <button
                    className="btn-icon"
                    onClick={() => setExpanded(expanded === f.user_id ? null : f.user_id)}
                  >
                    {expanded === f.user_id ? "Hide" : "Details"}
                  </button>
                </td>
              </tr>
              {expanded === f.user_id && (
                <tr>
                  <td colSpan={6} style={{ background: "#f8f9fa" }}>
                    <table className="nested-table">
                      <thead>
                        <tr>
                          <th>Course</th>
                          <th>Classes</th>
                          <th>Attendance %</th>
                        </tr>
                      </thead>
                      <tbody>
                        {f.courses.map((c) => (
                          <tr key={c.course_id}>
                            <td>
                              {c.course_code} - {c.course_name}
                            </td>
                            <td>{c.total_classes}</td>
                            <td>{c.attendance_percentage}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </td>
                </tr>
              )}
            </Fragment>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={6} style={{ textAlign: "center", padding: 32 }}>
                No data
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function ChronicLatecomersTab() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardAPI
      .chronicLatecomers()
      .then((res) => setRows(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Student</th>
            <th>Course</th>
            <th>Late</th>
            <th>LP</th>
            <th>ECA</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td>
                {r.student_name} <span className="muted">({r.student_code})</span>
              </td>
              <td>{r.course_code}</td>
              <td>{r.late_count}</td>
              <td>{r.lp_count}</td>
              <td>{r.eca_count}</td>
              <td>
                <strong>{r.total_late_related}</strong>
              </td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={6} style={{ textAlign: "center", padding: 32 }}>
                No chronic latecomers
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

function IncompleteRecordsTab() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardAPI
      .incompleteRecords()
      .then((res) => setRows(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="incomplete-list">
      {rows.map((r) => (
        <div key={r.course_id} className="panel incomplete-card">
          <h3>
            {r.course_code} - {r.course_name}
          </h3>
          <p className="muted">
            {r.marked_count} marked / {r.enrolled_count} enrolled &middot; {r.unmarked_count} missing
          </p>
          <ul>
            {r.missing_dates.map((d, i) => (
              <li key={i}>
                <strong>{d.date}</strong> — {d.unmarked_count} unmarked:{" "}
                {d.unmarked_students.join(", ")}
                {d.unmarked_count > d.unmarked_students.length ? ", ..." : ""}
              </li>
            ))}
          </ul>
        </div>
      ))}
      {!loading && rows.length === 0 && <div className="loading">No incomplete records — all clear</div>}
    </div>
  );
}

function BulkImportTab() {
  const [json, setJson] = useState("[]");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const runImport = async (dryRun) => {
    setError("");
    setResult(null);
    let parsed;
    try {
      parsed = JSON.parse(json);
    } catch {
      setError("Invalid JSON");
      return;
    }
    setBusy(true);
    try {
      const res = await dashboardAPI.masterDataImport(parsed, dryRun);
      setResult(res.data);
    } catch (err) {
      setError(JSON.stringify(err.response?.data || err.message));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="panel">
      <p className="muted" style={{ marginBottom: 12 }}>
        Paste a JSON array of records: student_id, course_code, first_name, last_name, email, program,
        section, course_name.
      </p>
      <textarea
        className="import-textarea"
        value={json}
        onChange={(e) => setJson(e.target.value)}
        rows={10}
      />
      <div className="modal-actions" style={{ marginTop: 16 }}>
        <button className="btn btn-secondary" disabled={busy} onClick={() => runImport(true)}>
          Dry Run
        </button>
        <button className="btn btn-primary" disabled={busy} onClick={() => runImport(false)}>
          Import
        </button>
      </div>
      {error && <p style={{ color: "#dc2626", marginTop: 16 }}>{error}</p>}
      {result && (
        <div style={{ marginTop: 16 }}>
          <p>
            {result.dry_run ? "Dry run" : "Import"} complete — created: {result.created}, updated:{" "}
            {result.updated}, skipped: {result.skipped}
          </p>
          {result.errors.length > 0 && (
            <pre className="import-errors">{JSON.stringify(result.errors, null, 2)}</pre>
          )}
        </div>
      )}
    </div>
  );
}

export default function Reports() {
  const { user } = useAuth();
  const [tab, setTab] = useState("stats");
  const visibleTabs = TABS.filter((t) => !t.adminOnly || user?.role === "admin");

  return (
    <div className="page">
      <div className="page-header">
        <h1>Reports</h1>
      </div>

      <div className="tabs">
        {visibleTabs.map((t) => (
          <button
            key={t.key}
            className={`tab-btn ${tab === t.key ? "active" : ""}`}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "stats" && <AttendanceStatsTab />}
      {tab === "faculty" && <FacultyPerformanceTab />}
      {tab === "latecomers" && <ChronicLatecomersTab />}
      {tab === "incomplete" && <IncompleteRecordsTab />}
      {tab === "import" && user?.role === "admin" && <BulkImportTab />}
    </div>
  );
}
