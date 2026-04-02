import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

type TransitionType = "crossfade" | "wipe" | "cut" | "slide";

interface TransitionWipeProps {
  type: TransitionType;
  durationFrames?: number;
  direction?: "left" | "right" | "up" | "down";
  children: React.ReactNode;
}

export const TransitionWipe: React.FC<TransitionWipeProps> = ({
  type,
  durationFrames = 15,
  direction = "left",
  children,
}) => {
  const frame = useCurrentFrame();

  let opacity = 1;
  let translateX = 0;
  let translateY = 0;
  let clipPath = "none";

  switch (type) {
    case "crossfade":
      opacity = interpolate(frame, [0, durationFrames], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "wipe": {
      const progress = interpolate(frame, [0, durationFrames], [0, 100], {
        extrapolateRight: "clamp",
      });
      switch (direction) {
        case "left":
          clipPath = `inset(0 ${100 - progress}% 0 0)`;
          break;
        case "right":
          clipPath = `inset(0 0 0 ${100 - progress}%)`;
          break;
        case "up":
          clipPath = `inset(0 0 ${100 - progress}% 0)`;
          break;
        case "down":
          clipPath = `inset(${100 - progress}% 0 0 0)`;
          break;
      }
      break;
    }

    case "slide":
      switch (direction) {
        case "left":
          translateX = interpolate(frame, [0, durationFrames], [100, 0], {
            extrapolateRight: "clamp",
          });
          break;
        case "right":
          translateX = interpolate(frame, [0, durationFrames], [-100, 0], {
            extrapolateRight: "clamp",
          });
          break;
        case "up":
          translateY = interpolate(frame, [0, durationFrames], [100, 0], {
            extrapolateRight: "clamp",
          });
          break;
        case "down":
          translateY = interpolate(frame, [0, durationFrames], [-100, 0], {
            extrapolateRight: "clamp",
          });
          break;
      }
      opacity = interpolate(frame, [0, Math.floor(durationFrames / 2)], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;

    case "cut":
      break;
  }

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        opacity,
        transform: `translate(${translateX}%, ${translateY}%)`,
        clipPath,
      }}
    >
      {children}
    </div>
  );
};
