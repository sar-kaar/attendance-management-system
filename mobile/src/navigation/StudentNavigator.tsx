import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import PlaceholderScreen from '../screens/PlaceholderScreen';

export type StudentTabParamList = {
  Attendance: undefined;
  CheckIn: undefined;
  Reports: undefined;
  Profile: undefined;
};

const Tab = createBottomTabNavigator<StudentTabParamList>();

// Empty shell per docs/mobile-architecture.md Navigation. Screen content is
// filled in by Phase 17 (attendance), Phase 19 (reports), Phase 23 (profile).
export default function StudentNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Attendance">
        {() => <PlaceholderScreen title="Attendance" />}
      </Tab.Screen>
      <Tab.Screen name="CheckIn">{() => <PlaceholderScreen title="Check In" />}</Tab.Screen>
      <Tab.Screen name="Reports">{() => <PlaceholderScreen title="Reports" />}</Tab.Screen>
      <Tab.Screen name="Profile">{() => <PlaceholderScreen title="Profile" />}</Tab.Screen>
    </Tab.Navigator>
  );
}
