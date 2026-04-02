import React from "react";
import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

interface GlassmorphismCardProps {
  blur?: number;
  opacity?: number;
  borderColor?: string;
  rounded?: number;
  animateIn?: "fade" | "scale" | "slide-up" | "none";
  children: React.ReactNode;
}

export const GlassmorphismCard: React.FC<GlassmorphismCardProps> = ({
  blur = 10,
  opacity = 0.1,
  borderColor = "rgba(255,255,255,0.2)",
  rounded = 16,
  animateIn = "scale",
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  let cardOpacity = 1;
  let scale = 1;
  let translateY = 0;

  switch (animateIn) {
    case "fade": {
      cardOpacity = interpolate(frame, [0, 20], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    }

    case "scale": {
      const scaleSpring = spring({
        frame,
        fps,
        config: { damping: 14, stiffness: 120, mass: 0.8 },
      });
      scale = interpolate(scaleSpring, [0, 1], [0.8, 1]);
      cardOpacity = interpolate(frame, [0, 12], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    }

    case "slide-up": {
      translateY = interpolate(frame, [0, 24], [40, 0], {
        extrapolateRight: "clamp",
      });
      cardOpacity = interpolate(frame, [0, 18], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    }

    case "none":
    default:
      break;
  }

  return (
    <div
      style={{
        background: `rgba(255,255,255,${opacity})`,
        backdropFilter: `blur(${blur}px)`,
        WebkitBackdropFilter: `blur(${blur}px)`,
        border: `1px solid ${borderColor}`,
        borderRadius: rounded,
        boxShadow: "0 8px 32px rgba(0,0,0,0.2)",
        padding: 24,
        opacity: cardOpacity,
        transform: `scale(${scale}) translateY(${translateY}px)`,
      }}
    >
      {children}
    </div>
  );
};
