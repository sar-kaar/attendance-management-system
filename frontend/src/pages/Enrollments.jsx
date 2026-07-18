import { useState, useEffect } from "react";
import { enrollmentAPI, studentAPI, courseAPI } from "../services/api";
import { FaPlus, FaTrash } from "react-icons/fa";
import "../styles/table.css";

export default function Enrollments() {
  const [enrollments, setEnrollments] = useState([]);
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [courseFilter, setCourseFilter] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ student: "", course: "" });
  const [error, setError] = useState("");

  const loadEnrollments = () => {
    setLoading(true);
    enrollmentAPI
      .list(courseFilter ? { course: courseFilter } : undefined)
      .then((res) => setEnrollments(res.data.results || res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    studentAPI.list().then((res) => setStudents(res.data.results || res.data));
    courseAPI.list().then((res) => setCourses(res.data.results || res.data));
  }, []);

  useEffect(() => {
    loadEnrollments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseFilter]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await enrollmentAPI.create(form);
      setShowModal(false);
      setForm({ student: "", course: "" });
      loadEnrollments();
    } catch (err) {
      setError(
        err.response?.data?.non_field_errors?.[0] ||
          JSON.stringify(err.response?.data) ||
          "Failed to enroll student"
      );
    }
  };

  const handleUnenroll = async (enrollment) => {
    if (!confirm(`Remove ${enrollment.student_name} from ${enrollment.course_name}?`)) return;
    await enrollmentAPI.delete(enrollment.id);
    loadEnrollments();
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Enrollments</h1>
        <button
          className="btn btn-primary"
          onClick={() => {
            setForm({ student: "", course: courseFilter || "" });
            setError("");
            setShowModal(true);
          }}
        >
          <FaPlus /> Enroll Student
        </button>
      </div>

      <div className="filter-bar">
        <select value={courseFilter} onChange={(e) => setCourseFilter(e.target.value)}>
          <option value="">All Courses</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.code} - {c.name}
            </option>
          ))}
        </select>
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
                <th>Enrolled Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {enrollments.map((e) => (
                <tr key={e.id}>
                  <td>{e.student_name}</td>
                  <td>{e.course_name}</td>
                  <td>{e.enrolled_date}</td>
                  <td>
                    <span className={`badge ${e.is_active ? "active" : "inactive"}`}>
                      {e.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="actions">
                    <button onClick={() => handleUnenroll(e)} className="btn-icon danger">
                      <FaTrash />
                    </button>
                  </td>
                </tr>
              ))}
              {enrollments.length === 0 && (
                <tr>
                  <td colSpan={5} style={{ textAlign: "center", padding: 32 }}>
                    No enrollments found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Enroll Student</h2>
            {error && (
              <p style={{ color: "#dc2626", marginBottom: 16, fontSize: 13 }}>{error}</p>
            )}
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group full-width">
                  <label>Student</label>
                  <select
                    value={form.student}
                    onChange={(e) => setForm({ ...form, student: e.target.value })}
                    required
                  >
                    <option value="">Select student...</option>
                    {students.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.student_id} - {s.first_name} {s.last_name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group full-width">
                  <label>Course</label>
                  <select
                    value={form.course}
                    onChange={(e) => setForm({ ...form, course: e.target.value })}
                    required
                  >
                    <option value="">Select course...</option>
                    {courses.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.code} - {c.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Enroll
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
