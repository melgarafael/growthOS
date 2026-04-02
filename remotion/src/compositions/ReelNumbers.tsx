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
import { CounterUp } from "../components/CounterUp";

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
        animation="fade-in"
        fontSize={56}
        fontWeight={800}
        color="#FFFFFF"
      />
      {scene.subtext && (
        <div style={{ marginTop: 20 }}>
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={12}
            fontSize={28}
            color="rgba(255, 255, 255, 0.7)"
          />
        </div>
      )}
    </AbsoluteFill>
  );
};

const NumberScene: React.FC<{
  scene: SceneProps;
  accentColor: string;
}> = ({ scene, accentColor }) => {
  // Parse target number from text (e.g. "10000" or "85%")
  const numericMatch = scene.text.match(/([\d,.]+)/);
  const target = numericMatch ? parseFloat(numericMatch[1].replace(/,/g, "")) : 0;

  // Extract prefix/suffix from around the number
  const prefix = scene.text.match(/^([^\d]*)/)?.[1] || "";
  const suffix = scene.text.match(/[\d,.]+(.*?)$/)?.[1] || "";

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
          gap: 20,
        }}
      >
        {scene.icon && (
          <div style={{ fontSize: 64, marginBottom: 8 }}>{scene.icon}</div>
        )}
        <CounterUp
          target={target}
          prefix={prefix}
          suffix={suffix}
          durationFrames={75}
          fontSize={96}
          color={accentColor}
          fontWeight={800}
        />
        {scene.subtext && (
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={20}
            fontSize={30}
            fontWeight={500}
            color="rgba(255, 255, 255, 0.8)"
          />
        )}
        {/* Accent glow line */}
        <div
          style={{
            width: 120,
            height: 3,
            backgroundColor: accentColor,
            borderRadius: 2,
            marginTop: 16,
            boxShadow: `0 0 20px ${accentColor}80`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

const InsightScene: React.FC<{ scene: SceneProps; accentColor: string }> = ({
  scene,
  accentColor,
}) => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
        backgroundColor: `${accentColor}08`,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 24,
        }}
      >
        <div
          style={{
            fontSize: 20,
            fontWeight: 600,
            color: accentColor,
            letterSpacing: 4,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          KEY INSIGHT
        </div>
        <AnimatedText
          text={scene.text}
          animation="slide-up"
          fontSize={44}
          fontWeight={700}
          color="#FFFFFF"
        />
        {scene.subtext && (
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={15}
            fontSize={26}
            color="rgba(255, 255, 255, 0.7)"
          />
        )}
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

export const ReelNumbers: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar = true,
  showWatermark = true,
}) => {
  const accentColor = brand.colors.accent;

  return (
    <AbsoluteFill>
      <BackgroundGradient colorFrom="#0a0a0a" colorTo="#0f0f1a" />

      {scenes.map((scene, i) => (
        <Sequence
          key={i}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
        >
          {scene.type === "hook" && (
            <HookScene scene={scene} accentColor={accentColor} />
          )}
          {scene.type === "number" && (
            <NumberScene scene={scene} accentColor={accentColor} />
          )}
          {scene.type === "point" && (
            <InsightScene scene={scene} accentColor={accentColor} />
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
