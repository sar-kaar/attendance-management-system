import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import PlaceholderScreen from '../screens/PlaceholderScreen';

export type FacultyTabParamList = {
  MarkAttendance: undefined;
  Dashboard: undefined;
  Courses: undefined;
  Profile: undefined;
};

const Tab = createBottomTabNavigator<FacultyTabParamList>();

// Empty shell per docs/mobile-architecture.md Navigation. Screen content is
// filled in by Phase 17 (attendance marking), Phase 18 (face recognition),
// Phase 20 (dashboard), Phase 23 (profile).
export default function FacultyNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="MarkAttendance">
        {() => <PlaceholderScreen title="Mark Attendance" />}
      </Tab.Screen>
      <Tab.Screen name="Dashboard">{() => <PlaceholderScreen title="Dashboard" />}</Tab.Screen>
      <Tab.Screen name="Courses">{() => <PlaceholderScreen title="Courses" />}</Tab.Screen>
      <Tab.Screen name="Profile">{() => <PlaceholderScreen title="Profile" />}</Tab.Screen>
    </Tab.Navigator>
  );
}
