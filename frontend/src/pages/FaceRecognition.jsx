import { useState, useEffect, useRef, useCallback } from "react";
import Webcam from "react-webcam";
import { faceAPI, courseAPI, dashboardAPI } from "../services/api";
import { FaCamera, FaUserPlus, FaList, FaUpload, FaSyncAlt, FaSearch, FaTimes } from "react-icons/fa";
import "../styles/table.css";

function dataURLtoFile(dataUrl, filename) {
  const [meta, base64] = dataUrl.split(",");
  const mime = meta.match(/:(.*?);/)[1];
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return new File([bytes], filename, { type: mime });
}

export default function FaceRecognition() {
  const [registeredFaces, setRegisteredFaces] = useState([]);
  const [courses, setCourses] = useState([]);
  const [activeTab, setActiveTab] = useState("register");
  const [selectedCourse, setSelectedCourse] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [inputMode, setInputMode] = useState("camera"); // "camera" | "upload"
  const [facingMode, setFacingMode] = useState("user");
  const [cameraError, setCameraError] = useState(null);
  const [studentQuery, setStudentQuery] = useState("");
  const [studentResults, setStudentResults] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [searchingStudents, setSearchingStudents] = useState(false);
  const webcamRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    faceAPI.registered().then((res) => setRegisteredFaces(res.data.students || []));
    courseAPI.list().then((res) => setCourses(res.data.results || res.data));
  }, []);

  useEffect(() => {
    if (activeTab !== "register" || selectedStudent) return;
    if (studentQuery.trim().length < 2) {
      setStudentResults([]);
      return;
    }
    setSearchingStudents(true);
    const handle = setTimeout(() => {
      dashboardAPI
        .searchStudents(studentQuery.trim())
        .then((res) => setStudentResults(res.data || []))
        .catch(() => setStudentResults([]))
        .finally(() => setSearchingStudents(false));
    }, 300);
    return () => clearTimeout(handle);
  }, [studentQuery, activeTab, selectedStudent]);

  const submitImage = async (file) => {
    setLoading(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("image", file);

      if (activeTab === "register") {
        if (!selectedStudent) {
          alert("Please search for and select a student first");
          setLoading(false);
          return;
        }
        formData.append("student_id", selectedStudent.student_id);
        const res = await faceAPI.register(formData);
        setResult({ type: "success", message: res.data.message });
        setSelectedStudent(null);
        setStudentQuery("");
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
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    await submitImage(file);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleCapture = useCallback(() => {
    const screenshot = webcamRef.current?.getScreenshot();
    if (!screenshot) {
      setCameraError("Couldn't capture from camera. Try again or switch to upload.");
      return;
    }
    const file = dataURLtoFile(screenshot, `capture-${Date.now()}.jpg`);
    submitImage(file);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, selectedCourse, selectedStudent]);

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

            {activeTab === "register" && (
              <div className="form-group" style={{ marginTop: 16, maxWidth: 360, position: "relative" }}>
                <label>Student</label>
                {selectedStudent ? (
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      border: "1px solid #d0d0d0",
                      borderRadius: 8,
                      padding: "10px 12px",
                    }}
                  >
                    <span>
                      {selectedStudent.first_name} {selectedStudent.last_name} ({selectedStudent.student_id})
                    </span>
                    <button
                      onClick={() => {
                        setSelectedStudent(null);
                        setStudentQuery("");
                      }}
                      style={{ background: "none", border: "none", cursor: "pointer" }}
                      title="Change student"
                    >
                      <FaTimes />
                    </button>
                  </div>
                ) : (
                  <div style={{ position: "relative" }}>
                    <div style={{ position: "relative" }}>
                      <FaSearch
                        style={{
                          position: "absolute",
                          left: 12,
                          top: "50%",
                          transform: "translateY(-50%)",
                          color: "#999",
                        }}
                      />
                      <input
                        type="text"
                        placeholder="Search by name, ID, or email..."
                        value={studentQuery}
                        onChange={(e) => setStudentQuery(e.target.value)}
                        style={{ width: "100%", padding: "10px 12px 10px 34px", boxSizing: "border-box" }}
                      />
                    </div>
                    {studentQuery.trim().length >= 2 && (
                      <div
                        style={{
                          position: "absolute",
                          top: "100%",
                          left: 0,
                          right: 0,
                          background: "white",
                          border: "1px solid #d0d0d0",
                          borderRadius: 8,
                          marginTop: 4,
                          maxHeight: 240,
                          overflowY: "auto",
                          zIndex: 10,
                          boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
                        }}
                      >
                        {searchingStudents ? (
                          <div style={{ padding: 12, color: "#999" }}>Searching...</div>
                        ) : studentResults.length === 0 ? (
                          <div style={{ padding: 12, color: "#999" }}>No students found</div>
                        ) : (
                          studentResults.map((s) => (
                            <div
                              key={s.id}
                              onClick={() => {
                                setSelectedStudent(s);
                                setStudentResults([]);
                              }}
                              style={{
                                padding: "10px 12px",
                                cursor: "pointer",
                                borderBottom: "1px solid #f0f0f0",
                              }}
                              onMouseEnter={(e) => (e.currentTarget.style.background = "#f5f5f5")}
                              onMouseLeave={(e) => (e.currentTarget.style.background = "white")}
                            >
                              <div>
                                {s.first_name} {s.last_name} ({s.student_id})
                              </div>
                              <div style={{ fontSize: 12, color: "#999" }}>{s.email}</div>
                            </div>
                          ))
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            <div style={{ marginTop: 24 }}>
              <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
                <button
                  className={`tab ${inputMode === "camera" ? "active" : ""}`}
                  onClick={() => {
                    setInputMode("camera");
                    setCameraError(null);
                  }}
                >
                  <FaCamera /> Use Camera
                </button>
                <button
                  className={`tab ${inputMode === "upload" ? "active" : ""}`}
                  onClick={() => setInputMode("upload")}
                >
                  <FaUpload /> Upload Photo
                </button>
              </div>

              {inputMode === "camera" ? (
                <div>
                  {cameraError ? (
                    <div
                      className="result-box error"
                      style={{ padding: 16, borderRadius: 8, background: "#fee2e2", maxWidth: 480 }}
                    >
                      <p>{cameraError}</p>
                    </div>
                  ) : (
                    <div style={{ maxWidth: 480 }}>
                      <Webcam
                        ref={webcamRef}
                        audio={false}
                        screenshotFormat="image/jpeg"
                        videoConstraints={{ facingMode }}
                        onUserMediaError={() =>
                          setCameraError(
                            "Camera access denied or unavailable. Check browser permissions, or switch to Upload Photo."
                          )
                        }
                        style={{ width: "100%", borderRadius: 8 }}
                      />
                      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
                        <button
                          className="btn btn-primary"
                          onClick={handleCapture}
                          disabled={loading}
                        >
                          <FaCamera /> {loading ? "Processing..." : "Capture & Submit"}
                        </button>
                        <button
                          className="btn"
                          onClick={() => setFacingMode((m) => (m === "user" ? "environment" : "user"))}
                          title="Switch camera"
                        >
                          <FaSyncAlt />
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <input
                    type="file"
                    accept="image/*"
                    ref={fileInputRef}
                    onChange={handleImageUpload}
                    style={{ display: "none" }}
                    id="face-input"
                  />
                  <label htmlFor="face-input" className="btn btn-primary" style={{ cursor: "pointer" }}>
                    <FaUpload /> {loading ? "Processing..." : "Choose Image File"}
                  </label>
                </div>
              )}
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
