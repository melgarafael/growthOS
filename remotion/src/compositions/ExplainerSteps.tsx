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

const IntroScene: React.FC<{
  scene: SceneProps;
  totalSteps: number;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, totalSteps, brandColors }) => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 80,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 32,
        }}
      >
        <AnimatedText
          text={scene.text}
          animation="fade-in"
          fontSize={56}
          fontWeight={800}
          color={brandColors.text}
        />
        <AnimatedText
          text={scene.subtext || `In ${totalSteps} simple steps`}
          animation="fade-in"
          delay={15}
          fontSize={28}
          fontWeight={400}
          color={`${brandColors.text}B0`}
        />
        {/* Decorative line */}
        <div
          style={{
            width: 100,
            height: 4,
            backgroundColor: brandColors.accent,
            borderRadius: 2,
            marginTop: 8,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

const StepScene: React.FC<{
  scene: SceneProps;
  stepNumber: number;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, stepNumber, brandColors }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const numberSpring = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 80 },
  });
  const numberScale = interpolate(numberSpring, [0, 1], [0.3, 1]);
  const numberOpacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        padding: "0 120px",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          gap: 60,
        }}
      >
        {/* Large step number */}
        <div
          style={{
            opacity: numberOpacity,
            transform: `scale(${numberScale})`,
            fontSize: 140,
            fontWeight: 900,
            color: brandColors.accent,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            lineHeight: 1,
            minWidth: 140,
            textAlign: "center",
          }}
        >
          {stepNumber}
        </div>

        {/* Step content */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 20,
            paddingTop: 16,
            flex: 1,
          }}
        >
          <AnimatedText
            text={scene.text}
            animation="slide-up"
            delay={8}
            fontSize={44}
            fontWeight={700}
            color={brandColors.text}
            textAlign="left"
          />
          {scene.subtext && (
            <AnimatedText
              text={scene.subtext}
              animation="fade-in"
              delay={20}
              fontSize={26}
              fontWeight={400}
              color={`${brandColors.text}90`}
              textAlign="left"
            />
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SummaryScene: React.FC<{
  steps: SceneProps[];
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ steps, brandColors }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 80,
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            steps.length <= 4 ? "repeat(2, 1fr)" : "repeat(3, 1fr)",
          gap: 32,
          maxWidth: 1600,
          width: "100%",
        }}
      >
        {steps.map((step, i) => {
          const delay = i * 6;
          const opacity = interpolate(frame, [delay, delay + 12], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const translateY = interpolate(frame, [delay, delay + 12], [30, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <div
              key={i}
              style={{
                opacity,
                transform: `translateY(${translateY}px)`,
                backgroundColor: `${brandColors.accent}12`,
                borderRadius: 16,
                padding: 28,
                display: "flex",
                alignItems: "center",
                gap: 20,
                border: `1px solid ${brandColors.accent}25`,
              }}
            >
              <div
                style={{
                  fontSize: 36,
                  fontWeight: 800,
                  color: brandColors.accent,
                  fontFamily:
                    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  minWidth: 48,
                  textAlign: "center",
                }}
              >
                {i + 1}
              </div>
              <div
                style={{
                  fontSize: 22,
                  fontWeight: 600,
                  color: brandColors.text,
                  fontFamily:
                    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  lineHeight: 1.3,
                }}
              >
                {step.text}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const CTAScene: React.FC<{
  scene: SceneProps;
  handle: string;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, handle, brandColors }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bounceSpring = spring({
    frame,
    fps,
    config: { damping: 8, stiffness: 120 },
  });
  const scale = interpolate(bounceSpring, [0, 1], [0.5, 1]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 80,
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
            fontSize: 44,
            fontWeight: 800,
            color: brandColors.text,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          {scene.text}
        </div>
        {scene.subtext && (
          <div
            style={{
              backgroundColor: brandColors.accent,
              color: "#FFFFFF",
              fontSize: 22,
              fontWeight: 700,
              padding: "14px 44px",
              borderRadius: 50,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            }}
          >
            {scene.subtext}
          </div>
        )}
        <div
          style={{
            fontSize: 24,
            fontWeight: 500,
            color: `${brandColors.text}80`,
            marginTop: 8,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          {handle}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── Main composition ──

export const ExplainerSteps: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar = true,
  showWatermark = true,
}) => {
  const brandColors = brand.colors;
  const stepScenes = scenes.filter((s) => s.type === "step");
  const isLightBg =
    brandColors.background.toLowerCase() === "#ffffff" ||
    brandColors.background.toLowerCase() === "#fff";

  let stepNumber = 0;

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom={isLightBg ? "#f8f9fa" : brandColors.background}
        colorTo={isLightBg ? "#e9ecef" : `${brandColors.primary}20`}
      />

      {scenes.map((scene, i) => {
        const currentStepNumber = scene.type === "step" ? ++stepNumber : 0;

        return (
          <Sequence
            key={i}
            from={scene.startFrame}
            durationInFrames={scene.durationFrames}
          >
            {scene.type === "hook" && (
              <IntroScene
                scene={scene}
                totalSteps={stepScenes.length}
                brandColors={brandColors}
              />
            )}
            {scene.type === "step" && (
              <StepScene
                scene={scene}
                stepNumber={currentStepNumber}
                brandColors={brandColors}
              />
            )}
            {scene.type === "point" && (
              <SummaryScene steps={stepScenes} brandColors={brandColors} />
            )}
            {scene.type === "cta" && (
              <CTAScene
                scene={scene}
                handle={brand.handle}
                brandColors={brandColors}
              />
            )}
          </Sequence>
        );
      })}

      {showProgressBar && (
        <ProgressBar color={brandColors.accent} position="bottom" />
      )}
      {showWatermark && (
        <BrandWatermark
          handle={brand.handle}
          position={brand.watermark_position}
          color={`${brandColors.text}60`}
        />
      )}
    </AbsoluteFill>
  );
};
