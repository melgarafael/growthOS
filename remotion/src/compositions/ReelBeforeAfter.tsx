import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
  AbsoluteFill,
} from "remotion";
import type { CompositionProps, SceneProps } from "../types";
import { AnimatedText } from "../components/AnimatedText";
import { ProgressBar } from "../components/ProgressBar";
import { BrandWatermark } from "../components/BrandWatermark";
import { BackgroundGradient } from "../components/BackgroundGradient";
import { TransitionWipe } from "../components/TransitionWipe";

// ── Scene renderers ──

const HookScene: React.FC<{ scene: SceneProps; accentColor: string }> = ({
  scene,
  accentColor,
}) => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <AnimatedText
        text={scene.text}
        animation="scale-in"
        fontSize={56}
        fontWeight={800}
        color="#FFFFFF"
      />
      {scene.subtext && (
        <div style={{ marginTop: 20 }}>
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={15}
            fontSize={26}
            color="rgba(255, 255, 255, 0.7)"
          />
        </div>
      )}
    </AbsoluteFill>
  );
};

const ComparisonScene: React.FC<{
  scene: SceneProps;
  accentColor: string;
}> = ({ scene, accentColor }) => {
  const frame = useCurrentFrame();

  // Split text on " | " or use text/subtext for before/after
  const beforeText = scene.text;
  const afterText = scene.subtext || "";

  const wipeProgress = interpolate(frame, [30, 50], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const beforeOpacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      {/* Before side (left) — dark */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: "50%",
          height: "100%",
          backgroundColor: "rgba(0, 0, 0, 0.4)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: 40,
          opacity: beforeOpacity,
        }}
      >
        <div
          style={{
            fontSize: 20,
            fontWeight: 600,
            color: "#FF6B6B",
            letterSpacing: 3,
            marginBottom: 24,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          BEFORE
        </div>
        <div
          style={{
            fontSize: 32,
            fontWeight: 700,
            color: "rgba(255, 255, 255, 0.85)",
            textAlign: "center",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            lineHeight: 1.3,
          }}
        >
          {beforeText}
        </div>
      </div>

      {/* After side (right) — revealed with wipe */}
      <div
        style={{
          position: "absolute",
          right: 0,
          top: 0,
          width: "50%",
          height: "100%",
          backgroundColor: `${accentColor}20`,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: 40,
          clipPath: `inset(0 ${100 - wipeProgress}% 0 0)`,
        }}
      >
        <div
          style={{
            fontSize: 20,
            fontWeight: 600,
            color: "#4ECB71",
            letterSpacing: 3,
            marginBottom: 24,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          AFTER
        </div>
        <div
          style={{
            fontSize: 32,
            fontWeight: 700,
            color: "#FFFFFF",
            textAlign: "center",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            lineHeight: 1.3,
          }}
        >
          {afterText}
        </div>
      </div>

      {/* Center divider */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "15%",
          bottom: "15%",
          width: 3,
          backgroundColor: "rgba(255, 255, 255, 0.2)",
          transform: "translateX(-50%)",
        }}
      />
    </AbsoluteFill>
  );
};

const RevealScene: React.FC<{ scene: SceneProps; accentColor: string }> = ({
  scene,
  accentColor,
}) => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
        backgroundColor: `${accentColor}10`,
      }}
    >
      <AnimatedText
        text={scene.text}
        animation="slide-up"
        fontSize={52}
        fontWeight={800}
        color="#FFFFFF"
      />
      {scene.subtext && (
        <div style={{ marginTop: 24 }}>
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={15}
            fontSize={28}
            color="rgba(255, 255, 255, 0.75)"
          />
        </div>
      )}
    </AbsoluteFill>
  );
};

const CTAScene: React.FC<{
  scene: SceneProps;
  handle: string;
  accentColor: string;
}> = ({ scene, handle, accentColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bounceSpring = spring({
    frame,
    fps,
    config: { damping: 8, stiffness: 150, mass: 0.8 },
  });
  const scale = interpolate(bounceSpring, [0, 1], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 28,
        }}
      >
        <div
          style={{
            fontSize: 30,
            fontWeight: 500,
            color: "rgba(255, 255, 255, 0.7)",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          {handle}
        </div>
        <div
          style={{
            fontSize: 44,
            fontWeight: 800,
            color: "#FFFFFF",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          {scene.text}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── Main composition ──

export const ReelBeforeAfter: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar = true,
  showWatermark = true,
}) => {
  const accentColor = brand.colors.accent;

  return (
    <AbsoluteFill>
      <BackgroundGradient colorFrom="#0a0a0a" colorTo="#12121f" />

      {scenes.map((scene, i) => (
        <Sequence
          key={i}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
        >
          {scene.type === "hook" && (
            <HookScene scene={scene} accentColor={accentColor} />
          )}
          {scene.type === "comparison" && (
            <ComparisonScene scene={scene} accentColor={accentColor} />
          )}
          {scene.type === "demo" && (
            <RevealScene scene={scene} accentColor={accentColor} />
          )}
          {scene.type === "cta" && (
            <CTAScene
              scene={scene}
              handle={brand.handle}
              accentColor={accentColor}
            />
          )}
        </Sequence>
      ))}

      {showProgressBar && <ProgressBar color={accentColor} />}
      {showWatermark && (
        <BrandWatermark
          handle={brand.handle}
          position={brand.watermark_position}
        />
      )}
    </AbsoluteFill>
  );
};
