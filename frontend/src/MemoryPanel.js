import React from "react";
import CodeBlock from "./CodeBlock";

function MemoryPanel({ messages }) {
  const pairs = [];
  for (let i = 0; i < messages.length - 1; i += 2) {
    const user = messages[i];
    const ai   = messages[i + 1];
    if (user && ai) pairs.push({ user: user.text, ai: ai.text, id: i });
  }
  const recent = pairs.slice(-5).reverse();

  return (
    <div style={styles.panel}>
      <h3 style={styles.heading}>🗂 MEMORY LOG</h3>
      {recent.length === 0 ? (
        <p style={styles.empty}>No interactions yet...</p>
      ) : (
        recent.map((pair) => (
          <div key={pair.id} style={styles.entry}>
            <div style={styles.row}>
              <span style={styles.label}>YOU</span>
              <span style={styles.userText}>{pair.user}</span>
            </div>
            <div style={styles.row}>
              <span style={styles.label}>AI </span>
              <div style={{ flex: 1 }}>
                <CodeBlock text={pair.ai} />
              </div>
            </div>
            <hr style={styles.divider} />
          </div>
        ))
      )}
    </div>
  );
}

const styles = {
  panel: {
    border: "1px solid #00ffe1", borderRadius: "10px",
    padding: "12px 16px", background: "rgba(0,255,225,0.03)",
    boxShadow: "0 0 15px rgba(0,255,225,0.15)",
    fontFamily: "'Courier New', monospace",
  },
  heading: {
    margin: "0 0 12px 0", borderBottom: "1px solid rgba(0,255,225,0.3)",
    paddingBottom: "8px", fontSize: "14px", letterSpacing: "2px",
  },
  empty: { color: "rgba(0,255,225,0.4)", fontSize: "13px", fontStyle: "italic" },
  entry: { marginBottom: "8px" },
  row: { display: "flex", gap: "10px", marginBottom: "3px", alignItems: "flex-start" },
  label: {
    fontSize: "10px", color: "rgba(0,255,225,0.5)", letterSpacing: "1px",
    minWidth: "28px", paddingTop: "2px",
  },
  userText: { fontSize: "13px", color: "#00ffe1", flex: 1 },
  divider: { border: "none", borderTop: "1px solid rgba(0,255,225,0.1)", margin: "8px 0 0 0" },
};

export default MemoryPanel;