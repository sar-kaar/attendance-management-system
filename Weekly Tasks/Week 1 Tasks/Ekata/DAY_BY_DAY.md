# Ekata — Week 1 (Sprint 0)

**Role:** Frontend Developer
**Branch prefix:** `docs/` or `chore/`
**Full rules:** see `../TEAM_SYNC_PROTOCOL.md` — do "before you start" and "end of day" steps every day below.

### Your scope
- Frontend code: React pages, components, styles, routing
- UI/UX: wireframes, mockups, color scheme
- User Manual doc
- Connecting UI to APIs (starts Sprint 1)

### Trello cards you own
T-003, T-006 · US-01, US-02, US-04, US-06, US-10, US-12, US-13, US-15 · UI/UX Design Research · User Manual

---

## Day 1 (Tue Jul 7) — DONE
Reviewed Trello + project structure, set up Discord notifications, accepted workspace invite. No git work.

## Day 2 (Wed Jul 8) — GitHub invite — partial (meeting did NOT happen)

**Correction: no team meeting happened Jul 8. Only accepting the GitHub collaborator invite is real. The actual kickoff meeting is TODAY (Jul 9) — run it using `Guidelines/06_TOMORROW_MEETING_GUIDE.md` before starting wireframes.** No git work this day.

---

## Day 3 (Thu Jul 9) — Wireframes

Standup 9 AM.

**Before you start:** check Abhishek's `docs/database-schema` branch once it's pushed — your pages need to match those field names later. Confirm with him in Discord if unsure.

```powershell
git checkout develop
git pull origin develop
git checkout -b docs/wireframes
mkdir docs\wireframes
```

**Tool: Figma** (free, collaborative). Create project "AMS - Attendance Management System", one page per screen, share with team.

**Screens to wireframe:**
1. Login — email, password, sign-in button, link to register
2. Register — full name, email, password, role dropdown
3. Dashboard — sidebar nav, 3 stat cards (today/week/month %), recent sessions list, quick actions
4. Student management — search bar, add-student button, table (roll no, name, course, face-registered ✅/❌)
5. Attendance marking — course + date selectors, camera preview, detected count, manual-entry fallback

Export each as PNG into `docs/wireframes/` (`login.png`, `register.png`, `dashboard.png`, `student-management.png`, `attendance-marking.png`).

**Commit + tell the team:**
```powershell
git add .
git commit -m "[docs] Add initial wireframes for core pages"
git push -u origin docs/wireframes
```
Post in Discord: "Wireframes pushed, `docs/wireframes` branch — take a look before I start on React setup."

**Running behind today?** Do Login, Dashboard, and Attendance-marking first — those three drive the most decisions for everyone else. Register and Student-management can slip to Day 4 morning.

---

## Day 4 (Fri Jul 10) — Google Sheets Dashboard Analysis

Standup 9 AM. Teacher meeting 11 AM.

