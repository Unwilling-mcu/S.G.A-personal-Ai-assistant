import React, { useState } from "react";

function TaskPanel({ messages }) {
  const [filter, setFilter] = useState("all");

  // Extract task-related AI responses from messages
  const taskMessages = messages.filter(m =>
    m.type === "ai" && (
      m.text.includes("Task added") ||
      m.text.includes("Pending:") ||
      m.text.includes("marked as done") ||
      m.text.includes("Task deleted") ||
      m.text.includes("no tasks")
    )
  );

  const lastTaskMsg = taskMessages[taskMessages.length - 1];

  // Parse pending tasks from "Pending: 1. task; 2. task"
  const parseTasks = (text) => {
    if (!text) return { pending: [], done: [] };
    const pendingMatch = text.match(/Pending:\s*(.+?)(?:\s*Done:|$)/s);
    const doneMatch    = text.match(/Done:\s*(.+?)$/s);
    const pending = pendingMatch
      ? pendingMatch[1].split(";").map(t => t.trim()).filter(Boolean)
      : [];
    const done = doneMatch
      ? doneMatch[1].split(";").map(t => t.trim()).filter(Boolean)
      : [];
    return { pending, done };
  };

  const { pending, done } = parseTasks(lastTaskMsg?.text || "");

  return (
    <div style={styles.panel}>
      <h3 style={styles.heading}>✅ TASK LIST</h3>

      {pending.length === 0 && done.length === 0 ? (
        <p style={styles.empty}>Say "add task [name]" or "my tasks"</p>
      ) : (
        <>
          {pending.length > 0 && (
            <div>
              <p style={styles.sectionLabel}>PENDING</p>
              {pending.map((t, i) => (
                <div key={i} style={styles.task}>
                  <span style={styles.bullet}>○</span>
                  <span style={styles.taskText}>{t.replace(/^\d+\.\s*/, "")}</span>
                </div>
              ))}
            </div>
          )}
          {done.length > 0 && (
            <div>
              <p style={{ ...styles.sectionLabel, color: "rgba(0,255,225,0.3)" }}>DONE</p>
              {done.map((t, i) => (
                <div key={i} style={styles.task}>
                  <span style={{ ...styles.bullet, color: "rgba(0,255,225,0.3)" }}>✓</span>
                  <span style={{ ...styles.taskText, opacity: 0.4, textDecoration: "line-through" }}>{t}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      <div style={styles.hint}>
        <span>Say: "add task buy milk" • "complete task 1" • "my tasks"</span>
      </div>
    </div>
  );
}

const styles = {
  panel: {
    border: "1px solid #00ffe1", borderRadius: 10,
    padding: "12px 16px", background: "rgba(0,255,225,0.03)",
    boxShadow: "0 0 15px rgba(0,255,225,0.1)",
    fontFamily: "'Courier New', monospace",
  },
  heading: {
    margin: "0 0 10px 0", borderBottom: "1px solid rgba(0,255,225,0.3)",
    paddingBottom: 8, fontSize: 13, letterSpacing: 2,
  },
  sectionLabel: {
    fontSize: 9, letterSpacing: 2, color: "rgba(0,255,225,0.4)",
    margin: "8px 0 4px 0",
  },
  task: {
    display: "flex", alignItems: "flex-start", gap: 8,
    marginBottom: 6,
  },
  bullet: { color: "#00ffe1", fontSize: 12, marginTop: 2, minWidth: 12 },
  taskText: { fontSize: 12, color: "#00ffe1", flex: 1, lineHeight: 1.4 },
  empty: { color: "rgba(0,255,225,0.3)", fontSize: 12, fontStyle: "italic" },
  hint: {
    marginTop: 10, paddingTop: 8,
    borderTop: "1px solid rgba(0,255,225,0.1)",
    fontSize: 10, color: "rgba(0,255,225,0.3)", lineHeight: 1.6,
  },
};

export default TaskPanel;
