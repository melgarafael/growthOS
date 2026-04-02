import React from "react";
import {
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";

interface AnimatedTextProps {
  text: string;
  animation: string;
  delay?: number;
  style?: React.CSSProperties;
}

export const AnimatedText: React.FC<AnimatedTextProps> = ({
  text,
  animation,
  delay = 0,
  style = {},
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const adjustedFrame = Math.max(0, frame - delay);

  let animStyle: React.CSSProperties = {};

  switch (animation) {
    case "fade-in":
      animStyle = {
        opacity: interpolate(adjustedFrame, [0, 15], [0, 1], {
          extrapolateRight: "clamp",
        }),
      };
      break;
    case "fade-out":
      animStyle = {
        opacity: interpolate(adjustedFrame, [0, 15], [1, 0], {
          extrapolateRight: "clamp",
        }),
      };
      break;
    case "slide-left":
      animStyle = {
        transform: `translateX(${interpolate(adjustedFrame, [0, 20], [width * 0.3, 0], { extrapolateRight: "clamp" })}px)`,
        opacity: interpolate(adjustedFrame, [0, 10], [0, 1], {
          extrapolateRight: "clamp",
        }),
      };
      break;
    case "slide-right":
      animStyle = {
        transform: `translateX(${interpolate(adjustedFrame, [0, 20], [-width * 0.3, 0], { extrapolateRight: "clamp" })}px)`,
        opacity: interpolate(adjustedFrame, [0, 10], [0, 1], {
          extrapolateRight: "clamp",
        }),
      };
      break;
    case "slide-up":
      animStyle = {
        transform: `translateY(${interpolate(adjustedFrame, [0, 20], [height * 0.2, 0], { extrapolateRight: "clamp" })}px)`,
        opacity: interpolate(adjustedFrame, [0, 10], [0, 1], {
          extrapolateRight: "clamp",
        }),
      };
      break;
    case "scale-in": {
      const scale = spring({
        frame: adjustedFrame,
        fps,
        config: { damping: 12, stiffness: 150 },
      });
      animStyle = {
        transform: `scale(${interpolate(scale, [0, 1], [0.5, 1])})`,
        opacity: interpolate(adjustedFrame, [0, 8], [0, 1], {
          extrapolateRight: "clamp",
        }),
      };
      break;
    }
    case "bounce": {
      const bounce = spring({
        frame: adjustedFrame,
        fps,
        config: { damping: 8, stiffness: 100 },
      });
      animStyle = {
        transform: `scale(${interpolate(bounce, [0, 1], [0.3, 1])})`,
        opacity: interpolate(adjustedFrame, [0, 5], [0, 1], {
          extrapolateRight: "clamp",
        }),
      };
      break;
    }
    case "typewriter":
      animStyle = { opacity: 1 };
      break;
    default:
      animStyle = { opacity: 1 };
  }

  const displayText =
    animation === "typewriter"
      ? text.slice(0, Math.floor(adjustedFrame / 2))
      : text;

  return (
    <div style={{ ...animStyle, ...style }}>
      {displayText}
    </div>
  );
};
