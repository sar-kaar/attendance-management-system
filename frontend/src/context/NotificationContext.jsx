import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { FaCheckCircle, FaExclamationCircle, FaInfoCircle, FaTimes } from "react-icons/fa";
import "../styles/notifications.css";

const NotificationContext = createContext(null);

const AUTO_DISMISS = { success: 3500, info: 4000, error: 6000 };

const ICONS = {
  success: <FaCheckCircle />,
  error: <FaExclamationCircle />,
  info: <FaInfoCircle />,
};

/**
 * Turn a DRF error payload into something a human can read.
 *
 * The pages used to `alert(JSON.stringify(err.response.data))`, which put raw
 * JSON in front of the user. DRF returns either {field: [msg, ...]} or
 * {detail: msg}, so flatten both into plain sentences.
 */
export function formatApiError(err, fallback = "Something went wrong.") {
  const data = err?.response?.data;
  if (!data) return err?.message || fallback;
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;
  if (data.error) return data.error;

  const parts = Object.entries(data).map(([field, val]) => {
    const text = Array.isArray(val) ? val.join(", ") : String(val);
    // non_field_errors has no useful label to show.
    return field === "non_field_errors" ? text : `${field.replace(/_/g, " ")}: ${text}`;
  });
  return parts.length ? parts.join("\n") : fallback;
}

export function NotificationProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const [dialog, setDialog] = useState(null);
  const nextId = useRef(1);
  const timers = useRef(new Map());
  const confirmBtn = useRef(null);
  const lastFocused = useRef(null);

  const dismiss = useCallback((id) => {
    setToasts((list) => list.filter((t) => t.id !== id));
    const timer = timers.current.get(id);
    if (timer) {
      clearTimeout(timer);
      timers.current.delete(id);
    }
  }, []);

  const notify = useCallback(
    (message, type = "info") => {
      if (!message) return undefined;
      const id = nextId.current++;
      setToasts((list) => [...list, { id, message: String(message), type }]);
      const timer = setTimeout(() => dismiss(id), AUTO_DISMISS[type] ?? 4000);
      timers.current.set(id, timer);
      return id;
    },
    [dismiss]
  );

  // Clear pending timers on unmount so they cannot fire into a dead tree.
  useEffect(() => {
    const pending = timers.current;
    return () => pending.forEach(clearTimeout);
  }, []);

  /**
   * Promise-based replacement for window.confirm.
   * `await confirm({...})` resolves true/false, so call sites keep reading
   * top-to-bottom instead of splintering into callbacks.
   */
  const confirm = useCallback(
    ({ title = "Are you sure?", message = "", confirmText = "Confirm", danger = false } = {}) =>
      new Promise((resolve) => {
        lastFocused.current = document.activeElement;
        setDialog({ title, message, confirmText, danger, resolve });
      }),
    []
  );

  const closeDialog = useCallback(
    (result) => {
      setDialog((current) => {
        current?.resolve(result);
        return null;
      });
      // Return focus to whatever opened the dialog, or the keyboard user is
      // dumped back at the top of the document.
      if (lastFocused.current?.focus) lastFocused.current.focus();
    },
    []
  );

  useEffect(() => {
    if (!dialog) return undefined;
    confirmBtn.current?.focus();
    const onKey = (e) => {
      if (e.key === "Escape") closeDialog(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [dialog, closeDialog]);

  return (
    <NotificationContext.Provider value={{ notify, confirm }}>
      {children}

      {/* aria-live so a screen reader announces toasts without stealing focus. */}
      <div className="toast-host" role="region" aria-live="polite" aria-label="Notifications">
        {toasts.map((t) => (
          <div key={t.id} className={`toast toast-${t.type}`} role="alert">
            <span className="toast-icon">{ICONS[t.type] ?? ICONS.info}</span>
            <span className="toast-msg">{t.message}</span>
            <button
              type="button"
              className="toast-close"
              onClick={() => dismiss(t.id)}
              aria-label="Dismiss notification"
            >
              <FaTimes />
            </button>
          </div>
        ))}
      </div>

      {dialog && (
        <div className="dialog-backdrop" onClick={() => closeDialog(false)}>
          <div
            className="dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="dialog-title"
            /* The backdrop closes on click; without this a click inside the
               panel would bubble up and dismiss it too. */
            onClick={(e) => e.stopPropagation()}
          >
            <h3 id="dialog-title">{dialog.title}</h3>
            {dialog.message && <p>{dialog.message}</p>}
            <div className="dialog-actions">
              <button type="button" className="btn-ghost" onClick={() => closeDialog(false)}>
                Cancel
              </button>
              <button
                type="button"
                ref={confirmBtn}
                className={dialog.danger ? "btn-danger" : "btn-primary"}
                onClick={() => closeDialog(true)}
              >
                {dialog.confirmText}
              </button>
            </div>
          </div>
        </div>
      )}
    </NotificationContext.Provider>
  );
}

export function useNotify() {
  const ctx = useContext(NotificationContext);
  if (!ctx) throw new Error("useNotify must be used inside NotificationProvider");
  return ctx;
}
