import React, { useEffect, useState, useRef, useCallback } from "react";
import JarvisCore from "./JarvisCore";
import Waveform from "./Waveform";
import DashboardPanel from "./DashboardPanel";
import IntelligencePanel from "./IntelligencePanel";
import MemoryPanel from "./MemoryPanel";
import TaskPanel from "./TaskPanel";
import VoiceOrb from "./VoiceOrb";
import TitleBar from "./TitleBar";
import CodeBlock from "./CodeBlock";
import GestureOverlay from "./GestureOverlay";

const WS_URL = "ws://127.0.0.1:8000/ws";
const RECONNECT_DELAY_MS = 3000;

function deriveOrbState(wsState, thinking, speaking) {
  if (wsState !== "Connected") return "idle";
  if (thinking) return "thinking";
  if (speaking) return "speaking";
  return "listening";
}

function App() {
  const [messages,      setMessages]      = useState([]);
  const [status,        setStatus]        = useState("Disconnected");
  const [thinking,      setThinking]      = useState(false);
  const [thinkingStep,  setThinkingStep]  = useState("");
  const [thinkingSteps, setThinkingSteps] = useState([]);
  const [speaking,      setSpeaking]      = useState(false);
  const [lastWords,     setLastWords]     = useState("");
  const [lastGesture,   setLastGesture]   = useState("");
  const [gestureActive, setGestureActive] = useState(false);
  const [intent,        setIntent]        = useState("");
  const [actions,       setActions]       = useState([]);
  const [parsedText,    setParsedText]    = useState("");
  const [uptime,        setUptime]        = useState(0);
  const [activeTab,     setActiveTab]     = useState("chat"); // chat | tasks

  const wsRef          = useRef(null);
  const reconnectTimer = useRef(null);
  const chatEndRef     = useRef(null);
  const speakTimer     = useRef(null);

  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);
  useEffect(() => {
    const t = setInterval(() => setUptime(u => u + 1), 1000);
    return () => clearInterval(t);
  }, []);

  const formatUptime = s => {
    const h = String(Math.floor(s/3600)).padStart(2,"0");
    const m = String(Math.floor((s%3600)/60)).padStart(2,"0");
    const sec = String(s%60).padStart(2,"0");
    return `${h}:${m}:${sec}`;
  };

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;
    ws.onopen  = () => { setStatus("Connected"); clearTimeout(reconnectTimer.current); };
    ws.onerror = () => setStatus("Error");
    ws.onclose = () => {
      setStatus("Reconnecting...");
      reconnectTimer.current = setTimeout(connect, RECONNECT_DELAY_MS);
    };
    ws.onmessage = (event) => {
      let data;
      try { data = JSON.parse(event.data); } catch { return; }
      if (data.type === "keepalive") return;
      if (data.type === "thinking") {
        setThinking(true); setSpeaking(false);
        setThinkingStep(data.step || "");
        setThinkingSteps(prev => [...prev, data.step]);
        return;
      }
      if (data.type === "response") {
        setThinking(false); setThinkingSteps([]);
        setSpeaking(true); setLastWords(data.ai || "");
        clearTimeout(speakTimer.current);
        const wc = (data.ai||"").split(" ").length;
        speakTimer.current = setTimeout(() => setSpeaking(false), Math.max(2500, wc*350));
        setMessages(prev => [...prev,
          { type:"user", text: data.user||"" },
          { type:"ai",   text: data.ai||""   },
        ]);
        setIntent(data.intent||"");
        setActions(data.actions||[]);
        setParsedText(data.parsed_text||"");
        // Auto-switch to tasks tab if task-related
        if (data.intent === "task" || (data.ai||"").includes("Task") || (data.ai||"").includes("Pending")) {
          setActiveTab("tasks");
        }
      }
      if (data.type === "status") setStatus(data.message||"Unknown");
      if (data.type === "gesture") {
        setLastGesture(data.gesture || "");
        setGestureActive(true);
        setTimeout(() => setGestureActive(false), 1500);
      }
    };
  }, []);

  useEffect(() => {
    connect();
    return () => { clearTimeout(reconnectTimer.current); wsRef.current?.close(); };
  }, [connect]);

  const statusColor =
    status === "Connected"         ? "#00ffe1" :
    status.startsWith("Reconnect") ? "#ffaa00" : "#ff4444";
  const orbState = deriveOrbState(status, thinking, speaking);

  return (
    <div style={styles.container}>
      <TitleBar />
      <h1 style={styles.title}>⚡ S . G . A</h1>

      <div style={styles.grid}>
        {/* Left */}
        <DashboardPanel title="🧠 SYSTEM STATUS">
          <p>Status: <span style={{ color: statusColor, fontWeight:"bold" }}>{status}</span></p>
          <p>Uptime: {formatUptime(uptime)}</p>
          <p>Mode: {orbState.toUpperCase()}</p>
          <p>Exchanges: {Math.floor(messages.length/2)}</p>
        </DashboardPanel>

        {/* Centre */}
        <div style={styles.centreCol}>
          <JarvisCore thinking={thinking} />
          <Waveform active={thinking||speaking} />
          {thinking && (
            <div style={styles.thinkingBox}>
              {thinkingSteps.map((step, i) => (
                <p key={i} style={styles.thinkingStep}>→ {step}</p>
              ))}
            </div>
          )}
        </div>

        {/* Right */}
        <IntelligencePanel intent={intent} actions={actions} text={parsedText} />
      </div>

      {/* Tab bar */}
      <div style={styles.tabBar}>
        {["chat","tasks","memory"].map(tab => (
          <button key={tab} style={{
            ...styles.tab,
            ...(activeTab===tab ? styles.tabActive : {})
          }} onClick={() => setActiveTab(tab)}>
            {tab === "chat" ? "💬 CHAT" : tab === "tasks" ? "✅ TASKS" : "🗂 MEMORY"}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "chat" && (
        <div style={styles.chatBox}>
          {messages.map((msg, i) => (
            <div key={i} style={{
              ...styles.bubble,
              ...(msg.type==="user" ? styles.userBubble : styles.aiBubble),
            }}>
              <span style={styles.bubbleLabel}>{msg.type==="user" ? "YOU" : "S.G.A"}</span>
              {msg.type === "ai" ? <CodeBlock text={msg.text} /> : <p style={styles.bubbleText}>{msg.text}</p>}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
      )}

      {activeTab === "tasks" && (
        <div style={{ marginTop: 16 }}>
          <TaskPanel messages={messages} />
        </div>
      )}

      {activeTab === "memory" && (
        <div style={{ marginTop: 16 }}>
          <MemoryPanel messages={messages} />
        </div>
      )}

      <GestureOverlay lastGesture={lastGesture} gestureActive={gestureActive} />
      <VoiceOrb state={orbState} thinkingStep={thinkingStep} lastWords={lastWords} />
    </div>
  );
}

const styles = {
  container: {
    background: "#02040a", color: "#00ffe1", minHeight: "100vh",
    padding: 20, paddingTop: 52,
    fontFamily: "'Courier New', monospace", boxSizing: "border-box",
  },
  title: {
    textAlign: "center", textShadow: "0 0 25px #00ffe1",
    letterSpacing: 8, marginBottom: 20,
  },
  grid: {
    display: "grid", gridTemplateColumns: "1fr 1fr 1fr",
    gap: 20, alignItems: "start",
  },
  centreCol: { display:"flex", flexDirection:"column", alignItems:"center" },
  thinkingBox: {
    marginTop: 12, width:"100%",
    background:"rgba(255,170,0,0.05)", border:"1px solid #ffaa00",
    borderRadius: 8, padding: 10,
  },
  thinkingStep: { color:"#ffaa00", fontSize:13, margin:"4px 0" },
  tabBar: {
    display:"flex", gap:8, marginTop:20,
    borderBottom: "1px solid rgba(0,255,225,0.2)", paddingBottom: 8,
  },
  tab: {
    background:"transparent", border:"1px solid rgba(0,255,225,0.2)",
    color:"rgba(0,255,225,0.5)", padding:"6px 18px", borderRadius:6,
    cursor:"pointer", fontFamily:"'Courier New', monospace",
    fontSize:11, letterSpacing:2, transition:"all 0.2s",
  },
  tabActive: {
    background:"rgba(0,255,225,0.1)", border:"1px solid #00ffe1",
    color:"#00ffe1",
  },
  chatBox: {
    marginTop: 12, height:"30vh", overflowY:"auto",
    border:"1px solid #00ffe1", borderRadius:8, padding:12,
    background:"rgba(0,255,225,0.02)", paddingBottom:80,
  },
  bubble: { padding:"10px 14px", marginBottom:10, borderRadius:10, maxWidth:"70%" },
  userBubble: {
    background:"rgba(0,255,225,0.15)", border:"1px solid #00ffe1", marginLeft:"auto",
  },
  aiBubble: {
    background:"rgba(0,255,225,0.04)", border:"1px solid rgba(0,255,225,0.3)",
  },
  bubbleLabel: { fontSize:10, opacity:0.5, letterSpacing:2, display:"block", marginBottom:4 },
  bubbleText: { margin:0, fontSize:14, lineHeight:1.5 },
};

export default App;