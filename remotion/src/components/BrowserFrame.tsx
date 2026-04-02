import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

type BrowserType = "chrome" | "safari" | "arc";

interface BrowserFrameProps {
  url: string;
  title?: string;
  browser?: BrowserType;
  darkMode?: boolean;
  shadow?: boolean;
  scale?: number;
  rounded?: boolean;
  children?: React.ReactNode;
}

const CHROME_ICON = (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
    <circle cx="12" cy="12" r="4" fill="currentColor" />
    <line x1="12" y1="2" x2="12" y2="8" stroke="currentColor" strokeWidth="2" />
    <line x1="21" y1="17" x2="15.5" y2="14" stroke="currentColor" strokeWidth="2" />
    <line x1="3" y1="17" x2="8.5" y2="14" stroke="currentColor" strokeWidth="2" />
  </svg>
);

const SAFARI_ICON = (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
    <polygon points="16,8 8,12 12,16 20,12" fill="currentColor" opacity="0.7" />
    <line x1="8" y1="16" x2="16" y2="8" stroke="currentColor" strokeWidth="1.5" />
  </svg>
);

const ARC_ICON = (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
    <path
      d="M12 3C7 3 3 7 3 12s4 9 9 9 9-4 9-9-4-9-9-9z"
      stroke="currentColor"
      strokeWidth="2"
      fill="none"
    />
    <path d="M12 7v5l3 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

const LOCK_ICON = (
  <svg
    width="10"
    height="11"
    viewBox="0 0 10 11"
    fill="none"
    style={{ flexShrink: 0 }}
  >
    <rect x="1.5" y="4.5" width="7" height="5.5" rx="1" fill="currentColor" opacity="0.7" />
    <path
      d="M3 4.5V3.2A2 2 0 0 1 7 3.2v1.3"
      stroke="currentColor"
      strokeWidth="1.3"
      strokeLinecap="round"
      fill="none"
    />
  </svg>
);

export const BrowserFrame: React.FC<BrowserFrameProps> = ({
  url,
  title,
  browser = "chrome",
  darkMode = true,
  shadow = true,
  scale = 1,
  rounded = true,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entranceSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120, mass: 1 },
  });

  const scaleValue = 0.85 + entranceSpring * 0.15 * scale;
  const opacity = Math.min(1, entranceSpring * 2);

  // Theme colors
  const chrome = darkMode
    ? { bg: "#1e1e1e", toolbar: "#2d2d2d", border: "#3d3d3d", text: "#c8c8c8", urlBg: "#3a3a3a", urlText: "#d0d0d0", iconColor: "#888" }
    : { bg: "#f0f0f0", toolbar: "#e0e0e0", border: "#c8c8c8", text: "#333", urlBg: "#fff", urlText: "#555", iconColor: "#888" };

  const browserIcon =
    browser === "safari" ? SAFARI_ICON : browser === "arc" ? ARC_ICON : CHROME_ICON;

  const TOOLBAR_HEIGHT = 44;
  const BORDER_RADIUS = rounded ? 12 : 4;

  return (
    <div
      style={{
        transform: `scale(${scaleValue})`,
        opacity,
        transformOrigin: "center center",
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          borderRadius: BORDER_RADIUS,
          overflow: "hidden",
          border: `1px solid ${chrome.border}`,
          display: "flex",
          flexDirection: "column",
          boxShadow: shadow
            ? darkMode
              ? "0 32px 80px rgba(0,0,0,0.7), 0 8px 24px rgba(0,0,0,0.5)"
              : "0 32px 80px rgba(0,0,0,0.25), 0 8px 24px rgba(0,0,0,0.12)"
            : "none",
        }}
      >
        {/* Chrome / Toolbar */}
        <div
          style={{
            height: TOOLBAR_HEIGHT,
            minHeight: TOOLBAR_HEIGHT,
            background: chrome.toolbar,
            display: "flex",
            alignItems: "center",
            padding: "0 14px",
            gap: 10,
            flexShrink: 0,
            borderBottom: `1px solid ${chrome.border}`,
          }}
        >
          {/* Traffic lights */}
          <div style={{ display: "flex", alignItems: "center", gap: 7, flexShrink: 0 }}>
            <div
              style={{
                width: 12,
                height: 12,
                borderRadius: "50%",
                background: "#ff5f57",
                boxShadow: "0 0 0 0.5px rgba(0,0,0,0.3)",
              }}
            />
            <div
              style={{
                width: 12,
                height: 12,
                borderRadius: "50%",
                background: "#ffbd2e",
                boxShadow: "0 0 0 0.5px rgba(0,0,0,0.3)",
              }}
            />
            <div
              style={{
                width: 12,
                height: 12,
                borderRadius: "50%",
                background: "#28c840",
                boxShadow: "0 0 0 0.5px rgba(0,0,0,0.3)",
              }}
            />
          </div>

          {/* Browser icon */}
          <div
            style={{
              color: chrome.iconColor,
              display: "flex",
              alignItems: "center",
              flexShrink: 0,
            }}
          >
            {browserIcon}
          </div>

          {/* URL Bar */}
          <div
            style={{
              flex: 1,
              background: chrome.urlBg,
              borderRadius: 8,
              height: 28,
              display: "flex",
              alignItems: "center",
              padding: "0 10px",
              gap: 6,
              overflow: "hidden",
              border: `1px solid ${chrome.border}`,
            }}
          >
            <div style={{ color: chrome.iconColor, display: "flex", alignItems: "center" }}>
              {LOCK_ICON}
            </div>
            <span
              style={{
                fontSize: 12,
                color: chrome.urlText,
                fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                flex: 1,
                userSelect: "none",
              }}
            >
              {url}
            </span>
          </div>

          {/* Title (optional) */}
          {title && (
            <span
              style={{
                fontSize: 12,
                color: chrome.text,
                fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                opacity: 0.7,
                flexShrink: 0,
                maxWidth: 120,
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
            >
              {title}
            </span>
          )}
        </div>

        {/* Viewport / Content area */}
        <div
          style={{
            flex: 1,
            background: darkMode ? "#141414" : "#ffffff",
            overflow: "hidden",
            position: "relative",
          }}
        >
          {children}
        </div>
      </div>
    </div>
  );
};
