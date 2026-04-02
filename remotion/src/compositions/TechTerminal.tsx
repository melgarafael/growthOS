import React from "react";
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  spring,
} from "remotion";
import { AnimatedText } from "../components/AnimatedText";
import { BackgroundGradient } from "../components/BackgroundGradient";
import { TerminalEmulator } from "../components/TerminalEmulator";
import { GlassmorphismCard } from "../components/GlassmorphismCard";
import { BrandWatermark } from "../components/BrandWatermark";

// ── Scene 1: Hook (0–90 frames / 3s) ────────────────────────────────────────

const SceneHook: React.FC = () => {
  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#0d1117"
        direction={135}
        animated={false}
      />

      {/* Subtle grid overlay for techy feel */}
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(rgba(0,206,201,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,206,201,0.03) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 24,
          padding: 60,
        }}
      >
        {/* Accent line above */}
        <SceneHookAccentLine />

        <AnimatedText
          text="Time de Marketing no Terminal"
          animation="scale-in"
          delay={5}
          fontSize={64}
          color="#ffffff"
          fontWeight={800}
          textAlign="center"
          style={{ letterSpacing: -1, lineHeight: 1.15 }}
        />

        <AnimatedText
          text="GrowthOS × Claude Code"
          animation="fade-in"
          delay={20}
          fontSize={28}
          color="#00cec9"
          fontWeight={500}
          textAlign="center"
          style={{ letterSpacing: 2 }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const SceneHookAccentLine: React.FC = () => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [0, 30], [0, 120], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width,
        height: 3,
        background: "linear-gradient(90deg, #6c5ce7, #00cec9)",
        borderRadius: 2,
        opacity,
        marginBottom: 8,
      }}
    />
  );
};

// ── Scene 2: Terminal Session (90–600 frames / 17s) ─────────────────────────

const TERMINAL_COMMANDS = [
  {
    text: "/grow create blog sobre automação com IA",
    type: "input" as const,
    delay: 15,
    typeSpeed: 2,
  },
  { text: "Pesquisando tendências...", type: "spinner" as const, delay: 10 },
  { text: "Blog criado — 1.847 palavras", type: "success" as const, delay: 5 },
  { text: "SEO score: 92/100", type: "success" as const, delay: 3 },
  { text: "", type: "blank" as const, delay: 10 },
  { text: "/grow publish linkedin", type: "input" as const, delay: 8, typeSpeed: 2 },
  {
    text: "Formatando para LinkedIn...",
    type: "spinner" as const,
    delay: 8,
  },
  {
    text: "Publicado em linkedin.com/in/automatiklabs",
    type: "success" as const,
    delay: 5,
  },
  { text: "", type: "blank" as const, delay: 8 },
  {
    text: "/grow analyze competitors",
    type: "input" as const,
    delay: 8,
    typeSpeed: 2,
  },
  {
    text: "Analisando 5 concorrentes...",
    type: "spinner" as const,
    delay: 8,
  },
  { text: "Relatório SWOT gerado", type: "success" as const, delay: 5 },
];

const SceneTerminal: React.FC = () => {
  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#0d1117"
        colorMid="#0d1117"
        direction={160}
        animated={false}
      />

      {/* Subtle scanline effect for terminal vibe */}
      <AbsoluteFill
        style={{
          backgroundImage:
            "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px)",
          pointerEvents: "none",
        }}
      />

      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: "40px 60px",
        }}
      >
        {/* Label above terminal */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            marginBottom: 24,
            alignSelf: "flex-start",
          }}
        >
          <TerminalLabelDot />
          <AnimatedText
            text="Claude Code — Terminal"
            animation="fade-in"
            delay={0}
            fontSize={18}
            color="rgba(0,206,201,0.7)"
            fontWeight={500}
          />
        </div>

        {/* Terminal — occupies ~65% height */}
        <div style={{ width: "100%", flex: 1 }}>
          <TerminalEmulator
            commands={TERMINAL_COMMANDS}
            theme="dark"
            prompt="growthOS $"
            title="Claude Code — GrowthOS"
            fontSize={18}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const TerminalLabelDot: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15, 25, 35], [0, 1, 1, 0.4], {
    extrapolateRight: "clamp",
  });
  const pulseOpacity = 0.4 + Math.sin(frame * 0.15) * 0.3;

  return (
    <div
      style={{
        width: 10,
        height: 10,
        borderRadius: "50%",
        background: "#00cec9",
        opacity: Math.max(opacity, pulseOpacity),
        boxShadow: "0 0 8px #00cec9",
      }}
    />
  );
};

