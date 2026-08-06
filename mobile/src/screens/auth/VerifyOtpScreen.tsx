import { useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
} from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { otpAPI } from '../../services/api';
import type { AuthStackParamList } from '../../navigation/AuthNavigator';

type Props = NativeStackScreenProps<AuthStackParamList, 'VerifyOtp'>;

const RESEND_COOLDOWN = 60;

function readError(err: unknown, fallback: string): string {
  const data = (err as { response?: { data?: { error?: string; detail?: string } } })?.response
    ?.data;
  return data?.error || data?.detail || fallback;
}

export default function VerifyOtpScreen({ navigation, route }: Props) {
  const { email } = route.params;
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState(
    `We sent a 6-digit code to ${email}. It expires in 10 minutes.`,
  );
  const [submitting, setSubmitting] = useState(false);
  const [secondsLeft, setSecondsLeft] = useState(RESEND_COOLDOWN);
  const isMounted = useRef(true);

  useEffect(() => {
    return () => {
      isMounted.current = false;
    };
  }, []);

  useEffect(() => {
    if (secondsLeft <= 0) return undefined;
    const t = setTimeout(() => setSecondsLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
  }, [secondsLeft]);

  const handleVerify = async () => {
    setError('');
    setNotice('');
    setSubmitting(true);
    try {
      await otpAPI.verify(email, code);
      navigation.replace('Login', { message: 'Email verified. You can sign in now.' });
    } catch (err) {
      if (isMounted.current) setError(readError(err, 'Verification failed. Please try again.'));
    } finally {
      if (isMounted.current) setSubmitting(false);
    }
  };

  const handleResend = async () => {
    setError('');
    setNotice('');
    try {
      await otpAPI.send(email);
      setNotice('A new code is on its way.');
      setSecondsLeft(RESEND_COOLDOWN);
    } catch (err) {
      const status = (err as { response?: { status?: number } })?.response?.status;
      setError(readError(err, 'Could not resend the code.'));
      if (status === 429) setSecondsLeft(RESEND_COOLDOWN);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <Text style={styles.title}>Verify your email</Text>
      <Text style={styles.subtitle}>{email}</Text>

      {notice ? <Text style={styles.notice}>{notice}</Text> : null}
      {error ? <Text style={styles.error}>{error}</Text> : null}

      <TextInput
        style={styles.input}
        placeholder="6-digit code"
        keyboardType="number-pad"
        autoComplete="one-time-code"
        value={code}
        onChangeText={(v) => setCode(v.replace(/\D/g, '').slice(0, 6))}
        maxLength={6}
        autoFocus
      />

      <Pressable
        style={[styles.button, (submitting || code.length !== 6) && styles.buttonDisabled]}
        onPress={handleVerify}
        disabled={submitting || code.length !== 6}
      >
        {submitting ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Verify Email</Text>
        )}
      </Pressable>

      <Pressable style={styles.linkButton} onPress={handleResend} disabled={secondsLeft > 0}>
        <Text style={[styles.linkText, secondsLeft > 0 && styles.linkTextDisabled]}>
          {secondsLeft > 0 ? `Resend code in ${secondsLeft}s` : 'Resend code'}
        </Text>
      </Pressable>
      <Pressable style={styles.linkButton} onPress={() => navigation.navigate('Login', {})}>
        <Text style={styles.linkText}>Back to login</Text>
      </Pressable>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  title: {
    fontSize: 20,
    fontWeight: '600',
    textAlign: 'center',
  },
  subtitle: {
    marginTop: 4,
    marginBottom: 24,
    color: '#666',
    textAlign: 'center',
  },
  notice: {
    color: '#1d4ed8',
    backgroundColor: '#eff6ff',
    padding: 10,
    borderRadius: 8,
    marginBottom: 12,
    textAlign: 'center',
  },
  error: {
    color: '#b91c1c',
    backgroundColor: '#fef2f2',
    padding: 10,
    borderRadius: 8,
    marginBottom: 12,
    textAlign: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    paddingHorizontal: 14,
    paddingVertical: 12,
    marginBottom: 12,
    fontSize: 16,
    textAlign: 'center',
    letterSpacing: 4,
  },
  button: {
    backgroundColor: '#1a237e',
    borderRadius: 8,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  linkButton: {
    marginTop: 16,
    alignItems: 'center',
  },
  linkText: {
    color: '#1a237e',
  },
  linkTextDisabled: {
    color: '#999',
  },
});
