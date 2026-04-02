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

// ── Constants ──

const TRANSITION_FRAMES = 15; // 0.5s at 30fps

// ── Scene renderers ──

const CoverScene: React.FC<{
  scene: SceneProps;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, brandColors }) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 20], [0, 1], {
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
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 24,
        }}
      >
        {scene.icon && (
          <div style={{ fontSize: 64, marginBottom: 8 }}>{scene.icon}</div>
        )}
        <div
          style={{
            fontSize: 56,
            fontWeight: 800,
            color: brandColors.text,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            lineHeight: 1.2,
            maxWidth: 900,
          }}
        >
          {scene.text}
        </div>
        {scene.subtext && (
          <div
            style={{
              fontSize: 26,
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
        {/* Swipe hint */}
        <div
          style={{
            fontSize: 16,
            fontWeight: 500,
            color: `${brandColors.text}50`,
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            marginTop: 40,
            letterSpacing: 2,
          }}
        >
          SWIPE &rarr;
        </div>
      </div>
    </AbsoluteFill>
  );
};

const ContentSlide: React.FC<{
  scene: SceneProps;
  slideIndex: number;
  totalSlides: number;
  brandColors: CompositionProps["brand"]["colors"];
}> = ({ scene, slideIndex, totalSlides, brandColors }) => {
  const frame = useCurrentFrame();

  // Slide-left entrance animation for first TRANSITION_FRAMES
  const slideX = interpolate(frame, [0, TRANSITION_FRAMES], [100, 0], {
    extrapolateRight: "clamp",
  });
  const slideOpacity = interpolate(frame, [0, TRANSITION_FRAMES], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        opacity: slideOpacity,
        transform: `translateX(${slideX}%)`,
      }}
    >
      <AbsoluteFill
        style={{
          justifyContent: "center",
          padding: 60,
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 24,
            maxWidth: 960,
            margin: "0 auto",
          }}
        >
          {/* Slide counter */}
          <div
            style={{
              fontSize: 16,
              fontWeight: 600,
              color: brandColors.accent,
              letterSpacing: 3,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            }}
          >
            {slideIndex + 1}/{totalSlides}
          </div>

          {scene.icon && (
            <div style={{ fontSize: 56 }}>{scene.icon}</div>
          )}

          <div
            style={{
              fontSize: 44,
              fontWeight: 700,
              color: brandColors.text,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              lineHeight: 1.3,
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
                lineHeight: 1.6,
                marginTop: 8,
              }}
            >
              {scene.subtext}
            </div>
          )}

          {/* Accent bar */}
          <div
            style={{
              width: 60,
              height: 4,
              backgroundColor: brandColors.accent,
              borderRadius: 2,
              marginTop: 16,
            }}
          />
        </div>
      </AbsoluteFill>
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
              padding: "14px 40px",
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

export const CarouselAnimated: React.FC<CompositionProps> = ({
  brand,
  scenes,
  showProgressBar = true,
  showWatermark = true,
}) => {
  const brandColors = brand.colors;
  const contentScenes = scenes.filter(
    (s) => s.type !== "hook" && s.type !== "cta"
  );
  const totalContentSlides = contentScenes.length;
  const isLightBg =
    brandColors.background.toLowerCase() === "#ffffff" ||
    brandColors.background.toLowerCase() === "#fff";

  let slideIndex = 0;

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom={isLightBg ? "#f8f9fa" : brandColors.background}
        colorTo={isLightBg ? "#ffffff" : `${brandColors.primary}10`}
      />

      {scenes.map((scene, i) => {
        const currentSlideIndex =
          scene.type !== "hook" && scene.type !== "cta" ? slideIndex++ : 0;

        return (
          <Sequence
            key={i}
            from={scene.startFrame}
            durationInFrames={scene.durationFrames}
          >
            {scene.type === "hook" && (
              <CoverScene scene={scene} brandColors={brandColors} />
            )}
            {scene.type !== "hook" && scene.type !== "cta" && (
              <ContentSlide
                scene={scene}
                slideIndex={currentSlideIndex}
                totalSlides={totalContentSlides}
                brandColors={brandColors}
              />
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
        <ProgressBar color={brandColors.accent} position="bottom" height={3} />
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
