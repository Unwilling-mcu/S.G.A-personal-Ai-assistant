import React from "react";

function DashboardPanel({ title, children }) {
  return (
    <div style={styles.panel}>
      <h3 style={styles.title}>{title}</h3>
      <div style={styles.content}>{children}</div>
    </div>
  );
}

const styles = {
  panel: {
    border: "1px solid #00ffe1",
    padding: "14px",
    borderRadius: "10px",
    boxShadow: "0 0 15px rgba(0,255,225,0.2)",
    background: "rgba(0, 255, 225, 0.03)",
    backdropFilter: "blur(5px)",
    fontFamily: "'Courier New', monospace",
  },
  title: {
    margin: "0 0 10px 0",
    borderBottom: "1px solid rgba(0,255,225,0.3)",
    paddingBottom: "8px",
    fontSize: "13px",
    letterSpacing: "2px",
  },
  content: {
    fontSize: "13px",
    lineHeight: "1.8",
    color: "rgba(0,255,225,0.85)",
  },
};

export default DashboardPanel;