import { useState, useEffect } from "react";
import { adminUserAPI } from "../services/api";
import { FaPlus, FaEdit, FaTrash, FaKey } from "react-icons/fa";
import { useNotify, formatApiError } from "../context/NotificationContext";
import "../styles/table.css";

const emptyForm = {
  username: "",
  email: "",
  password: "",
  role: "faculty",
  phone: "",
  first_name: "",
  last_name: "",
  is_active: true,
  student_id: "",
};

export default function Users() {
  const { notify, confirm } = useNotify();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [resetUser, setResetUser] = useState(null);
  const [resetPassword, setResetPassword] = useState("");

  const loadUsers = (role) => {
    setLoading(true);
    adminUserAPI
      .list(role ? { role } : undefined)
      .then((res) => setUsers(res.data.results || res.data))
      .catch((err) => notify(formatApiError(err, "Could not load users."), "error"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetch-on-filter-change, standard data-loading pattern
    loadUsers(roleFilter);
  }, [roleFilter]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { ...form };
    if (editUser && !payload.password) delete payload.password;
    if (!payload.student_id) delete payload.student_id;
    try {
      if (editUser) {
        await adminUserAPI.update(editUser.id, payload);
      } else {
        await adminUserAPI.create(payload);
      }
      setShowModal(false);
      setForm(emptyForm);
      setEditUser(null);
      loadUsers(roleFilter);
      notify(editUser ? "User updated." : "User created.", "success");
    } catch (err) {
      notify(formatApiError(err, "Could not save the user."), "error");
    }
  };

  const handleEdit = (u) => {
    setEditUser(u);
    setForm({
      username: u.username,
      email: u.email,
      password: "",
      role: u.role,
      phone: u.phone || "",
      first_name: u.first_name || "",
      last_name: u.last_name || "",
      is_active: u.is_active,
      student_id: "",
    });
    setShowModal(true);
  };

  const handleDelete = async (u) => {
    const ok = await confirm({
      title: "Delete user account?",
      message: `This permanently removes ${u.username}'s login. It does not delete any linked Student record.`,
      confirmText: "Delete",
      danger: true,
    });
    if (!ok) return;
    try {
      await adminUserAPI.delete(u.id);
      loadUsers(roleFilter);
      notify("User deleted.", "success");
    } catch (err) {
      notify(formatApiError(err, "Could not delete the user."), "error");
    }
  };

  const handleResetPasswordSubmit = async (e) => {
    e.preventDefault();
    if (resetPassword.length < 6) {
      notify("Password must be at least 6 characters.", "error");
      return;
    }
    try {
      await adminUserAPI.resetPassword(resetUser.id, resetPassword);
      notify(`Password reset for ${resetUser.username}.`, "success");
      setResetUser(null);
      setResetPassword("");
    } catch (err) {
      notify(formatApiError(err, "Could not reset the password."), "error");
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>User Management</h1>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <select value={roleFilter} onChange={(e) => setRoleFilter(e.target.value)}>
            <option value="">All roles</option>
            <option value="admin">Admin</option>
            <option value="faculty">Faculty</option>
            <option value="student">Student</option>
          </select>
          <button
            className="btn btn-primary"
            onClick={() => {
              setForm(emptyForm);
              setEditUser(null);
              setShowModal(true);
            }}
          >
            <FaPlus /> Add User
          </button>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Username</th>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Linked Student</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.username}</td>
                  <td>{[u.first_name, u.last_name].filter(Boolean).join(" ") || "-"}</td>
                  <td>{u.email}</td>
                  <td>
                    <span className={`badge role-${u.role}`}>{u.role}</span>
                  </td>
                  <td>{u.linked_student_id || "-"}</td>
                  <td>
                    <span className={`badge ${u.is_active ? "active" : "inactive"}`}>
                      {u.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="actions">
                    <button onClick={() => handleEdit(u)} className="btn-icon" title="Edit">
                      <FaEdit />
                    </button>
                    <button
                      onClick={() => {
                        setResetUser(u);
                        setResetPassword("");
                      }}
                      className="btn-icon"
                      title="Reset password"
                    >
                      <FaKey />
                    </button>
                    <button
                      onClick={() => handleDelete(u)}
                      className="btn-icon danger"
                      title="Delete"
                    >
                      <FaTrash />
                    </button>
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan={7} style={{ textAlign: "center", padding: 32 }}>
                    No users found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editUser ? "Edit User" : "Add User"}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Username</label>
                  <input
                    value={form.username}
                    onChange={(e) => setForm({ ...form, username: e.target.value })}
                    required
                    disabled={!!editUser}
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
                  <label>{editUser ? "New Password (leave blank to keep)" : "Password"}</label>
                  <input
                    type="password"
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                    required={!editUser}
                    minLength={6}
                  />
                </div>
                <div className="form-group">
                  <label>Role</label>
                  <select
                    value={form.role}
                    onChange={(e) => setForm({ ...form, role: e.target.value })}
                  >
                    <option value="admin">Admin</option>
                    <option value="faculty">Faculty</option>
                    <option value="student">Student</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>First Name</label>
                  <input
                    value={form.first_name}
                    onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Last Name</label>
                  <input
                    value={form.last_name}
                    onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Phone</label>
                  <input
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                  />
                </div>
                {form.role === "student" && (
                  <div className="form-group">
                    <label>Link to Student ID (optional)</label>
                    <input
                      value={form.student_id}
                      onChange={(e) => setForm({ ...form, student_id: e.target.value })}
                      placeholder="e.g. STU-2026-001"
                    />
                  </div>
                )}
                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={form.is_active}
                      onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                    />
                    &nbsp;&nbsp;Active
                  </label>
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editUser ? "Update" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {resetUser && (
        <div className="modal-overlay">
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Reset password for {resetUser.username}</h2>
            <form onSubmit={handleResetPasswordSubmit}>
              <div className="form-grid">
                <div className="form-group full-width">
                  <label>New Password</label>
                  <input
                    type="password"
                    value={resetPassword}
                    onChange={(e) => setResetPassword(e.target.value)}
                    minLength={6}
                    required
                    autoFocus
                  />
                  <small>
                    Minimum 6 characters. The user is not notified automatically — tell them
                    directly.
                  </small>
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setResetUser(null)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Reset Password
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
