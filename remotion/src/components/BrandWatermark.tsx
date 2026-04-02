import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface BrandWatermarkProps {
  handle: string;
  position?: "bottom-right" | "bottom-left" | "top-right";
  color?: string;
  fontSize?: number;
}

export const BrandWatermark: React.FC<BrandWatermarkProps> = ({
  handle,
  position = "bottom-right",
  color = "rgba(255, 255, 255, 0.6)",
  fontSize = 20,
}) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  const positionStyles: React.CSSProperties = {};
  switch (position) {
    case "bottom-right":
      positionStyles.bottom = 40;
      positionStyles.right = 40;
      break;
    case "bottom-left":
      positionStyles.bottom = 40;
      positionStyles.left = 40;
      break;
    case "top-right":
      positionStyles.top = 40;
      positionStyles.right = 40;
      break;
  }

  return (
    <div
      style={{
        position: "absolute",
        opacity,
        color,
        fontSize,
        fontWeight: 500,
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        zIndex: 90,
        ...positionStyles,
      }}
    >
      {handle}
    </div>
  );
};
