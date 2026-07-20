import { useState, useEffect } from "react";
import { attendanceCodeAPI } from "../services/api";
import { useAuth } from "../context/AuthContext";
import { FaPlus, FaEdit, FaTrash } from "react-icons/fa";
import { useNotify, formatApiError } from "../context/NotificationContext";
import "../styles/table.css";

export default function AttendanceCodes() {
  const { user } = useAuth();
  const { notify, confirm } = useNotify();
  const isAdmin = user?.role === "admin";
  const [codes, setCodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editCode, setEditCode] = useState(null);
  const [form, setForm] = useState({ code: "", label: "", description: "", is_active: true });

  const loadCodes = () => {
    setLoading(true);
    attendanceCodeAPI
      .list()
      .then((res) => setCodes(res.data.results || res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadCodes();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editCode) {
        await attendanceCodeAPI.update(editCode.id, form);
      } else {
        await attendanceCodeAPI.create(form);
      }
      setShowModal(false);
      loadCodes();
      notify(editCode ? "Attendance code updated." : "Attendance code created.", "success");
      setEditCode(null);
    } catch (err) {
      notify(formatApiError(err, "Could not save the attendance code."), "error");
    }
  };

  const handleEdit = (code) => {
    setEditCode(code);
    setForm({
      code: code.code,
      label: code.label,
      description: code.description || "",
      is_active: code.is_active,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    const ok = await confirm({
      title: "Delete attendance code?",
      message: "This cannot be undone.",
      confirmText: "Delete",
      danger: true,
    });
    if (!ok) return;
    try {
      await attendanceCodeAPI.delete(id);
      loadCodes();
      notify("Attendance code deleted.", "success");
    } catch (err) {
      // The delete used to be unguarded, so a failure vanished silently and
      // the row simply stayed put with no explanation.
      notify(formatApiError(err, "Could not delete the attendance code."), "error");
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Attendance Codes</h1>
        {isAdmin && (
          <button
            className="btn btn-primary"
            onClick={() => {
              setForm({ code: "", label: "", description: "", is_active: true });
              setEditCode(null);
              setShowModal(true);
            }}
          >
            <FaPlus /> Add Code
          </button>
        )}
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Code</th>
                <th>Label</th>
                <th>Description</th>
                <th>Status</th>
                {isAdmin && <th>Actions</th>}
              </tr>
            </thead>
            <tbody>
              {codes.map((c) => (
                <tr key={c.id}>
                  <td>
                    <strong>{c.code}</strong>
                  </td>
                  <td>{c.label}</td>
                  <td>{c.description || "-"}</td>
                  <td>
                    <span className={`badge ${c.is_active ? "active" : "inactive"}`}>
                      {c.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  {isAdmin && (
                    <td className="actions">
                      <button onClick={() => handleEdit(c)} className="btn-icon">
                        <FaEdit />
                      </button>
                      <button onClick={() => handleDelete(c.id)} className="btn-icon danger">
                        <FaTrash />
                      </button>
                    </td>
                  )}
                </tr>
              ))}
              {codes.length === 0 && (
                <tr>
                  <td colSpan={isAdmin ? 5 : 4} style={{ textAlign: "center", padding: 32 }}>
                    No attendance codes configured
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
            <h2>{editCode ? "Edit Code" : "Add Code"}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Code</label>
                  <input
                    value={form.code}
                    onChange={(e) => setForm({ ...form, code: e.target.value.toUpperCase() })}
                    required
                    maxLength={10}
                  />
                </div>
                <div className="form-group">
                  <label>Label</label>
                  <input
                    value={form.label}
                    onChange={(e) => setForm({ ...form, label: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group full-width">
                  <label>Description</label>
                  <textarea
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    rows={2}
                  />
                </div>
                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={form.is_active}
                      onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                      style={{ marginRight: 8 }}
                    />
                    Active
                  </label>
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editCode ? "Update" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
