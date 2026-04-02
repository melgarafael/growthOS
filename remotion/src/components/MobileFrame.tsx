import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

type DeviceName = "iphone15" | "iphone-se" | "pixel8" | "generic";
type Orientation = "portrait" | "landscape";
type NotchType = "dynamic-island" | "none" | "punch-hole" | "notch";

interface DeviceSpec {
  width: number;
  height: number;
  notch: NotchType;
  cornerRadius: number;
  bezelWidth: number;
  statusBarHeight: number;
  homeIndicator: boolean;
  label: string;
}

const DEVICE_SPECS: Record<DeviceName, DeviceSpec> = {
  iphone15: {
    width: 390,
    height: 844,
    notch: "dynamic-island",
    cornerRadius: 47,
    bezelWidth: 12,
    statusBarHeight: 54,
    homeIndicator: true,
    label: "iPhone 15",
  },
  "iphone-se": {
    width: 375,
    height: 667,
    notch: "none",
    cornerRadius: 20,
    bezelWidth: 20,
    statusBarHeight: 20,
    homeIndicator: false,
    label: "iPhone SE",
  },
  pixel8: {
    width: 412,
    height: 892,
    notch: "punch-hole",
    cornerRadius: 28,
    bezelWidth: 10,
    statusBarHeight: 40,
    homeIndicator: false,
    label: "Pixel 8",
  },
  generic: {
    width: 360,
    height: 780,
    notch: "notch",
    cornerRadius: 30,
    bezelWidth: 14,
    statusBarHeight: 38,
    homeIndicator: false,
    label: "Android",
  },
};

interface MobileFrameProps {
  device?: DeviceName;
  orientation?: Orientation;
  darkMode?: boolean;
  scale?: number;
  children?: React.ReactNode;
}

// Dynamic Island pill
const DynamicIsland: React.FC<{ darkMode: boolean }> = ({ darkMode }) => (
  <div
    style={{
      position: "absolute",
      top: 12,
      left: "50%",
      transform: "translateX(-50%)",
      width: 120,
      height: 34,
      background: "#000",
      borderRadius: 20,
      zIndex: 10,
      boxShadow: darkMode
        ? "0 0 0 1px rgba(255,255,255,0.06)"
        : "0 0 0 1px rgba(0,0,0,0.12)",
    }}
  />
);

// Traditional notch
const Notch: React.FC = () => (
  <div
    style={{
      position: "absolute",
      top: 0,
      left: "50%",
      transform: "translateX(-50%)",
      width: 150,
      height: 28,
      background: "#000",
      borderRadius: "0 0 20px 20px",
      zIndex: 10,
    }}
  />
);

// Punch-hole camera
const PunchHole: React.FC<{ darkMode: boolean }> = ({ darkMode }) => (
  <div
    style={{
      position: "absolute",
      top: 12,
      left: "50%",
      transform: "translateX(-50%)",
      width: 12,
      height: 12,
      background: "#000",
      borderRadius: "50%",
      zIndex: 10,
      boxShadow: darkMode
        ? "0 0 0 1px rgba(255,255,255,0.08)"
        : "0 0 0 1px rgba(0,0,0,0.15)",
    }}
  />
);

// Home indicator bar (iPhone gesture bar)
const HomeIndicator: React.FC<{ darkMode: boolean }> = ({ darkMode }) => (
  <div
    style={{
      position: "absolute",
      bottom: 8,
      left: "50%",
      transform: "translateX(-50%)",
      width: 130,
      height: 5,
      background: darkMode ? "rgba(255,255,255,0.35)" : "rgba(0,0,0,0.2)",
      borderRadius: 3,
      zIndex: 10,
    }}
  />
);

// Physical side buttons
const SideButtons: React.FC<{
  deviceWidth: number;
  deviceHeight: number;
  bezel: number;
  darkMode: boolean;
  spec: DeviceSpec;
}> = ({ deviceWidth, deviceHeight, bezel, darkMode, spec }) => {
  const buttonColor = darkMode ? "#2a2a2a" : "#d0d0d0";
  const buttonHighlight = darkMode ? "#3a3a3a" : "#e8e8e8";

  const totalW = deviceWidth + bezel * 2;
  const totalH = deviceHeight + bezel * 2;

  const isIphone = spec.notch === "dynamic-island" || spec.notch === "none";

  return (
    <>
      {/* Power / lock button — right side */}
      <div
        style={{
          position: "absolute",
          right: -4,
          top: totalH * 0.3,
          width: 4,
          height: isIphone ? 70 : 60,
          background: buttonColor,
          borderRadius: "0 3px 3px 0",
          boxShadow: `1px 0 0 ${buttonHighlight}`,
        }}
      />

      {/* Volume up — left side */}
      <div
        style={{
          position: "absolute",
          left: -4,
          top: totalH * 0.25,
          width: 4,
          height: isIphone ? 40 : 48,
          background: buttonColor,
          borderRadius: "3px 0 0 3px",
          boxShadow: `-1px 0 0 ${buttonHighlight}`,
        }}
      />

      {/* Volume down — left side */}
      <div
        style={{
          position: "absolute",
          left: -4,
          top: totalH * 0.25 + (isIphone ? 54 : 62),
          width: 4,
          height: isIphone ? 40 : 48,
          background: buttonColor,
          borderRadius: "3px 0 0 3px",
          boxShadow: `-1px 0 0 ${buttonHighlight}`,
        }}
      />

      {/* Silent toggle (iPhone only) */}
      {isIphone && (
        <div
          style={{
            position: "absolute",
            left: -4,
            top: totalH * 0.18,
            width: 4,
            height: 22,
            background: buttonColor,
            borderRadius: "3px 0 0 3px",
            boxShadow: `-1px 0 0 ${buttonHighlight}`,
          }}
        />
      )}
    </>
  );
};

