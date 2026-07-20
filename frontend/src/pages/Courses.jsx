import { useState, useEffect } from "react";
import { courseAPI } from "../services/api";
import { FaPlus, FaEdit, FaTrash } from "react-icons/fa";
import { useNotify, formatApiError } from "../context/NotificationContext";
import "../styles/table.css";

export default function Courses() {
  const { notify, confirm } = useNotify();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editCourse, setEditCourse] = useState(null);
  const [form, setForm] = useState({
    name: "",
    code: "",
    description: "",
    credits: 3,
  });

  const loadCourses = () => {
    setLoading(true);
    courseAPI
      .list()
      .then((res) => setCourses(res.data.results || res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadCourses();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editCourse) {
        await courseAPI.update(editCourse.id, form);
      } else {
        await courseAPI.create(form);
      }
      setShowModal(false);
      setForm({ name: "", code: "", description: "", credits: 3 });
      loadCourses();
      notify(editCourse ? "Course updated." : "Course created.", "success");
      setEditCourse(null);
    } catch (err) {
      notify(formatApiError(err, "Could not save the course."), "error");
    }
  };

  const handleEdit = (course) => {
    setEditCourse(course);
    setForm({
      name: course.name,
      code: course.code,
      description: course.description || "",
      credits: course.credits,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    const ok = await confirm({
      title: "Delete course?",
      message: "Enrollments and attendance recorded against it may be affected.",
      confirmText: "Delete",
      danger: true,
    });
    if (!ok) return;
    try {
      await courseAPI.delete(id);
      loadCourses();
      notify("Course deleted.", "success");
    } catch (err) {
      notify(formatApiError(err, "Could not delete the course."), "error");
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Course Management</h1>
        <button
          className="btn btn-primary"
          onClick={() => {
            setForm({ name: "", code: "", description: "", credits: 3 });
            setEditCourse(null);
            setShowModal(true);
          }}
        >
          <FaPlus /> Add Course
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Code</th>
                <th>Name</th>
                <th>Credits</th>
                <th>Faculty</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((c) => (
                <tr key={c.id}>
                  <td>{c.code}</td>
                  <td>{c.name}</td>
                  <td>{c.credits}</td>
                  <td>{c.faculty_name || "-"}</td>
                  <td>
                    <span className={`badge ${c.is_active ? "active" : "inactive"}`}>
                      {c.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="actions">
                    <button onClick={() => handleEdit(c)} className="btn-icon">
                      <FaEdit />
                    </button>
                    <button onClick={() => handleDelete(c.id)} className="btn-icon danger">
                      <FaTrash />
                    </button>
                  </td>
                </tr>
              ))}
              {courses.length === 0 && (
                <tr>
                  <td colSpan={6} style={{ textAlign: "center", padding: 32 }}>
                    No courses found
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
            <h2>{editCourse ? "Edit Course" : "Add Course"}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Course Name</label>
                  <input
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Course Code</label>
                  <input
                    value={form.code}
                    onChange={(e) => setForm({ ...form, code: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Credits</label>
                  <input
                    type="number"
                    value={form.credits}
                    onChange={(e) => setForm({ ...form, credits: parseInt(e.target.value) || 0 })}
                    required
                  />
                </div>
                <div className="form-group full-width">
                  <label>Description</label>
                  <textarea
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    rows={3}
                  />
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editCourse ? "Update" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
