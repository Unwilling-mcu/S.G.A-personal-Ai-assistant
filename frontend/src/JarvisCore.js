import React from "react";
import { motion } from "framer-motion";

function JarvisCore({ thinking }) {
  return (
    <div style={styles.container}>
      {/* Outer glow ring */}
      <motion.div
        animate={{
          scale: thinking ? [1, 1.15, 1] : [1, 1.03, 1],
          opacity: thinking ? [0.5, 1, 0.5] : [0.4, 0.6, 0.4],
          boxShadow: thinking
            ? ["0 0 30px #00ffe1", "0 0 60px #00ffe1", "0 0 30px #00ffe1"]
            : ["0 0 15px #00ffe1", "0 0 25px #00ffe1", "0 0 15px #00ffe1"],
        }}
        transition={{ repeat: Infinity, duration: thinking ? 1.2 : 3, ease: "easeInOut" }}
        style={styles.outerRing}
      />

      {/* Middle ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: thinking ? 4 : 10, ease: "linear" }}
        style={styles.middleRing}
      />

      {/* Inner core */}
      <motion.div
        animate={{
          scale: thinking ? [1, 1.12, 1] : [1, 1.05, 1],
          background: thinking
            ? ["#00ffe1", "#00ccff", "#00ffe1"]
            : ["#00ffe1", "#00e6cc", "#00ffe1"],
        }}
        transition={{ repeat: Infinity, duration: thinking ? 0.8 : 2, ease: "easeInOut" }}
        style={styles.core}
      />

      <p style={styles.label}>S . G . A</p>
    </div>
  );
}

const styles = {
  container: {
    position: "relative",
    width: "200px",
    height: "200px",
    margin: "20px auto",
  },
  outerRing: {
    position: "absolute",
    inset: 0,
    borderRadius: "50%",
    border: "2px solid #00ffe1",
  },
  middleRing: {
    position: "absolute",
    inset: "20px",
    borderRadius: "50%",
    border: "1px dashed rgba(0,255,225,0.4)",
  },
  core: {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: "80px",
    height: "80px",
    borderRadius: "50%",
    boxShadow: "0 0 40px #00ffe1",
  },
  label: {
    position: "absolute",
    bottom: "-28px",
    width: "100%",
    textAlign: "center",
    color: "#00ffe1",
    letterSpacing: "6px",
    fontSize: "12px",
    margin: 0,
  },
};

export default JarvisCore;