export const MobileFrame: React.FC<MobileFrameProps> = ({
  device = "iphone15",
  orientation = "portrait",
  darkMode = true,
  scale = 1,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entranceSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120, mass: 1 },
  });

  const scaleValue = (0.85 + entranceSpring * 0.15) * scale;
  const opacity = Math.min(1, entranceSpring * 2);

  const spec = DEVICE_SPECS[device];
  const isLandscape = orientation === "landscape";

  // In landscape, swap dimensions
  const screenW = isLandscape ? spec.height : spec.width;
  const screenH = isLandscape ? spec.width : spec.height;
  const bezel = spec.bezelWidth;

  // Total device dimensions
  const deviceW = screenW + bezel * 2;
  const deviceH = screenH + bezel * 2;

  // In landscape, bottom bezel gets extra for finger grip
  const bottomBezel = isLandscape ? bezel : bezel * 2.5;
  const topBezel = isLandscape ? bezel : bezel * 2;
  const totalW = screenW + bezel * 2;
  const totalH = screenH + topBezel + bottomBezel;

  // Theme
  const bezelBg = darkMode
    ? "linear-gradient(145deg, #2a2a2a 0%, #1a1a1a 60%, #0f0f0f 100%)"
    : "linear-gradient(145deg, #e8e8e8 0%, #d0d0d0 60%, #bfbfbf 100%)";
  const bezelBorder = darkMode ? "#444" : "#aaa";
  const screenBg = darkMode ? "#0a0a0a" : "#ffffff";
  const gloss = darkMode
    ? "linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 50%)"
    : "linear-gradient(135deg, rgba(255,255,255,0.5) 0%, transparent 50%)";

  const cornerRadius = isLandscape ? spec.cornerRadius * 0.75 : spec.cornerRadius;
  const innerRadius = Math.max(4, cornerRadius - bezel);

  return (
    <div
      style={{
        transform: `scale(${scaleValue})`,
        opacity,
        transformOrigin: "center center",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100%",
      }}
    >
      {/* Device body */}
      <div
        style={{
          position: "relative",
          width: totalW,
          height: totalH,
          background: bezelBg,
          borderRadius: cornerRadius,
          border: `1px solid ${bezelBorder}`,
          boxShadow: darkMode
            ? "0 40px 100px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.08)"
            : "0 40px 100px rgba(0,0,0,0.3), 0 10px 30px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.6)",
          flexShrink: 0,
        }}
      >
        {/* Side buttons */}
        <SideButtons
          deviceWidth={screenW}
          deviceHeight={screenH}
          bezel={bezel}
          darkMode={darkMode}
          spec={spec}
        />

        {/* Screen area */}
        <div
          style={{
            position: "absolute",
            top: topBezel,
            left: bezel,
            width: screenW,
            height: screenH,
            background: screenBg,
            borderRadius: innerRadius,
            overflow: "hidden",
          }}
        >
          {/* Notch / camera cutout */}
          {!isLandscape && spec.notch === "dynamic-island" && (
            <DynamicIsland darkMode={darkMode} />
          )}
          {!isLandscape && spec.notch === "notch" && <Notch />}
          {!isLandscape && spec.notch === "punch-hole" && (
            <PunchHole darkMode={darkMode} />
          )}

          {/* Content */}
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              overflow: "hidden",
            }}
          >
            {children}
          </div>

          {/* Home indicator */}
          {!isLandscape && spec.homeIndicator && (
            <HomeIndicator darkMode={darkMode} />
          )}
        </div>

        {/* Glossy reflection overlay */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: cornerRadius,
            background: gloss,
            pointerEvents: "none",
          }}
        />

        {/* Speaker notch (top, portrait only) — decorative */}
        {!isLandscape && spec.notch === "none" && (
          <div
            style={{
              position: "absolute",
              top: topBezel * 0.4,
              left: "50%",
              transform: "translateX(-50%)",
              width: 50,
              height: 6,
              background: darkMode ? "#111" : "#ccc",
              borderRadius: 3,
            }}
          />
        )}

        {/* Bottom home button (iphone-se style) */}
        {!isLandscape && !spec.homeIndicator && spec.notch === "none" && (
          <div
            style={{
              position: "absolute",
              bottom: bottomBezel * 0.3,
              left: "50%",
              transform: "translateX(-50%)",
              width: 36,
              height: 36,
              borderRadius: "50%",
              border: `2px solid ${darkMode ? "#444" : "#aaa"}`,
              background: darkMode ? "#1a1a1a" : "#ddd",
              boxShadow: darkMode
                ? "inset 0 1px 2px rgba(0,0,0,0.6), 0 1px 0 rgba(255,255,255,0.05)"
                : "inset 0 1px 2px rgba(0,0,0,0.15), 0 1px 0 rgba(255,255,255,0.8)",
            }}
          />
        )}
      </div>
    </div>
  );
};
