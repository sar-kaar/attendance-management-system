import { StyleSheet, Text, View } from 'react-native';

// Phase 15 foundation shell — real screen content lands in the phase that owns
// each feature (see docs/phases.md Phases 16-21).
export default function PlaceholderScreen({ title }: { title: string }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.subtitle}>Coming soon</Text>
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
  },
  subtitle: {
    marginTop: 4,
    color: '#666',
  },
});
