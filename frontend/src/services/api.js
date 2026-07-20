import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          localStorage.setItem("access_token", res.data.access);
          if (res.data.refresh) {
            localStorage.setItem("refresh_token", res.data.refresh);
          }
          originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
          return api(originalRequest);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post("/auth/login/", credentials),
  register: (data) => api.post("/auth/register/", data),
  me: () => api.get("/auth/me/"),
};

// The OTP itself is never sent to the browser - we only ask the server to mail
// one, then hand back whatever the user typed for the server to judge.
export const otpAPI = {
  send: (email, purpose = "email_verification") =>
    api.post("/auth/otp/send/", { email, purpose }),
  verify: (email, code, purpose = "email_verification") =>
    api.post("/auth/otp/verify/", { email, code, purpose }),
};

// The provider token is posted straight to our backend, which validates it
// against Google/Facebook before issuing our own JWTs.
export const socialAPI = {
  google: (token) => api.post("/auth/google/", { token }),
  facebook: (token) => api.post("/auth/facebook/", { token }),
};

export const studentAPI = {
  list: (params) => api.get("/students/", { params }),
  get: (id) => api.get(`/students/${id}/`),
  create: (data) => api.post("/students/", data),
  update: (id, data) => api.put(`/students/${id}/`, data),
  patch: (id, data) => api.patch(`/students/${id}/`, data),
  delete: (id) => api.delete(`/students/${id}/`),
};

export const courseAPI = {
  list: (params) => api.get("/courses/", { params }),
  get: (id) => api.get(`/courses/${id}/`),
  create: (data) => api.post("/courses/", data),
  update: (id, data) => api.put(`/courses/${id}/`, data),
  delete: (id) => api.delete(`/courses/${id}/`),
};

export const enrollmentAPI = {
  list: (params) => api.get("/enrollments/", { params }),
  get: (id) => api.get(`/enrollments/${id}/`),
  create: (data) => api.post("/enrollments/", data),
  update: (id, data) => api.put(`/enrollments/${id}/`, data),
  delete: (id) => api.delete(`/enrollments/${id}/`),
};

export const attendanceAPI = {
  list: (params) => api.get("/attendance/", { params }),
  get: (id) => api.get(`/attendance/${id}/`),
  create: (data) => api.post("/attendance/", data),
  update: (id, data) => api.put(`/attendance/${id}/`, data),
  delete: (id) => api.delete(`/attendance/${id}/`),
  markBulk: (data) => api.post("/attendance/mark_bulk/", data),
  myAttendance: (studentId) =>
    api.get("/attendance/my_attendance/", { params: { student_id: studentId } }),
  report: (params) => api.get("/attendance/report/", { params }),
  dashboard: () => api.get("/attendance/dashboard/"),
  exportCSV: (params) =>
    api.get("/attendance/export_csv/", { params, responseType: "blob" }),
  exportPDF: (params) =>
    api.get("/attendance/export_pdf/", { params, responseType: "blob" }),
};

export const dashboardAPI = {
  searchStudents: (search) => api.get("/dashboard/students/", { params: { search } }),
  atRisk: (params) => api.get("/dashboard/at-risk/", { params }),
  attendanceStats: (params) => api.get("/dashboard/attendance-stats/", { params }),
  facultyPerformance: (params) => api.get("/dashboard/faculty-performance/", { params }),
  chronicLatecomers: (params) => api.get("/dashboard/chronic-latecomers/", { params }),
  incompleteRecords: (params) => api.get("/dashboard/incomplete-records/", { params }),
  masterDataImport: (data, dryRun) =>
    api.post("/dashboard/master-data/import/", data, { params: { dry_run: dryRun } }),
};

export const attendanceCodeAPI = {
  list: () => api.get("/attendance/codes/"),
  create: (data) => api.post("/attendance/codes/", data),
  update: (id, data) => api.put(`/attendance/codes/${id}/`, data),
  delete: (id) => api.delete(`/attendance/codes/${id}/`),
};

export const faceAPI = {
  register: (formData) =>
    api.post("/face/register/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  recognize: (formData) =>
    api.post("/face/recognize/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  markAttendance: (formData) =>
    api.post("/face/mark-attendance/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  registered: () => api.get("/face/registered/"),
};

export default api;