// ── Scene 3: Output Highlight (600–810 frames / 7s) ─────────────────────────

interface ResultCardProps {
  icon: string;
  headline: string;
  subtext: string;
  accentColor: string;
  delayFrames: number;
}

const ResultCard: React.FC<ResultCardProps> = ({
  icon,
  headline,
  subtext,
  accentColor,
  delayFrames,
}) => {
  const frame = useCurrentFrame();
  const localFrame = Math.max(0, frame - delayFrames);
  const { fps } = useVideoConfig();

  const slideSpring = spring({
    frame: localFrame,
    fps,
    config: { damping: 14, stiffness: 100, mass: 0.9 },
  });

  const translateY = interpolate(slideSpring, [0, 1], [50, 0]);
  const opacity = interpolate(localFrame, [0, 18], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        transform: `translateY(${translateY}px)`,
        opacity,
      }}
    >
      <GlassmorphismCard
        blur={16}
        opacity={0.12}
        borderColor={`${accentColor}40`}
        rounded={20}
        animateIn="none"
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 24,
            padding: "8px 16px",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          <div
            style={{
              fontSize: 44,
              lineHeight: 1,
              flexShrink: 0,
            }}
          >
            {icon}
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div
              style={{
                fontSize: 34,
                fontWeight: 800,
                color: "#ffffff",
                letterSpacing: -0.5,
              }}
            >
              {headline}
            </div>
            <div
              style={{
                fontSize: 20,
                color: accentColor,
                fontWeight: 500,
                opacity: 0.9,
              }}
            >
              {subtext}
            </div>
          </div>
        </div>
      </GlassmorphismCard>
    </div>
  );
};

