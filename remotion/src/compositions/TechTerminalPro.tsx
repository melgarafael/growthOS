import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
  Sequence,
} from "remotion";
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "500", "600", "700", "800", "900"],
  subsets: ["latin"],
});

// ── Design Tokens ──────────────────────────────
const T = {
  bg: "#050510",
  surface: "#0c0c1d",
  surfaceLight: "#141432",
  border: "#1e1e3f",
  text: "#f0f0ff",
  textMuted: "#7878a0",
  primary: "#6c5ce7",
  primaryGlow: "#8b7cf7",
  secondary: "#00cec9",
  accent: "#fd79a8",
  success: "#00e676",
  termGreen: "#4ade80",
  termCyan: "#22d3ee",
  termYellow: "#fbbf24",
  termRed: "#f87171",
};

// ── Animated Gradient Background ───────────────
const CinematicBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const hueShift = interpolate(frame, [0, durationInFrames], [0, 30]);
  const orbX = interpolate(frame, [0, durationInFrames], [20, 80], {
    easing: Easing.inOut(Easing.sin),
  });
  const orbY = interpolate(frame, [0, durationInFrames], [30, 70], {
    easing: Easing.inOut(Easing.sin),
  });
  const orb2X = interpolate(frame, [0, durationInFrames], [70, 30], {
    easing: Easing.inOut(Easing.sin),
  });

  return (
    <AbsoluteFill>
      {/* Base */}
      <div style={{ position: "absolute", inset: 0, background: T.bg }} />

      {/* Orb 1 — primary glow */}
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${T.primary}30 0%, transparent 70%)`,
          left: `${orbX}%`,
          top: `${orbY}%`,
          transform: "translate(-50%, -50%)",
          filter: "blur(80px)",
        }}
      />

      {/* Orb 2 — accent glow */}
      <div
        style={{
          position: "absolute",
          width: 400,
          height: 400,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${T.accent}20 0%, transparent 70%)`,
          left: `${orb2X}%`,
          top: "60%",
          transform: "translate(-50%, -50%)",
          filter: "blur(60px)",
        }}
      />

      {/* Grid overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(${T.border}15 1px, transparent 1px),
            linear-gradient(90deg, ${T.border}15 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
          opacity: interpolate(frame, [0, 30], [0, 0.4], { extrapolateRight: "clamp" }),
        }}
      />

      {/* Vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(ellipse at center, transparent 40%, ${T.bg} 100%)`,
        }}
      />

      {/* Noise/grain */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.03,
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
        }}
      />
    </AbsoluteFill>
  );
};

// ── Kinetic Text — word-by-word reveal ─────────
const KineticText: React.FC<{
  text: string;
  fontSize: number;
  color?: string;
  fontWeight?: number;
  delay?: number;
  staggerFrames?: number;
  highlightWord?: string;
  highlightColor?: string;
  lineHeight?: number;
}> = ({
  text,
  fontSize,
  color = T.text,
  fontWeight = 800,
  delay = 0,
  staggerFrames = 4,
  highlightWord,
  highlightColor = T.accent,
  lineHeight = 1.15,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: fontSize * 0.25,
        fontFamily,
        fontSize,
        fontWeight,
        lineHeight,
        maxWidth: "90%",
      }}
    >
      {words.map((word, i) => {
        const wordDelay = delay + i * staggerFrames;
        const progress = spring({
          frame: frame - wordDelay,
          fps,
          config: { damping: 15, stiffness: 200 },
        });

        const isHighlight = highlightWord && word.toLowerCase().includes(highlightWord.toLowerCase());
        const wordColor = isHighlight ? highlightColor : color;

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              opacity: interpolate(progress, [0, 0.5], [0, 1], { extrapolateRight: "clamp" }),
              transform: `translateY(${interpolate(progress, [0, 1], [20, 0])}px)`,
              color: wordColor,
              textShadow: isHighlight
                ? `0 0 30px ${highlightColor}60, 0 0 60px ${highlightColor}30`
                : "none",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

// ── Glow Line Divider ──────────────────────────
const GlowLine: React.FC<{ color?: string; delay?: number; width?: string }> = ({
  color = T.primary,
  delay = 0,
  width = "60%",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const drawProgress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 200 },
    durationInFrames: 30,
  });

  return (
    <div
      style={{
        width,
        height: 2,
        margin: "0 auto",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          width: `${drawProgress * 100}%`,
          height: "100%",
          background: `linear-gradient(90deg, transparent, ${color}, transparent)`,
          boxShadow: `0 0 15px ${color}60, 0 0 30px ${color}30`,
        }}
      />
    </div>
  );
};

// ── Pro Terminal Window ─────────────────────────
const SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];

