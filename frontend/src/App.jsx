import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import DashboardLayout from "./layouts/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import Students from "./pages/Students";
import Courses from "./pages/Courses";
import Attendance from "./pages/Attendance";
import FaceRecognition from "./pages/FaceRecognition";
import StudentDashboard from "./pages/StudentDashboard";
import Enrollments from "./pages/Enrollments";
import AttendanceCodes from "./pages/AttendanceCodes";
import Reports from "./pages/Reports";

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading">Loading...</div>;
  if (!user) return <Navigate to="/login" />;
  return children;
}

function RoleRoute({ children, allowed }) {
  const { user } = useAuth();
  if (!allowed.includes(user?.role)) return <Navigate to="/dashboard" />;
  return children;
}

function AppRoutes() {
  const { user, loading } = useAuth();

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <Routes>
      <Route
        path="/login"
        element={user ? <Navigate to={user.role === "student" ? "/student" : "/dashboard"} /> : <Login />}
      />
      <Route path="/register" element={<Register />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <RoleRoute allowed={["admin", "faculty"]}>
              <DashboardLayout />
            </RoleRoute>
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="students" element={<Students />} />
        <Route path="courses" element={<Courses />} />
        <Route path="attendance" element={<Attendance />} />
        <Route path="face-recognition" element={<FaceRecognition />} />
        <Route path="enrollments" element={<Enrollments />} />
        <Route path="attendance-codes" element={<AttendanceCodes />} />
        <Route path="reports" element={<Reports />} />
      </Route>

      <Route
        path="/student"
        element={
          <ProtectedRoute>
            <RoleRoute allowed={["student"]}>
              <StudentDashboard />
            </RoleRoute>
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
