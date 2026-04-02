import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface CounterUpProps {
  target: number;
  durationFrames?: number;
  delay?: number;
  prefix?: string;
  suffix?: string;
  fontSize?: number;
  color?: string;
  decimals?: number;
  fontWeight?: number;
}

export const CounterUp: React.FC<CounterUpProps> = ({
  target,
  durationFrames = 60,
  delay = 0,
  prefix = "",
  suffix = "",
  fontSize = 96,
  color = "#FFFFFF",
  decimals = 0,
  fontWeight = 800,
}) => {
  const frame = useCurrentFrame();
  const adjustedFrame = Math.max(0, frame - delay);

  const progress = interpolate(adjustedFrame, [0, durationFrames], [0, 1], {
    extrapolateRight: "clamp",
  });
  const eased = 1 - Math.pow(1 - progress, 3);
  const value = eased * target;

  const displayValue =
    decimals > 0 ? value.toFixed(decimals) : Math.floor(value).toString();

  const opacity = interpolate(adjustedFrame, [0, 8], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        opacity,
        fontSize,
        color,
        fontWeight,
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        textAlign: "center",
        fontVariantNumeric: "tabular-nums",
      }}
    >
      {prefix}
      {displayValue}
      {suffix}
    </div>
  );
};
