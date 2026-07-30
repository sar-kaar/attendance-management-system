import { StyleSheet, Text, View } from 'react-native';

// Placeholder boot shell for the unauthenticated stack.
// Real login form + API wiring lands in Phase 16 (Mobile Authentication).
export default function LoginScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Attendance Management System</Text>
      <Text style={styles.subtitle}>Login coming soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: '600',
    textAlign: 'center',
    paddingHorizontal: 24,
  },
  subtitle: {
    marginTop: 4,
    color: '#666',
  },
});
