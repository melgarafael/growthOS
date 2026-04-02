import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

type AnimationType =
  | "fade-in"
  | "fade-out"
  | "slide-left"
  | "slide-right"
  | "slide-up"
  | "scale-in"
  | "bounce"
  | "typewriter";

interface AnimatedTextProps {
  text: string;
  animation: AnimationType;
  delay?: number;
  fontSize?: number;
  color?: string;
  fontWeight?: number;
  textAlign?: React.CSSProperties["textAlign"];
  style?: React.CSSProperties;
}

export const AnimatedText: React.FC<AnimatedTextProps> = ({
  text,
  animation,
  delay = 0,
  fontSize = 48,
  color = "#FFFFFF",
  fontWeight = 700,
  textAlign = "center",
  style = {},
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const adjustedFrame = Math.max(0, frame - delay);

  let opacity = 1;
  let translateX = 0;
  let translateY = 0;
  let scale = 1;
  let displayText = text;

  switch (animation) {
    case "fade-in":
      opacity = interpolate(adjustedFrame, [0, 15], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "fade-out":
      opacity = interpolate(adjustedFrame, [0, 15], [1, 0], {
        extrapolateRight: "clamp",
      });
      break;

    case "slide-left":
      translateX = interpolate(adjustedFrame, [0, 20], [300, 0], {
        extrapolateRight: "clamp",
      });
      opacity = interpolate(adjustedFrame, [0, 10], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "slide-right":
      translateX = interpolate(adjustedFrame, [0, 20], [-300, 0], {
        extrapolateRight: "clamp",
      });
      opacity = interpolate(adjustedFrame, [0, 10], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "slide-up":
      translateY = interpolate(adjustedFrame, [0, 20], [200, 0], {
        extrapolateRight: "clamp",
      });
      opacity = interpolate(adjustedFrame, [0, 10], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "scale-in": {
      const scaleSpring = spring({
        frame: adjustedFrame,
        fps,
        config: { damping: 12, stiffness: 100 },
      });
      scale = interpolate(scaleSpring, [0, 1], [0.3, 1]);
      opacity = interpolate(adjustedFrame, [0, 8], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    }

    case "bounce": {
      const bounceSpring = spring({
        frame: adjustedFrame,
        fps,
        config: { damping: 8, stiffness: 150, mass: 0.8 },
      });
      scale = interpolate(bounceSpring, [0, 1], [0, 1]);
      opacity = interpolate(adjustedFrame, [0, 5], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    }

    case "typewriter": {
      const charsToShow = Math.floor(
        interpolate(adjustedFrame, [0, text.length * 2], [0, text.length], {
          extrapolateRight: "clamp",
        })
      );
      displayText = text.slice(0, charsToShow);
      break;
    }
  }

  return (
    <div
      style={{
        opacity,
        transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
        fontSize,
        color,
        fontWeight,
        textAlign,
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        lineHeight: 1.3,
        ...style,
      }}
    >
      {displayText}
    </div>
  );
};
