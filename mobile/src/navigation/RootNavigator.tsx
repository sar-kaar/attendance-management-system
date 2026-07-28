import { ActivityIndicator, View } from 'react-native';
import { useAuth } from '../context/AuthContext';
import AuthNavigator from './AuthNavigator';
import StudentNavigator from './StudentNavigator';
import FacultyNavigator from './FacultyNavigator';
import PlaceholderScreen from '../screens/PlaceholderScreen';

// admin is web-only for v1 — see docs/mobile-requirements.md Target Roles & Platforms.
export default function RootNavigator() {
  const { loading, isAuthenticated, user } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <ActivityIndicator />
      </View>
    );
  }

  if (!isAuthenticated) {
    return <AuthNavigator />;
  }

  if (user?.role === 'faculty') {
    return <FacultyNavigator />;
  }

  if (user?.role === 'student') {
    return <StudentNavigator />;
  }

  return <PlaceholderScreen title="This role isn't supported on mobile yet" />;
}
