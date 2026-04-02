import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Sequence,
} from "remotion";
import { AnimatedText } from "../components/AnimatedText";
import { ProgressBar } from "../components/ProgressBar";
import { BrandWatermark } from "../components/BrandWatermark";
import type { CompositionProps, SceneProps } from "../types";

const Scene: React.FC<{
  scene: SceneProps;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, brandColors }) => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  const isHook = scene.type === "hook";
  const isCta = scene.type === "cta";

  return (
    <AbsoluteFill
      style={{
        backgroundColor: brandColors.background,
        opacity: bgOpacity,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "80px 60px",
      }}
    >
      {/* Background gradient */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: isHook
            ? `radial-gradient(ellipse at center, ${brandColors.primary}22 0%, ${brandColors.background} 70%)`
            : isCta
              ? `radial-gradient(ellipse at center, ${brandColors.accent}22 0%, ${brandColors.background} 70%)`
              : `linear-gradient(180deg, ${brandColors.background} 0%, ${brandColors.primary}08 100%)`,
          zIndex: 0,
        }}
      />

      {/* Icon */}
      {scene.icon && (
        <AnimatedText
          text={scene.icon}
          animation={scene.animation}
          delay={0}
          style={{
            fontSize: isHook ? 80 : 64,
            marginBottom: 24,
            zIndex: 1,
          }}
        />
      )}

      {/* Main text */}
      <AnimatedText
        text={scene.text}
        animation={scene.animation}
        delay={5}
        style={{
          fontSize: isHook ? 72 : isCta ? 64 : 56,
          fontWeight: 800,
          color: brandColors.text,
          textAlign: "center",
          lineHeight: 1.2,
          zIndex: 1,
          fontFamily: "SF Pro Display, Inter, system-ui, sans-serif",
          maxWidth: "90%",
        }}
      />

      {/* Subtext */}
      {scene.subtext && (
        <AnimatedText
          text={scene.subtext}
          animation="fade-in"
          delay={15}
          style={{
            fontSize: isCta ? 40 : 28,
            fontWeight: isCta ? 700 : 400,
            color: isCta ? brandColors.accent : `${brandColors.text}bb`,
            textAlign: "center",
            marginTop: 20,
            lineHeight: 1.4,
            zIndex: 1,
            fontFamily: "SF Pro Display, Inter, system-ui, sans-serif",
            maxWidth: "85%",
          }}
        />
      )}
    </AbsoluteFill>
  );
};

export const ReelTips: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar,
  showWatermark,
}) => {
  const { fps } = useVideoConfig();

  // If no scenes provided, use the GrowthOS demo storyboard
  const videoScenes: SceneProps[] =
    scenes.length > 0
      ? scenes
      : [
          {
            type: "hook",
            startFrame: 0,
            durationFrames: 90,
            text: "Time de Marketing Futurista",
            subtext: "dentro do Claude Code",
            icon: "🤖",
            animation: "scale-in",
            transition: "cut",
          },
          {
            type: "point",
            startFrame: 90,
            durationFrames: 150,
            text: "7 Agentes de IA especializados",
            subtext: "Estrategista, Copywriter, Designer, Analista...",
            icon: "🧠",
            animation: "slide-left",
            transition: "crossfade",
          },
          {
            type: "point",
            startFrame: 240,
            durationFrames: 150,
            text: "Cria conteúdo com a sua voz",
            subtext: "Blog, social, vídeo, carousel — tudo on-brand",
            icon: "✍️",
            animation: "slide-right",
            transition: "crossfade",
          },
          {
            type: "point",
            startFrame: 390,
            durationFrames: 150,
            text: "Pesquisa, analisa e publica",
            subtext: "Concorrentes, tendências, SEO — automático",
            icon: "📊",
            animation: "slide-left",
            transition: "crossfade",
          },
          {
            type: "point",
            startFrame: 540,
            durationFrames: 150,
            text: "Pipeline completo",
            subtext: "Da ideia ao post publicado — sem sair do terminal",
            icon: "⚡",
            animation: "slide-right",
            transition: "crossfade",
          },
          {
            type: "point",
            startFrame: 690,
            durationFrames: 150,
            text: "Tudo grátis e open-source",
            subtext: "Roda direto no seu Claude Code",
            icon: "🔓",
            animation: "scale-in",
            transition: "crossfade",
          },
          {
            type: "transition",
            startFrame: 840,
            durationFrames: 60,
            text: "",
            animation: "fade-out",
            transition: "crossfade",
          },
          {
            type: "cta",
            startFrame: 900,
            durationFrames: 150,
            text: "Quer o GrowthOS de graça?",
            subtext: "Comenta GROWTH 👇",
            icon: "💬",
            animation: "bounce",
            transition: "crossfade",
          },
        ];

  return (
    <AbsoluteFill style={{ backgroundColor: brand.colors.background }}>
      {/* Scenes */}
      {videoScenes.map((scene, i) => (
        <Sequence
          key={i}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
        >
          <Scene scene={scene} brandColors={brand.colors} />
        </Sequence>
      ))}

      {/* Progress bar */}
      {showProgressBar && (
        <ProgressBar color={brand.colors.primary} position="top" />
      )}

      {/* Watermark */}
      {showWatermark && (
        <BrandWatermark
          handle={brand.handle}
          color={brand.colors.text}
          position="bottom-right"
          opacity={0.4}
        />
      )}
    </AbsoluteFill>
  );
};
