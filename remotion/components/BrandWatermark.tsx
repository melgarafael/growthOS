import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface BrandWatermarkProps {
  handle: string;
  color: string;
  position?: "bottom-right" | "bottom-left" | "top-right";
  opacity?: number;
}

export const BrandWatermark: React.FC<BrandWatermarkProps> = ({
  handle,
  color,
  position = "bottom-right",
  opacity = 0.4,
}) => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 30], [0, opacity], {
    extrapolateRight: "clamp",
  });

  const positionStyle: React.CSSProperties = {
    position: "absolute",
    zIndex: 50,
    ...(position === "bottom-right" && { bottom: 120, right: 40 }),
    ...(position === "bottom-left" && { bottom: 120, left: 40 }),
    ...(position === "top-right" && { top: 40, right: 40 }),
  };

  return (
    <div
      style={{
        ...positionStyle,
        opacity: fadeIn,
        color,
        fontSize: 20,
        fontFamily: "SF Pro Display, Inter, system-ui, sans-serif",
        fontWeight: 600,
        letterSpacing: 0.5,
      }}
    >
      {handle}
    </div>
  );
};
