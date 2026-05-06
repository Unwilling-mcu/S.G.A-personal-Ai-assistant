import React, { useEffect, useRef } from "react";

function Waveform({ active }) {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const frameRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const BAR_COUNT = 32;
    const W = canvas.width;
    const H = canvas.height;
    const barW = W / BAR_COUNT - 2;

    const draw = () => {
      frameRef.current++;
      ctx.clearRect(0, 0, W, H);

      for (let i = 0; i < BAR_COUNT; i++) {
        let height;
        if (active) {
          // Animated bars when active/thinking
          height =
            Math.abs(Math.sin((frameRef.current * 0.08) + i * 0.4)) * (H * 0.7) +
            Math.abs(Math.sin((frameRef.current * 0.05) + i * 0.7)) * (H * 0.2) +
            4;
        } else {
          // Gentle idle pulse
          height = Math.abs(Math.sin(i * 0.3)) * (H * 0.2) + 4;
        }

        const x = i * (barW + 2);
        const y = (H - height) / 2;

        const alpha = active ? 0.8 : 0.3;
        ctx.fillStyle = `rgba(0, 255, 225, ${alpha})`;
        ctx.beginPath();
        ctx.roundRect(x, y, barW, height, 2);
        ctx.fill();
      }

      animRef.current = requestAnimationFrame(draw);
    };

    draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [active]);

  return (
    <canvas
      ref={canvasRef}
      width={220}
      height={50}
      style={styles.canvas}
    />
  );
}

const styles = {
  canvas: {
    display: "block",
    margin: "10px auto 0",
  },
};

export default Waveform;