const SceneOutputHighlight: React.FC = () => {
  const frame = useCurrentFrame();

  // Terminal fades to dimmed background
  const terminalOpacity = interpolate(frame, [0, 20], [1, 0.28], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#0d1117"
        direction={160}
        animated={false}
      />

      {/* Dimmed terminal in background */}
      <AbsoluteFill
        style={{
          opacity: terminalOpacity,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: "40px 60px",
        }}
      >
        <div style={{ width: "100%", flex: 1 }}>
          <TerminalEmulator
            commands={TERMINAL_COMMANDS}
            theme="dark"
            prompt="growthOS $"
            title="Claude Code — GrowthOS"
            fontSize={18}
          />
        </div>
      </AbsoluteFill>

      {/* Purple glow overlay */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(108,92,231,0.18) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />

      {/* Result cards column — centered overlay */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: "60px 80px",
          gap: 28,
        }}
      >
        <ResultCard
          icon="✍️"
          headline="1.847 palavras"
          subtext="Blog completo em 30 segundos"
          accentColor="#00cec9"
          delayFrames={0}
        />
        <ResultCard
          icon="📱"
          headline="LinkedIn"
          subtext="Publicado e otimizado para a plataforma"
          accentColor="#6c5ce7"
          delayFrames={60}
        />
        <ResultCard
          icon="📊"
          headline="SWOT"
          subtext="5 concorrentes analisados automaticamente"
          accentColor="#fd79a8"
          delayFrames={120}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 4: CTA (810–1050 frames / 8s) ─────────────────────────────────────

const SceneCTA: React.FC = () => {
  const frame = useCurrentFrame();

  const cardsOpacity = interpolate(frame, [0, 20], [1, 0], {
    extrapolateRight: "clamp",
  });

  // Glowing ring pulse
  const glowScale = 1 + Math.sin(frame * 0.08) * 0.04;
  const glowOpacity = 0.15 + Math.sin(frame * 0.1) * 0.08;

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#1a1a2e"
        colorMid="#0d1117"
        direction={145}
        animated={false}
      />

      {/* Animated glow behind CTA */}
      <AbsoluteFill
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div
          style={{
            width: 600,
            height: 600,
            borderRadius: "50%",
            background:
              "radial-gradient(ellipse, rgba(108,92,231,0.25) 0%, transparent 70%)",
            transform: `scale(${glowScale})`,
            opacity: glowOpacity,
          }}
        />
      </AbsoluteFill>

      {/* Fading cards (carry-over from prev scene) */}
      <AbsoluteFill style={{ opacity: cardsOpacity }}>
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            padding: "60px 80px",
            gap: 28,
          }}
        >
          <GlassmorphismCard
            blur={16}
            opacity={0.08}
            borderColor="rgba(0,206,201,0.2)"
            rounded={20}
            animateIn="none"
          >
            <div style={{ padding: "8px 32px", color: "#ffffff", fontSize: 32 }}>
              ✍️ 1.847 palavras
            </div>
          </GlassmorphismCard>
          <GlassmorphismCard
            blur={16}
            opacity={0.08}
            borderColor="rgba(108,92,231,0.2)"
            rounded={20}
            animateIn="none"
          >
            <div style={{ padding: "8px 32px", color: "#ffffff", fontSize: 32 }}>
              📱 LinkedIn
            </div>
          </GlassmorphismCard>
          <GlassmorphismCard
            blur={16}
            opacity={0.08}
            borderColor="rgba(253,121,168,0.2)"
            rounded={20}
            animateIn="none"
          >
            <div style={{ padding: "8px 32px", color: "#ffffff", fontSize: 32 }}>
              📊 SWOT
            </div>
          </GlassmorphismCard>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* Main CTA content */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 32,
          padding: 60,
        }}
      >
        <AnimatedText
          text="Instale o GrowthOS grátis"
          animation="bounce"
          delay={15}
          fontSize={56}
          color="#ffffff"
          fontWeight={800}
          textAlign="center"
          style={{ letterSpacing: -1 }}
        />

        <AnimatedText
          text="Comenta GROWTH 👇"
          animation="fade-in"
          delay={35}
          fontSize={36}
          color="#fd79a8"
          fontWeight={700}
          textAlign="center"
        />

        {/* Decorative divider */}
        <CTADivider delay={50} />
      </AbsoluteFill>

      <BrandWatermark
        handle="@automatiklabs"
        position="bottom-right"
        color="rgba(255,255,255,0.45)"
        fontSize={20}
      />
    </AbsoluteFill>
  );
};

const CTADivider: React.FC<{ delay: number }> = ({ delay }) => {
  const frame = useCurrentFrame();
  const localFrame = Math.max(0, frame - delay);
  const width = interpolate(localFrame, [0, 25], [0, 200], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(localFrame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width,
        height: 2,
        background: "linear-gradient(90deg, #6c5ce7, #fd79a8)",
        borderRadius: 2,
        opacity,
      }}
    />
  );
};

// ── Main Composition ─────────────────────────────────────────────────────────

export const TechTerminal: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      {/* Scene 1: Hook — 0 to 90 frames (3s) */}
      <Sequence from={0} durationInFrames={90}>
        <SceneHook />
      </Sequence>

      {/* Scene 2: Terminal Session — 90 to 600 frames (17s) */}
      <Sequence from={90} durationInFrames={510}>
        <SceneTerminal />
      </Sequence>

      {/* Scene 3: Output Highlight — 600 to 810 frames (7s) */}
      <Sequence from={600} durationInFrames={210}>
        <SceneOutputHighlight />
      </Sequence>

      {/* Scene 4: CTA — 810 to 1050 frames (8s) */}
      <Sequence from={810} durationInFrames={240}>
        <SceneCTA />
      </Sequence>
    </AbsoluteFill>
  );
};
