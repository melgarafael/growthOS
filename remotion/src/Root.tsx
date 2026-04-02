import React from "react";
import { Composition, AbsoluteFill, Sequence } from "remotion";
import { compositions } from "./compositions/index";
import type { CompositionProps, BrandProps } from "./types";
import { AnimatedText } from "./components/AnimatedText";
import { ProgressBar } from "./components/ProgressBar";
import { BrandWatermark } from "./components/BrandWatermark";
import { BackgroundGradient } from "./components/BackgroundGradient";

/** Generic scene renderer used by all compositions until Phase B templates are built */
const GenericComposition: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar = true,
  showWatermark = true,
}) => {
  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom={brand.colors.background}
        colorTo={brand.colors.primary}
        colorMid={brand.colors.secondary}
      />
      {scenes.map((scene, i) => (
        <Sequence
          key={i}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
          name={`${scene.type}-${i}`}
        >
          <AbsoluteFill
            style={{
              justifyContent: "center",
              alignItems: "center",
              padding: 40,
              flexDirection: "column",
              gap: 20,
            }}
          >
            {scene.icon && (
              <div style={{ fontSize: 64, marginBottom: 10 }}>{scene.icon}</div>
            )}
            <AnimatedText
              text={scene.text}
              animation={scene.animation}
              color={brand.colors.text}
              fontSize={48}
            />
            {scene.subtext && (
              <AnimatedText
                text={scene.subtext}
                animation="fade-in"
                delay={15}
                color={brand.colors.text}
                fontSize={28}
              />
            )}
          </AbsoluteFill>
        </Sequence>
      ))}
      {showProgressBar && <ProgressBar color={brand.colors.accent} />}
      {showWatermark && (
        <BrandWatermark
          handle={brand.handle}
          position={brand.watermark_position}
        />
      )}
    </AbsoluteFill>
  );
};

// ── Default props ──

const defaultBrand: BrandProps = {
  name: "GrowthOS",
  handle: "growthos",
  colors: {
    primary: "#6366f1",
    secondary: "#8b5cf6",
    background: "#0f0f23",
    text: "#ffffff",
    accent: "#f59e0b",
  },
  watermark_position: "bottom-right",
};

const defaultProps: CompositionProps = {
  brand: defaultBrand,
  scenes: [
    {
      type: "hook",
      startFrame: 0,
      durationFrames: 90,
      text: "Your Hook Here",
      animation: "scale-in",
    },
    {
      type: "point",
      startFrame: 90,
      durationFrames: 150,
      text: "Main Point",
      subtext: "Supporting detail goes here",
      animation: "slide-left",
    },
    {
      type: "cta",
      startFrame: 240,
      durationFrames: 90,
      text: "Follow for more!",
      icon: "\uD83D\uDC49",
      animation: "bounce",
    },
  ],
  showProgressBar: true,
  showWatermark: true,
};

// ── Root registration ──

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {compositions.map((comp) => (
        <Composition
          key={comp.id}
          id={comp.id}
          component={GenericComposition}
          durationInFrames={comp.defaultDuration * comp.fps}
          fps={comp.fps}
          width={comp.width}
          height={comp.height}
          defaultProps={defaultProps}
        />
      ))}
    </>
  );
};
