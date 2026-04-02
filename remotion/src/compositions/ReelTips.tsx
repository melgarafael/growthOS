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

// ── Scene renderers ──

const HookScene: React.FC<{ scene: SceneProps; accentColor: string }> = ({
  scene,
  accentColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scaleSpring = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 80 },
  });
  const scale = interpolate(scaleSpring, [0, 1], [0.4, 1]);
  const opacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateRight: "clamp",
  });

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
          opacity,
          transform: `scale(${scale})`,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontSize: 64,
            fontWeight: 800,
            color: "#FFFFFF",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            lineHeight: 1.2,
            textShadow: `0 4px 30px ${accentColor}40`,
          }}
        >
          {scene.text}
        </div>
        {scene.subtext && (
          <div
            style={{
              fontSize: 28,
              fontWeight: 400,
              color: "rgba(255, 255, 255, 0.7)",
              marginTop: 24,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            }}
          >
            {scene.subtext}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

const PointScene: React.FC<{
  scene: SceneProps;
  index: number;
  accentColor: string;
}> = ({ scene, index, accentColor }) => {
  const isLeft = index % 2 === 0;
  const animation = isLeft ? "slide-left" : "slide-right";

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
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 24,
          maxWidth: 900,
        }}
      >
        {scene.icon && (
          <div style={{ fontSize: 80, marginBottom: 8 }}>{scene.icon}</div>
        )}
        <AnimatedText
          text={scene.text}
          animation={animation}
          fontSize={52}
          fontWeight={700}
          color="#FFFFFF"
        />
        {scene.subtext && (
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={10}
            fontSize={28}
            fontWeight={400}
            color="rgba(255, 255, 255, 0.75)"
          />
        )}
        {/* Accent underline */}
        <div
          style={{
            width: 80,
            height: 4,
            backgroundColor: accentColor,
            borderRadius: 2,
            marginTop: 12,
          }}
        />
      </div>
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
  const opacity = interpolate(frame, [0, 8], [0, 1], {
    extrapolateRight: "clamp",
  });

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
          opacity,
          transform: `scale(${scale})`,
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 32,
        }}
      >
        <div
          style={{
            fontSize: 32,
            fontWeight: 600,
            color: "rgba(255, 255, 255, 0.8)",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          {handle}
        </div>
        <div
          style={{
            fontSize: 48,
            fontWeight: 800,
            color: "#FFFFFF",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          {scene.text}
        </div>
        {scene.subtext && (
          <div
            style={{
              backgroundColor: accentColor,
              color: "#FFFFFF",
              fontSize: 24,
              fontWeight: 700,
              padding: "14px 40px",
              borderRadius: 50,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            }}
          >
            {scene.subtext}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

// ── Main composition ──

export const ReelTips: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar = true,
  showWatermark = true,
}) => {
  const accentColor = brand.colors.accent;

  let pointIndex = 0;

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#1a1a2e"
        colorMid={`${accentColor}15`}
      />

      {scenes.map((scene, i) => {
        const currentPointIndex = scene.type === "point" ? pointIndex++ : 0;

        return (
          <Sequence
            key={i}
            from={scene.startFrame}
            durationInFrames={scene.durationFrames}
          >
            {scene.type === "hook" && (
              <HookScene scene={scene} accentColor={accentColor} />
            )}
            {scene.type === "point" && (
              <PointScene
                scene={scene}
                index={currentPointIndex}
                accentColor={accentColor}
              />
            )}
            {scene.type === "cta" && (
              <CTAScene
                scene={scene}
                handle={brand.handle}
                accentColor={accentColor}
              />
            )}
          </Sequence>
        );
      })}

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