interface TermLine {
  text: string;
  type: "input" | "output" | "spinner" | "success" | "error" | "blank";
  color?: string;
  delay?: number;
  typeSpeed?: number;
}

const ProTerminal: React.FC<{
  lines: TermLine[];
  title?: string;
}> = ({ lines, title = "Claude Code — GrowthOS" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance animation
  const entrance = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 120 },
  });
  const termScale = interpolate(entrance, [0, 1], [0.92, 1]);
  const termOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  // Build timeline
  let cursor = 8;
  const timeline: Array<TermLine & { start: number; end: number }> = [];
  for (const line of lines) {
    cursor += line.delay ?? 6;
    let dur: number;
    if (line.type === "input") dur = line.text.length * (line.typeSpeed ?? 2);
    else if (line.type === "spinner") dur = 50;
    else if (line.type === "blank") dur = 1;
    else dur = 3;
    timeline.push({ ...line, start: cursor, end: cursor + dur });
    cursor += dur;
  }

  return (
    <div
      style={{
        width: "88%",
        margin: "0 auto",
        transform: `scale(${termScale})`,
        opacity: termOpacity,
      }}
    >
      <div
        style={{
          background: `linear-gradient(145deg, ${T.surface}, ${T.bg})`,
          borderRadius: 16,
          overflow: "hidden",
          border: `1px solid ${T.border}`,
          boxShadow: `
            0 4px 6px rgba(0,0,0,0.3),
            0 12px 40px rgba(0,0,0,0.5),
            inset 0 1px 0 ${T.surfaceLight}40
          `,
        }}
      >
        {/* Title bar */}
        <div
          style={{
            padding: "12px 18px",
            display: "flex",
            alignItems: "center",
            gap: 8,
            borderBottom: `1px solid ${T.border}`,
            background: `linear-gradient(180deg, ${T.surfaceLight}80, ${T.surface})`,
          }}
        >
          <div style={{ display: "flex", gap: 7 }}>
            {["#ff5f57", "#febc2e", "#28c840"].map((c, i) => (
              <div
                key={i}
                style={{
                  width: 11,
                  height: 11,
                  borderRadius: "50%",
                  background: c,
                  boxShadow: `inset 0 -1px 1px rgba(0,0,0,0.15)`,
                }}
              />
            ))}
          </div>
          <div
            style={{
              flex: 1,
              textAlign: "center",
              fontFamily,
              fontSize: 12,
              fontWeight: 500,
              color: T.textMuted,
              letterSpacing: 0.3,
            }}
          >
            {title}
          </div>
          <div style={{ width: 50 }} />
        </div>

        {/* Terminal body */}
        <div
          style={{
            padding: "20px 24px",
            fontFamily: "'Fira Code', 'SF Mono', 'Cascadia Code', monospace",
            fontSize: 15,
            lineHeight: 2,
            minHeight: 380,
            color: T.text,
          }}
        >
          {timeline.map((item, i) => {
            if (frame < item.start) return null;

            if (item.type === "blank") return <div key={i} style={{ height: 12 }} />;

            if (item.type === "input") {
              const chars = Math.min(
                item.text.length,
                Math.floor((frame - item.start) / (item.typeSpeed ?? 2))
              );
              const typing = frame < item.end;
              return (
                <div key={i}>
                  <span style={{ color: T.primary, fontWeight: 600 }}>❯ </span>
                  <span style={{ color: T.termGreen }}>{item.text.slice(0, chars)}</span>
                  {typing && (
                    <span
                      style={{
                        display: "inline-block",
                        width: 9,
                        height: 18,
                        background: T.termGreen,
                        marginLeft: 2,
                        opacity: Math.sin(frame * 0.25) > 0 ? 0.9 : 0,
                        verticalAlign: "text-bottom",
                      }}
                    />
                  )}
                </div>
              );
            }

            if (item.type === "spinner") {
              const done = frame >= item.end;
              const idx = Math.floor((frame - item.start) / 3) % SPINNER.length;
              return (
                <div key={i} style={{ color: item.color ?? T.termCyan }}>
                  {done ? (
                    <span style={{ color: T.success }}>✓ </span>
                  ) : (
                    <span>{SPINNER[idx]} </span>
                  )}
                  <span style={{ color: done ? T.text : T.textMuted }}>{item.text}</span>
                </div>
              );
            }

            // success / error / output
            const fadeIn = interpolate(frame - item.start, [0, 8], [0, 1], { extrapolateRight: "clamp" });
            const slideUp = interpolate(frame - item.start, [0, 8], [6, 0], { extrapolateRight: "clamp" });
            const prefix = item.type === "success" ? "✓ " : item.type === "error" ? "✗ " : "";
            const col =
              item.color ??
              (item.type === "success" ? T.success : item.type === "error" ? T.termRed : T.textMuted);

            return (
              <div
                key={i}
                style={{
                  opacity: fadeIn,
                  transform: `translateY(${slideUp}px)`,
                  color: col,
                }}
              >
                {prefix}
                {item.text}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ── Metric Card (glassmorphism + glow) ─────────
const MetricCard: React.FC<{
  icon: string;
  value: string;
  label: string;
  accentColor: string;
  delay: number;
}> = ({ icon, value, label, accentColor, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, stiffness: 160 },
  });
  const scale = interpolate(entrance, [0, 1], [0.8, 1]);
  const opacity = interpolate(frame - delay, [0, 12], [0, 1], { extrapolateRight: "clamp" });
  const slideY = interpolate(entrance, [0, 1], [30, 0]);

  return (
    <div
      style={{
        transform: `scale(${scale}) translateY(${slideY}px)`,
        opacity,
        background: `linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02))`,
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        border: `1px solid ${accentColor}30`,
        borderRadius: 20,
        padding: "24px 28px",
        display: "flex",
        alignItems: "center",
        gap: 20,
        boxShadow: `
          0 8px 32px rgba(0,0,0,0.3),
          inset 0 1px 0 rgba(255,255,255,0.05),
          0 0 40px ${accentColor}10
        `,
      }}
    >
      <div
        style={{
          fontSize: 36,
          width: 56,
          height: 56,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: `${accentColor}15`,
          borderRadius: 14,
          border: `1px solid ${accentColor}25`,
        }}
      >
        {icon}
      </div>
      <div>
        <div
          style={{
            fontFamily,
            fontSize: 26,
            fontWeight: 800,
            color: T.text,
            letterSpacing: -0.5,
          }}
        >
          {value}
        </div>
        <div
          style={{
            fontFamily,
            fontSize: 14,
            fontWeight: 500,
            color: T.textMuted,
            marginTop: 2,
          }}
        >
          {label}
        </div>
      </div>
    </div>
  );
};

// ── CTA Button ─────────────────────────────────
const CTAButton: React.FC<{ text: string; delay?: number }> = ({ text, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - delay,
    fps,
    config: { damping: 10, stiffness: 120 },
  });
  const scale = interpolate(entrance, [0, 1], [0.5, 1]);
  const opacity = interpolate(frame - delay, [0, 10], [0, 1], { extrapolateRight: "clamp" });

  // Subtle pulse
  const pulse = 1 + Math.sin((frame - delay) * 0.08) * 0.015;

  return (
    <div
      style={{
        transform: `scale(${scale * pulse})`,
        opacity,
        background: `linear-gradient(135deg, ${T.primary}, ${T.accent})`,
        padding: "16px 48px",
        borderRadius: 50,
        fontFamily,
        fontSize: 20,
        fontWeight: 700,
        color: "#fff",
        letterSpacing: 0.5,
        boxShadow: `
          0 4px 20px ${T.primary}50,
          0 8px 40px ${T.accent}30,
          inset 0 1px 0 rgba(255,255,255,0.2)
        `,
      }}
    >
      {text}
    </div>
  );
};

// ── Progress Bar ───────────────────────────────
const CinematicProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames, width } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames], [0, 1]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: 3,
        background: `${T.border}30`,
        zIndex: 100,
      }}
    >
      <div
        style={{
          width: `${progress * 100}%`,
          height: "100%",
          background: `linear-gradient(90deg, ${T.primary}, ${T.accent})`,
          boxShadow: `0 0 10px ${T.primary}60`,
        }}
      />
    </div>
  );
};

