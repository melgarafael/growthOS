import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { AbsoluteFill } from "remotion";

interface BackgroundGradientProps {
  colorFrom?: string;
  colorTo?: string;
  colorMid?: string;
  direction?: number;
  animated?: boolean;
}

export const BackgroundGradient: React.FC<BackgroundGradientProps> = ({
  colorFrom = "#0a0a0a",
  colorTo = "#1a1a2e",
  colorMid,
  direction = 135,
  animated = true,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const angle = animated
    ? interpolate(frame, [0, durationInFrames], [direction, direction + 30], {
        extrapolateRight: "clamp",
      })
    : direction;

  const gradient = colorMid
    ? `linear-gradient(${angle}deg, ${colorFrom}, ${colorMid}, ${colorTo})`
    : `linear-gradient(${angle}deg, ${colorFrom}, ${colorTo})`;

  return (
    <AbsoluteFill
      style={{
        background: gradient,
      }}
    />
  );
};
