import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

interface ProgressBarProps {
  position?: "top" | "bottom";
  color?: string;
  height?: number;
  backgroundColor?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  position = "top",
  color = "#FFFFFF",
  height = 4,
  backgroundColor = "rgba(255, 255, 255, 0.15)",
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames], [0, 100], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        [position]: 0,
        height,
        backgroundColor,
        zIndex: 100,
      }}
    >
      <div
        style={{
          width: `${progress}%`,
          height: "100%",
          backgroundColor: color,
          borderRadius: position === "top" ? "0 0 2px 0" : "0 2px 0 0",
        }}
      />
    </div>
  );
};