// ── Watermark ──────────────────────────────────
const Watermark: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [15, 30], [0, 0.35], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 100,
        right: 40,
        fontFamily,
        fontSize: 16,
        fontWeight: 600,
        color: T.text,
        opacity,
        letterSpacing: 0.5,
        zIndex: 50,
      }}
    >
      @automatiklabs
    </div>
  );
};

// ══════════════════════════════════════════════════
// MAIN COMPOSITION
// ══════════════════════════════════════════════════
export const TechTerminalPro: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: T.bg }}>
      <CinematicBackground />
      <CinematicProgressBar />
      <Watermark />

      <TransitionSeries>
        {/* ── Scene 1: Hook (3s) ─────────────────── */}
        <TransitionSeries.Sequence durationInFrames={100}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              gap: 20,
              padding: "0 60px",
            }}
          >
            <KineticText
              text="Time de Marketing"
              fontSize={68}
              fontWeight={900}
              staggerFrames={5}
            />
            <KineticText
              text="no Terminal"
              fontSize={68}
              fontWeight={900}
              delay={20}
              staggerFrames={5}
              highlightWord="Terminal"
              highlightColor={T.secondary}
            />
            <GlowLine color={T.primary} delay={35} width="40%" />
            <KineticText
              text="GrowthOS × Claude Code"
              fontSize={24}
              fontWeight={500}
              color={T.textMuted}
              delay={45}
              staggerFrames={3}
            />
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 18 })}
        />

        {/* ── Scene 2: Terminal Session (18s) ────── */}
        <TransitionSeries.Sequence durationInFrames={540}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              padding: "40px 0",
            }}
          >
            <ProTerminal
              title="Claude Code — GrowthOS"
              lines={[
                { text: "/grow create blog sobre automação com IA", type: "input", delay: 12, typeSpeed: 2 },
                { text: "Pesquisando tendências...", type: "spinner", delay: 8 },
                { text: "Blog criado — 1.847 palavras", type: "success", delay: 4 },
                { text: "SEO score: 92/100", type: "success", delay: 3 },
                { text: "", type: "blank", delay: 12 },
                { text: "/grow publish linkedin", type: "input", delay: 6, typeSpeed: 2 },
                { text: "Formatando para LinkedIn...", type: "spinner", delay: 6 },
                { text: "Publicado — linkedin.com/in/automatiklabs", type: "success", delay: 4 },
                { text: "", type: "blank", delay: 12 },
                { text: "/grow analyze competitors", type: "input", delay: 6, typeSpeed: 2 },
                { text: "Analisando 5 concorrentes...", type: "spinner", delay: 6 },
                { text: "Relatório SWOT gerado — 12 insights", type: "success", delay: 4 },
              ]}
            />
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 20 })}
        />

        {/* ── Scene 3: Metrics Highlight (7s) ────── */}
        <TransitionSeries.Sequence durationInFrames={210}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              gap: 16,
              padding: "60px 80px",
            }}
          >
            <MetricCard
              icon="✍️"
              value="1.847 palavras"
              label="Blog completo em 30 segundos"
              accentColor={T.secondary}
              delay={0}
            />
            <MetricCard
              icon="📱"
              value="LinkedIn"
              label="Publicado e otimizado para a plataforma"
              accentColor={T.primary}
              delay={18}
            />
            <MetricCard
              icon="📊"
              value="12 insights"
              label="5 concorrentes analisados automaticamente"
              accentColor={T.accent}
              delay={36}
            />
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: "from-bottom" })}
          timing={springTiming({ config: { damping: 200 }, durationInFrames: 20 })}
        />

        {/* ── Scene 4: CTA (7s) ──────────────────── */}
        <TransitionSeries.Sequence durationInFrames={210}>
          <AbsoluteFill
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              gap: 24,
              padding: "0 80px",
            }}
          >
            <KineticText
              text="Quer o GrowthOS de graça?"
              fontSize={52}
              fontWeight={800}
              staggerFrames={4}
              highlightWord="graça"
              highlightColor={T.secondary}
            />
            <GlowLine color={T.accent} delay={25} width="30%" />
            <KineticText
              text="Comenta GROWTH 👇"
              fontSize={36}
              fontWeight={700}
              color={T.accent}
              delay={35}
              staggerFrames={4}
            />
            <div style={{ marginTop: 12 }}>
              <CTAButton text="Instale grátis" delay={50} />
            </div>
          </AbsoluteFill>
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
