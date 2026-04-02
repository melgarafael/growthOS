import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

interface ProgressBarProps {
  color: string;
  position?: "top" | "bottom";
  height?: number;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  color,
  position = "top",
  height = 4,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, width } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames], [0, width], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        [position]: 0,
        left: 0,
        width,
        height,
        backgroundColor: "rgba(255,255,255,0.15)",
        zIndex: 100,
      }}
    >
      <div
        style={{
          width: progress,
          height: "100%",
          backgroundColor: color,
          borderRadius: position === "top" ? "0 0 2px 0" : "0 2px 0 0",
        }}
      />
    </div>
  );
};
