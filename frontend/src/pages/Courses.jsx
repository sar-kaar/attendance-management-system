import { useState, useEffect } from "react";
import { courseAPI, enrollmentAPI, studentAPI } from "../services/api";
import { FaPlus, FaEdit, FaTrash } from "react-icons/fa";
import "../styles/table.css";

export default function Courses() {
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
      setEditCourse(null);
      setForm({ name: "", code: "", description: "", credits: 3 });
      loadCourses();
    } catch (err) {
      alert(JSON.stringify(err.response?.data));
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
    if (!confirm("Delete this course?")) return;
    await courseAPI.delete(id);
    loadCourses();
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
