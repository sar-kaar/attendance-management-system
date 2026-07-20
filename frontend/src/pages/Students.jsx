import { useState, useEffect } from "react";
import { studentAPI } from "../services/api";
import { FaPlus, FaEdit, FaTrash, FaSearch } from "react-icons/fa";
import { useNotify, formatApiError } from "../context/NotificationContext";
import "../styles/table.css";

export default function Students() {
  const { notify, confirm } = useNotify();
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [editStudent, setEditStudent] = useState(null);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    student_id: "",
    phone: "",
    program: "",
    section: "",
    date_of_birth: "",
    address: "",
  });

  const loadStudents = () => {
    setLoading(true);
    studentAPI
      .list({ search: search || undefined })
      .then((res) => setStudents(res.data.results || res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadStudents();
  }, [search]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editStudent) {
        await studentAPI.update(editStudent.id, form);
      } else {
        await studentAPI.create(form);
      }
      setShowModal(false);
      resetForm();
      loadStudents();
      notify(editStudent ? "Student updated." : "Student added.", "success");
      setEditStudent(null);
    } catch (err) {
      notify(formatApiError(err, "Could not save the student."), "error");
    }
  };

  const handleEdit = (student) => {
    setEditStudent(student);
    setForm({
      first_name: student.first_name,
      last_name: student.last_name,
      email: student.email,
      student_id: student.student_id,
      phone: student.phone || "",
      program: student.program || "",
      section: student.section || "",
      date_of_birth: student.date_of_birth || "",
      address: student.address || "",
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    const ok = await confirm({
      title: "Delete student?",
      message: "Their enrollments and attendance history may be affected. This cannot be undone.",
      confirmText: "Delete",
      danger: true,
    });
    if (!ok) return;
    try {
      await studentAPI.delete(id);
      loadStudents();
      notify("Student deleted.", "success");
    } catch (err) {
      notify(formatApiError(err, "Could not delete the student."), "error");
    }
  };

  const resetForm = () => {
    setForm({
      first_name: "",
      last_name: "",
      email: "",
      student_id: "",
      phone: "",
      program: "",
      section: "",
      date_of_birth: "",
      address: "",
    });
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Student Management</h1>
        <button
          className="btn btn-primary"
          onClick={() => {
            resetForm();
            setEditStudent(null);
            setShowModal(true);
          }}
        >
          <FaPlus /> Add Student
        </button>
      </div>

      <div className="search-bar">
        <FaSearch className="search-icon" />
        <input
          type="text"
          placeholder="Search by name, ID, or email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Program</th>
                <th>Section</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id}>
                  <td>{s.student_id}</td>
                  <td>
                    {s.first_name} {s.last_name}
                  </td>
                  <td>{s.email}</td>
                  <td>{s.program || "-"}</td>
                  <td>{s.section || "-"}</td>
                  <td>
                    <span className={`badge ${s.is_active ? "active" : "inactive"}`}>
                      {s.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="actions">
                    <button onClick={() => handleEdit(s)} className="btn-icon">
                      <FaEdit />
                    </button>
                    <button onClick={() => handleDelete(s.id)} className="btn-icon danger">
                      <FaTrash />
                    </button>
                  </td>
                </tr>
              ))}
              {students.length === 0 && (
                <tr>
                  <td colSpan={7} style={{ textAlign: "center", padding: 32 }}>
                    No students found
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
            <h2>{editStudent ? "Edit Student" : "Add Student"}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>First Name</label>
                  <input
                    value={form.first_name}
                    onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Last Name</label>
                  <input
                    value={form.last_name}
                    onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Student ID</label>
                  <input
                    value={form.student_id}
                    onChange={(e) => setForm({ ...form, student_id: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Phone</label>
                  <input
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Program</label>
                  <input
                    value={form.program}
                    onChange={(e) => setForm({ ...form, program: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Section</label>
                  <input
                    value={form.section}
                    onChange={(e) => setForm({ ...form, section: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Date of Birth</label>
                  <input
                    type="date"
                    value={form.date_of_birth}
                    onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })}
                  />
                </div>
                <div className="form-group full-width">
                  <label>Address</label>
                  <textarea
                    value={form.address}
                    onChange={(e) => setForm({ ...form, address: e.target.value })}
                    rows={2}
                  />
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editStudent ? "Update" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