**Important update:** Google Sheets dashboards (SUM I 2026 Dashboard, Testing Dashboard, Student Master Dashboard) were read and analyzed. 10 new user stories were created as GitHub Issues (#17-#26) + Trello cards (86-95) in Product Backlog.

**Key dashboard features your frontend will need to implement (starting Week 2):**
- **US-06 (#19):** Student Academic Dashboard — search + per-subject breakdown + color-coded status
- **US-07 (#17):** Attendance Stats Overview — per-subject stats table
- **US-08 (#18):** Faculty Performance — per-faculty analytics
- **US-09 (#20):** At-Risk Students (<60% attendance)
- **US-10 (#24):** Chronic Latecomers (3+ late marks)
- **US-13 (#22):** Incomplete Records

**React setup tasks from original Day 4 plan remain valid for implementation when ready.**

Reference the Google Sheets layout for dashboard page structure:
- Top: Program/Section/Student search bar with auto-fill
- Main: Subject-wise attendance table with color-coded %
- Tabs: Overview, Faculty, At-Risk, Latecomers, Incomplete

---

## Day 5 (Sat Jul 11) — Base Components

Standup 9 AM.

```powershell
git checkout develop
git pull origin develop
git checkout -b chore/base-components
```

Reusable components — `frontend/src/components/common/`:

`Button.js`:
```javascript
import { Button as MuiButton } from '@mui/material';
const Button = ({ children, variant = 'contained', color = 'primary', ...props }) => (
  <MuiButton variant={variant} color={color} {...props}>{children}</MuiButton>
);
export default Button;
```

`Input.js`:
```javascript
import { TextField } from '@mui/material';
const Input = ({ label, type = 'text', value, onChange, error, helperText, ...props }) => (
  <TextField fullWidth label={label} type={type} value={value} onChange={onChange}
    error={error} helperText={helperText} variant="outlined" margin="normal" {...props} />
);
export default Input;
```

`Card.js`:
```javascript
import { Card as MuiCard, CardContent, CardHeader, Typography } from '@mui/material';
const Card = ({ title, subtitle, children, ...props }) => (
  <MuiCard {...props}>
    {title && <CardHeader title={<Typography variant="h6">{title}</Typography>} subheader={subtitle} />}
    <CardContent>{children}</CardContent>
  </MuiCard>
);
export default Card;
```

`Table.js`:
```javascript
import { DataGrid } from '@mui/x-data-grid';
import { Paper } from '@mui/material';
const Table = ({ rows, columns, pageSize = 10, loading = false, ...props }) => (
  <Paper elevation={0} sx={{ height: 400, width: '100%' }}>
    <DataGrid rows={rows} columns={columns} pageSize={pageSize}
      rowsPerPageOptions={[5, 10, 20]} loading={loading} disableSelectionOnClick {...props} />
  </Paper>
);
export default Table;
```

Layout — `frontend/src/components/Layout/`:

`Navbar.js`:
```javascript
import { AppBar, Toolbar, Typography, IconButton, Avatar } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

const Navbar = ({ onMenuClick }) => (
  <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
    <Toolbar>
      <IconButton color="inherit" edge="start" onClick={onMenuClick} sx={{ mr: 2 }}><MenuIcon /></IconButton>
      <Typography variant="h6" noWrap sx={{ flexGrow: 1 }}>Attendance Management System</Typography>
      <Avatar alt="User" src="/avatar.jpg" />
    </Toolbar>
  </AppBar>
);
export default Navbar;
```

`Sidebar.js`:
```javascript
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import SchoolIcon from '@mui/icons-material/School';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;
const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Students', icon: <PeopleIcon />, path: '/students' },
  { text: 'Courses', icon: <SchoolIcon />, path: '/courses' },
  { text: 'Attendance', icon: <CheckCircleIcon />, path: '/attendance' },
  { text: 'Reports', icon: <AssessmentIcon />, path: '/reports' },
];

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  return (
    <Drawer variant="permanent" sx={{ width: drawerWidth, flexShrink: 0,
      '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box' } }}>
      <Toolbar />
      <List>
        {menuItems.map((item) => (
          <ListItem button key={item.text} selected={location.pathname === item.path}
            onClick={() => navigate(item.path)}>
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};
export default Sidebar;
```

`Layout.js`:
```javascript
import { Box, Toolbar } from '@mui/material';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

const Layout = () => (
  <Box sx={{ display: 'flex' }}>
    <Navbar />
    <Sidebar />
    <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
      <Toolbar />
      <Outlet />
    </Box>
  </Box>
);
export default Layout;
```

Login page — `frontend/src/pages/Login.js`:
```javascript
import { useState } from 'react';
import { Container, Box, Typography, Paper, Link } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Input from '../components/common/Input';
import Button from '../components/common/Button';

const Login = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = (e) => { e.preventDefault(); navigate('/'); }; // TODO: connect to API in Sprint 1

  return (
    <Container maxWidth="xs">
      <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
          <Typography variant="h4" align="center" gutterBottom fontWeight="bold">Attendance MS</Typography>
          <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>Sign in to your account</Typography>
          <form onSubmit={handleSubmit}>
            <Input label="Email" name="email" type="email" value={form.email} onChange={handleChange} />
            <Input label="Password" name="password" type="password" value={form.password} onChange={handleChange} />
            <Button type="submit" fullWidth sx={{ mt: 2, mb: 2 }}>Sign In</Button>
          </form>
          <Typography variant="body2" align="center">
            Don't have an account? <Link href="/register" underline="hover">Register</Link>
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};
export default Login;
```

**Verify:** `npm start`, check login page renders, register link navigates, sidebar highlights active page.

```powershell
git add .
git commit -m "[chore] Add base UI components and routing"
git push -u origin chore/base-components
```

---

## Day 6 (Sun Jul 12) — Review + Merge

Week End Review 4 PM.

- [ ] Get feedback from Prizma + Abhishek on wireframes, update if needed
- [ ] Export final wireframe versions to `docs/wireframes/`

```powershell
git checkout develop
git pull origin develop
git merge docs/wireframes
git merge chore/frontend-setup
git merge chore/base-components
git push origin develop
```

Write `docs/ui-decisions.md` — framework choice (MUI), theme colors, layout (240px sidebar, fixed navbar), page-by-page notes. Keep it short, this is a reference not an essay.

```powershell
git add .
git commit -m "[docs] Add UI decisions documentation"
git push origin develop
```

---

## Week 1 checklist
- [ ] Figma workspace + 5 wireframes exported
- [ ] React project initialized, Material UI themed
- [ ] Router set up with all page routes
- [ ] Reusable components: Button, Input, Card, Table
- [ ] Layout: Navbar, Sidebar, Layout wrapper
- [ ] Login page built
- [ ] UI decisions documented
