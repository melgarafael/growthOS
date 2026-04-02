import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig, Img, staticFile } from "remotion";

type AnimationType = "fade-in" | "scale-in" | "slide-up" | "none";
type FitType = "contain" | "cover" | "fill";

interface ScreenshotOverlayProps {
  src: string;
  animation?: AnimationType;
  fit?: FitType;
  rounded?: number;
  shadow?: boolean;
}

export const ScreenshotOverlay: React.FC<ScreenshotOverlayProps> = ({
  src,
  animation = "fade-in",
  fit = "cover",
  rounded = 0,
  shadow = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Resolve image source — remote URLs used as-is, local paths via staticFile()
  const resolvedSrc = src.startsWith("http") ? src : staticFile(src);

  // Animation values
  let opacity = 1;
  let scale = 1;
  let translateY = 0;

  switch (animation) {
    case "fade-in":
      opacity = interpolate(frame, [0, 20], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "scale-in": {
      const scaleSpring = spring({
        frame,
        fps,
        config: { damping: 14, stiffness: 120, mass: 1 },
        from: 0,
        to: 1,
      });
      scale = interpolate(scaleSpring, [0, 1], [0.9, 1]);
      opacity = interpolate(frame, [0, 15], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    }

    case "slide-up":
      translateY = interpolate(frame, [0, 25], [30, 0], {
        extrapolateRight: "clamp",
      });
      opacity = interpolate(frame, [0, 20], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "none":
    default:
      break;
  }

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
        borderRadius: rounded,
        opacity,
        transform: `scale(${scale}) translateY(${translateY}px)`,
        boxShadow: shadow ? "0 8px 32px rgba(0,0,0,0.3)" : "none",
        position: "relative",
      }}
    >
      <Img
        src={resolvedSrc}
        style={{
          width: "100%",
          height: "100%",
          objectFit: fit,
          display: "block",
        }}
      />
    </div>
  );
};
