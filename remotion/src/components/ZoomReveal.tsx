import React from "react";
import { useCurrentFrame, interpolate, useVideoConfig } from "remotion";

interface ZoomTarget {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface ZoomRevealProps {
  target: ZoomTarget;
  zoomLevel?: number;
  duration?: number;
  highlightBox?: boolean;
  highlightColor?: string;
  children: React.ReactNode;
}

export const ZoomReveal: React.FC<ZoomRevealProps> = ({
  target,
  zoomLevel = 3,
  duration = 40,
  highlightBox = true,
  highlightColor = "#fd79a8",
  children,
}) => {
  const frame = useCurrentFrame();
  const { width: videoWidth, height: videoHeight } = useVideoConfig();

  // Phase boundaries
  const HIGHLIGHT_IN_END = 20;
  const ZOOM_START = 20;
  const ZOOM_END = ZOOM_START + duration;

  // Phase 1 (0–20): highlight box fades in
  const highlightOpacity = interpolate(frame, [0, HIGHLIGHT_IN_END], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Phase 2 (20 → 20+duration): highlight box fades out as zoom begins
  const highlightFadeOut = interpolate(
    frame,
    [ZOOM_START, ZOOM_START + Math.floor(duration * 0.4)],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const highlightFinalOpacity =
    frame < ZOOM_START ? highlightOpacity : highlightOpacity * highlightFadeOut;

  // Zoom progress (0 → 1) during zoom phase
  const zoomProgress = interpolate(frame, [ZOOM_START, ZOOM_END], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (t) => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t, // ease-in-out
  });

  // Current scale
  const scale = interpolate(zoomProgress, [0, 1], [1, zoomLevel]);

  // Target center in content coordinates
  const targetCenterX = target.x + target.width / 2;
  const targetCenterY = target.y + target.height / 2;

  // When zoomed, we want targetCenter to appear at the viewport center.
  // With transformOrigin "top left" and scale S:
  //   rendered position of a point P = P * S + translate
  //   we want: targetCenter * S + translate = videoCenter
  //   => translate = videoCenter - targetCenter * S
  const videoCenterX = videoWidth / 2;
  const videoCenterY = videoHeight / 2;

  const finalTranslateX = videoCenterX - targetCenterX * zoomLevel;
  const finalTranslateY = videoCenterY - targetCenterY * zoomLevel;

  const translateX = interpolate(zoomProgress, [0, 1], [0, finalTranslateX]);
  const translateY = interpolate(zoomProgress, [0, 1], [0, finalTranslateY]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* Zoomable content layer */}
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
          transformOrigin: "top left",
          position: "relative",
        }}
      >
        {children}

        {/* Highlight box drawn on top of children, in content space */}
        {highlightBox && (
          <div
            style={{
              position: "absolute",
              left: target.x,
              top: target.y,
              width: target.width,
              height: target.height,
              border: `3px solid ${highlightColor}`,
              boxShadow: `0 0 0 2px rgba(0,0,0,0.3), 0 0 20px ${highlightColor}80, inset 0 0 20px ${highlightColor}20`,
              borderRadius: 4,
              opacity: highlightFinalOpacity,
              pointerEvents: "none",
              boxSizing: "border-box",
            }}
          />
        )}
      </div>
    </div>
  );
};
