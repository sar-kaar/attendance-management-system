import { useState, useEffect, useRef } from "react";
import { faceAPI, courseAPI } from "../services/api";
import { FaCamera, FaUserPlus, FaList } from "react-icons/fa";
import "../styles/table.css";

export default function FaceRecognition() {
  const [registeredFaces, setRegisteredFaces] = useState([]);
  const [courses, setCourses] = useState([]);
  const [activeTab, setActiveTab] = useState("register");
  const [selectedCourse, setSelectedCourse] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const webcamRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    faceAPI.registered().then((res) => setRegisteredFaces(res.data.students || []));
    courseAPI.list().then((res) => setCourses(res.data.results || res.data));
  }, []);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("image", file);

      if (activeTab === "register") {
        const studentId = prompt("Enter Student ID to register face for:");
        if (!studentId) {
          setLoading(false);
          return;
        }
        formData.append("student_id", studentId);
        const res = await faceAPI.register(formData);
        setResult({ type: "success", message: res.data.message });
        faceAPI.registered().then((r) => setRegisteredFaces(r.data.students || []));
      } else if (activeTab === "recognize") {
        const res = await faceAPI.recognize(formData);
        setResult({
          type: res.data.matched ? "success" : "warning",
          data: res.data,
        });
      } else if (activeTab === "mark") {
        if (!selectedCourse) {
          alert("Please select a course first");
          setLoading(false);
          return;
        }
        formData.append("course_id", selectedCourse);
        const res = await faceAPI.markAttendance(formData);
        setResult({
          type: res.data.marked ? "success" : "warning",
          data: res.data,
        });
      }
    } catch (err) {
      setResult({
        type: "error",
        message: err.response?.data?.error || "Operation failed",
      });
    } finally {
      setLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const tabs = [
    { id: "register", label: "Register Face", icon: <FaUserPlus /> },
    { id: "recognize", label: "Recognize Face", icon: <FaCamera /> },
    { id: "mark", label: "Mark Attendance", icon: <FaCamera /> },
    { id: "list", label: "Registered Faces", icon: <FaList /> },
  ];

  return (
    <div className="page">
      <h1>Face Recognition</h1>

      <div className="tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? "active" : ""}`}
            onClick={() => {
              setActiveTab(tab.id);
              setResult(null);
            }}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      <div className="panel" style={{ marginTop: 24 }}>
        {activeTab === "list" ? (
          <div>
            <h3>Registered Faces ({registeredFaces.length})</h3>
            <table style={{ marginTop: 16 }}>
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Name</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {registeredFaces.map((f) => (
                  <tr key={f.student_id}>
                    <td>{f.student_id}</td>
                    <td>{f.name}</td>
                    <td>
                      <span className="badge active">Registered</span>
                    </td>
                  </tr>
                ))}
                {registeredFaces.length === 0 && (
                  <tr>
                    <td colSpan={3} style={{ textAlign: "center", padding: 32 }}>
                      No faces registered yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        ) : (
          <div>
            <h3>
              {activeTab === "register" && "Register New Face"}
              {activeTab === "recognize" && "Identify Student"}
              {activeTab === "mark" && "Mark Attendance by Face"}
            </h3>

            {activeTab === "mark" && (
              <div className="form-group" style={{ marginTop: 16, maxWidth: 300 }}>
                <label>Select Course</label>
                <select value={selectedCourse} onChange={(e) => setSelectedCourse(e.target.value)}>
                  <option value="">Select Course</option>
                  {courses.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.code} - {c.name}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div style={{ marginTop: 24 }}>
              <input
                type="file"
                accept="image/*"
                capture="environment"
                ref={fileInputRef}
                onChange={handleImageUpload}
                style={{ display: "none" }}
                id="face-input"
              />
              <label htmlFor="face-input" className="btn btn-primary" style={{ cursor: "pointer" }}>
                <FaCamera /> {loading ? "Processing..." : "Take Photo / Upload Image"}
              </label>
            </div>

            {result && (
              <div
                className={`result-box ${result.type}`}
                style={{
                  marginTop: 24,
                  padding: 16,
                  borderRadius: 8,
                  background:
                    result.type === "success"
                      ? "#dcfce7"
                      : result.type === "warning"
                      ? "#fef3c7"
                      : "#fee2e2",
                }}
              >
                {result.message && <p>{result.message}</p>}
                {result.data && (
                  <pre style={{ fontSize: 13, whiteSpace: "pre-wrap" }}>
                    {JSON.stringify(result.data, null, 2)}
                  </pre>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      <style>{`
        .tabs {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }
        .tab {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 20px;
          border: 1px solid #d0d0d0;
          border-radius: 8px;
          background: white;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.2s;
        }
        .tab.active {
          background: #4a90d9;
          color: white;
          border-color: #4a90d9;
        }
        .tab:hover:not(.active) {
          background: #f0f0f0;
        }

      `}</style>
    </div>
  );
}
