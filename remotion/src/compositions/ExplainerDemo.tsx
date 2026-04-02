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

const ProblemScene: React.FC<{
  scene: SceneProps;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, brandColors }) => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 100,
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
        {scene.icon && (
          <div style={{ fontSize: 72, marginBottom: 8 }}>{scene.icon}</div>
        )}
        <AnimatedText
          text={scene.text}
          animation="fade-in"
          fontSize={52}
          fontWeight={800}
          color={brandColors.text}
        />
        {scene.subtext && (
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={12}
            fontSize={26}
            color={`${brandColors.text}90`}
          />
        )}
      </div>
    </AbsoluteFill>
  );
};

const SolutionScene: React.FC<{
  scene: SceneProps;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, brandColors }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scaleSpring = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 80 },
  });
  const scale = interpolate(scaleSpring, [0, 1], [0.5, 1]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 100,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
        }}
      >
        <div
          style={{
            fontSize: 20,
            fontWeight: 600,
            color: brandColors.accent,
            letterSpacing: 4,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          }}
        >
          INTRODUCING
        </div>
        <div
          style={{
            fontSize: 64,
            fontWeight: 900,
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
              fontSize: 28,
              fontWeight: 400,
              color: `${brandColors.text}80`,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              marginTop: 8,
            }}
          >
            {scene.subtext}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

const FeatureScene: React.FC<{
  scene: SceneProps;
  featureIndex: number;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, featureIndex, brandColors }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cardSpring = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });
  const cardScale = interpolate(cardSpring, [0, 1], [0.8, 1]);
  const cardOpacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 100,
      }}
    >
      <div
        style={{
          opacity: cardOpacity,
          transform: `scale(${cardScale})`,
          backgroundColor: `${brandColors.accent}10`,
          borderRadius: 24,
          padding: 60,
          maxWidth: 1200,
          width: "100%",
          border: `2px solid ${brandColors.accent}25`,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 40,
          }}
        >
          {scene.icon && (
            <div style={{ fontSize: 64 }}>{scene.icon}</div>
          )}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 16,
              flex: 1,
            }}
          >
            <div
              style={{
                fontSize: 14,
                fontWeight: 600,
                color: brandColors.accent,
                letterSpacing: 3,
                fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              }}
            >
              FEATURE {featureIndex + 1}
            </div>
            <div
              style={{
                fontSize: 40,
                fontWeight: 700,
                color: brandColors.text,
                fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                lineHeight: 1.2,
              }}
            >
              {scene.text}
            </div>
            {scene.subtext && (
              <div
                style={{
                  fontSize: 24,
                  fontWeight: 400,
                  color: `${brandColors.text}80`,
                  fontFamily:
                    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  lineHeight: 1.5,
                  marginTop: 8,
                }}
              >
                {scene.subtext}
              </div>
            )}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SocialProofScene: React.FC<{
  scene: SceneProps;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, brandColors }) => {
  // Parse number from text like "10000 users already..."
  const numericMatch = scene.text.match(/([\d,.]+)/);
  const target = numericMatch ? parseFloat(numericMatch[1].replace(/,/g, "")) : 0;
  const textBefore = scene.text.match(/^(.*?)[\d,.]+/)?.[1] || "";
  const textAfter = scene.text.match(/[\d,.]+(.*?)$/)?.[1] || "";

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 100,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 16,
        }}
      >
        {target > 0 ? (
          <div
            style={{
              display: "flex",
              alignItems: "baseline",
              gap: 12,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            }}
          >
            {textBefore && (
              <span
                style={{
                  fontSize: 36,
                  fontWeight: 600,
                  color: brandColors.text,
                }}
              >
                {textBefore}
              </span>
            )}
            <CounterUp
              target={target}
              durationFrames={90}
              fontSize={80}
              color={brandColors.accent}
              fontWeight={800}
            />
            {textAfter && (
              <span
                style={{
                  fontSize: 36,
                  fontWeight: 600,
                  color: brandColors.text,
                }}
              >
                {textAfter}
              </span>
            )}
          </div>
        ) : (
          <AnimatedText
            text={scene.text}
            animation="scale-in"
            fontSize={48}
            fontWeight={700}
            color={brandColors.text}
          />
        )}
        {scene.subtext && (
          <AnimatedText
            text={scene.subtext}
            animation="fade-in"
            delay={20}
            fontSize={26}
            color={`${brandColors.text}80`}
          />
        )}
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
    config: { damping: 8, stiffness: 150, mass: 0.8 },
  });
  const scale = interpolate(bounceSpring, [0, 1], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 100,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 24,
        }}
      >
        <div
          style={{
            fontSize: 48,
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
              fontSize: 24,
              fontWeight: 700,
              padding: "16px 48px",
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
            fontSize: 22,
            fontWeight: 500,
            color: `${brandColors.text}70`,
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

export const ExplainerDemo: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar = true,
  showWatermark = true,
}) => {
  const brandColors = brand.colors;
  const isLightBg =
    brandColors.background.toLowerCase() === "#ffffff" ||
    brandColors.background.toLowerCase() === "#fff";

  let featureIndex = 0;

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom={isLightBg ? "#f8f9fa" : brandColors.background}
        colorTo={isLightBg ? "#ffffff" : `${brandColors.primary}15`}
      />

      {scenes.map((scene, i) => {
        const currentFeatureIndex = scene.type === "demo" ? featureIndex++ : 0;

        return (
          <Sequence
            key={i}
            from={scene.startFrame}
            durationInFrames={scene.durationFrames}
          >
            {scene.type === "hook" && (
              <ProblemScene scene={scene} brandColors={brandColors} />
            )}
            {scene.type === "step" && (
              <SolutionScene scene={scene} brandColors={brandColors} />
            )}
            {scene.type === "demo" && (
              <FeatureScene
                scene={scene}
                featureIndex={currentFeatureIndex}
                brandColors={brandColors}
              />
            )}
            {scene.type === "number" && (
              <SocialProofScene scene={scene} brandColors={brandColors} />
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
