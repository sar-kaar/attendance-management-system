import { useState, useEffect } from "react";
import { attendanceAPI, courseAPI, studentAPI, enrollmentAPI } from "../services/api";
import { FaDownload, FaFilePdf, FaFileCsv } from "react-icons/fa";
import { useNotify, formatApiError } from "../context/NotificationContext";
import "../styles/table.css";

export default function Attendance() {
  const { notify } = useNotify();
  const [records, setRecords] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ course: "", date: "" });
  const [showBulkModal, setShowBulkModal] = useState(false);
  const [bulkForm, setBulkForm] = useState({ course_id: "", date: "", records: [] });
  const [enrolledStudents, setEnrolledStudents] = useState([]);

  const loadRecords = () => {
    setLoading(true);
    attendanceAPI
      .list({
        course: filters.course || undefined,
        date: filters.date || undefined,
      })
      .then((res) => setRecords(res.data.results || res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    courseAPI.list().then((res) => setCourses(res.data.results || res.data));
  }, []);

  useEffect(() => {
    loadRecords();
  }, [filters]);

  const loadEnrolled = async (courseId) => {
    if (!courseId) {
      setEnrolledStudents([]);
      return;
    }
    const res = await enrollmentAPI.list({ course: courseId, is_active: "true" });
    const enrollments = res.data.results || res.data;
    setEnrolledStudents(
      enrollments.map((e) => ({
        student_id: e.student_name,
        student: e.student,
        status: "present",
      }))
    );
    setBulkForm((prev) => ({
      ...prev,
      course_id: courseId,
      records: enrollments.map((e) => ({
        student_id: e.student_name,
        status: "present",
      })),
    }));
  };

  const handleBulkSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        course_id: parseInt(bulkForm.course_id),
        date: bulkForm.date,
        records: bulkForm.records,
      };
      await attendanceAPI.markBulk(payload);
      setShowBulkModal(false);
      loadRecords();
      notify("Attendance saved.", "success");
    } catch (err) {
      notify(formatApiError(err, "Could not save attendance."), "error");
    }
  };

  const handleExport = async (type) => {
    const params = {
      course: filters.course || undefined,
      start_date: filters.date || undefined,
      end_date: filters.date || undefined,
    };
    const res = type === "csv" ? await attendanceAPI.exportCSV(params) : await attendanceAPI.exportPDF(params);
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = `attendance_report.${type}`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const updateBulkRecord = (index, field, value) => {
    setBulkForm((prev) => {
      const records = [...prev.records];
      records[index] = { ...records[index], [field]: value };
      return { ...prev, records };
    });
  };

  const statusColor = (status) => {
    switch (status) {
      case "present":
        return { background: "#dcfce7", color: "#16a34a" };
      case "absent":
        return { background: "#fee2e2", color: "#dc2626" };
      case "late":
      case "lp":
        return { background: "#fef3c7", color: "#d97706" };
      case "eca":
        return { background: "#ede9fe", color: "#7c3aed" };
      default:
        return { background: "#f3f4f6", color: "#6b7280" };
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Attendance Management</h1>
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn btn-primary" onClick={() => setShowBulkModal(true)}>
            Mark Bulk Attendance
          </button>
          <button className="btn btn-secondary" onClick={() => handleExport("csv")}>
            <FaFileCsv /> CSV
          </button>
          <button className="btn btn-secondary" onClick={() => handleExport("pdf")}>
            <FaFilePdf /> PDF
          </button>
        </div>
      </div>

      <div className="filter-bar">
        <select
          value={filters.course}
          onChange={(e) => setFilters({ ...filters, course: e.target.value })}
        >
          <option value="">All Courses</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.code} - {c.name}
            </option>
          ))}
        </select>
        <input
          type="date"
          value={filters.date}
          onChange={(e) => setFilters({ ...filters, date: e.target.value })}
        />
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Student</th>
                <th>Course</th>
                <th>Date</th>
                <th>Status</th>
                <th>Marked By</th>
                <th>Remarks</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r) => (
                <tr key={r.id}>
                  <td>{r.student_name}</td>
                  <td>{r.course_name}</td>
                  <td>{r.date}</td>
                  <td>
                    <span className="badge" style={statusColor(r.status)}>
                      {r.status}
                    </span>
                  </td>
                  <td>{r.marked_by}</td>
                  <td>{r.remarks || "-"}</td>
                </tr>
              ))}
              {records.length === 0 && (
                <tr>
                  <td colSpan={6} style={{ textAlign: "center", padding: 32 }}>
                    No attendance records found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {showBulkModal && (
        <div className="modal-overlay" onClick={() => setShowBulkModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Mark Bulk Attendance</h2>
            <form onSubmit={handleBulkSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Course</label>
                  <select
                    value={bulkForm.course_id}
                    onChange={(e) => {
                      setBulkForm({ ...bulkForm, course_id: e.target.value });
                      loadEnrolled(e.target.value);
                    }}
                    required
                  >
                    <option value="">Select Course</option>
                    {courses.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.code} - {c.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Date</label>
                  <input
                    type="date"
                    value={bulkForm.date}
                    onChange={(e) => setBulkForm({ ...bulkForm, date: e.target.value })}
                    required
                  />
                </div>
              </div>

              {bulkForm.records.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <label style={{ fontWeight: 500, fontSize: 14 }}>Student Attendance</label>
                  <table style={{ marginTop: 8 }}>
                    <thead>
                      <tr>
                        <th>Student</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {bulkForm.records.map((rec, i) => (
                        <tr key={i}>
                          <td>{rec.student_id}</td>
                          <td>
                            <select
                              value={rec.status}
                              onChange={(e) => updateBulkRecord(i, "status", e.target.value)}
                            >
                              <option value="present">Present</option>
                              <option value="absent">Absent</option>
                              <option value="late">Late</option>
                              <option value="lp">Late Present</option>
                              <option value="eca">ECA</option>
                            </select>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowBulkModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Submit
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
