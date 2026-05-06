import React, { useState } from "react";

/**
 * CodeBlock — renders markdown-style code blocks from AI responses.
 * Detects ```language ... ``` fences and renders them with syntax highlighting styling.
 */
function CodeBlock({ text }) {
  if (!text) return null;

  // Split on code fences
  const parts = text.split(/(```[\w]*\n[\s\S]*?```)/g);

  return (
    <div style={styles.wrapper}>
      {parts.map((part, i) => {
        const fenceMatch = part.match(/```([\w]*)\n([\s\S]*?)```/);
        if (fenceMatch) {
          const lang = fenceMatch[1] || "code";
          const code = fenceMatch[2];
          return <CodeFence key={i} lang={lang} code={code} />;
        }
        // Plain text — render with line breaks
        return (
          <span key={i} style={styles.text}>
            {part.split("\n").map((line, j) => (
              <span key={j}>{line}<br /></span>
            ))}
          </span>
        );
      })}
    </div>
  );
}

function CodeFence({ lang, code }) {
  const [copied, setCopied] = useState(false);

  const copy = () => {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div style={styles.fence}>
      <div style={styles.fenceHeader}>
        <span style={styles.langLabel}>{lang.toUpperCase()}</span>
        <button style={styles.copyBtn} onClick={copy}>
          {copied ? "✓ Copied" : "Copy"}
        </button>
      </div>
      <pre style={styles.pre}>
        <code style={styles.code}>{code}</code>
      </pre>
    </div>
  );
}

const styles = {
  wrapper: {
    fontSize: 13,
    lineHeight: 1.6,
    color: "#00ffe1",
    fontFamily: "'Courier New', monospace",
  },
  text: {
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
  },
  fence: {
    margin: "10px 0",
    borderRadius: 8,
    overflow: "hidden",
    border: "1px solid rgba(0,255,225,0.3)",
    background: "rgba(0,0,0,0.4)",
  },
  fenceHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "4px 12px",
    background: "rgba(0,255,225,0.08)",
    borderBottom: "1px solid rgba(0,255,225,0.15)",
  },
  langLabel: {
    fontSize: 10,
    letterSpacing: 2,
    color: "rgba(0,255,225,0.6)",
  },
  copyBtn: {
    background: "transparent",
    border: "1px solid rgba(0,255,225,0.3)",
    color: "#00ffe1",
    fontSize: 11,
    padding: "2px 10px",
    borderRadius: 4,
    cursor: "pointer",
    fontFamily: "'Courier New', monospace",
  },
  pre: {
    margin: 0,
    padding: "12px 16px",
    overflowX: "auto",
  },
  code: {
    fontSize: 12,
    color: "#a8ff78",
    fontFamily: "'Courier New', monospace",
    whiteSpace: "pre",
  },
};

export default CodeBlock;