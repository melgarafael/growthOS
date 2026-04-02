import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

// ── Types ────────────────────────────────────────────────────────────────────

type CursorAction = "move" | "click" | "hover";

interface CursorPoint {
  x: number;
  y: number;
  action?: CursorAction;
  delay?: number;
}

interface AnimatedCursorProps {
  path: CursorPoint[];
  speed?: number;
  clickEffect?: "ring" | "ripple" | "none";
  cursorStyle?: "arrow" | "pointer" | "text";
  color?: string;
}

// ── SVG Cursors ───────────────────────────────────────────────────────────────

const ArrowCursor: React.FC<{ size?: number }> = ({ size = 28 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 28 28"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <filter id="cursor-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" floodColor="rgba(0,0,0,0.4)" />
    </filter>
    <polygon
      points="4,2 4,22 9,17 13,26 16,25 12,16 19,16"
      fill="white"
      stroke="black"
      strokeWidth="1.5"
      strokeLinejoin="round"
      filter="url(#cursor-shadow)"
    />
  </svg>
);

const PointerCursor: React.FC<{ size?: number }> = ({ size = 28 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 28 28"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <filter id="cursor-shadow-ptr" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" floodColor="rgba(0,0,0,0.4)" />
    </filter>
    <g filter="url(#cursor-shadow-ptr)">
      {/* Palm */}
      <path
        d="M9 13V6.5a1.5 1.5 0 0 1 3 0V12"
        stroke="black"
        strokeWidth="1.5"
        fill="white"
        strokeLinecap="round"
      />
      <path
        d="M12 12V5.5a1.5 1.5 0 0 1 3 0V12"
        stroke="black"
        strokeWidth="1.5"
        fill="white"
        strokeLinecap="round"
      />
      <path
        d="M15 12V7.5a1.5 1.5 0 0 1 3 0V14"
        stroke="black"
        strokeWidth="1.5"
        fill="white"
        strokeLinecap="round"
      />
      {/* Finger base + palm body */}
      <path
        d="M9 13C9 13 7 13 7 15v4a6 6 0 0 0 12 0v-5c0-1.1-.9-2-2-2"
        fill="white"
        stroke="black"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      {/* Index finger outline */}
      <rect
        x="7.5"
        y="5.5"
        width="3"
        height="9"
        rx="1.5"
        fill="white"
        stroke="black"
        strokeWidth="1.2"
      />
    </g>
  </svg>
);

const TextCursor: React.FC<{ size?: number }> = ({ size = 28 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 28 28"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <filter id="cursor-shadow-txt" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" floodColor="rgba(0,0,0,0.5)" />
    </filter>
    <g filter="url(#cursor-shadow-txt)">
      {/* I-beam vertical bar */}
      <line x1="14" y1="4" x2="14" y2="24" stroke="white" strokeWidth="2" strokeLinecap="round" />
      {/* Top serif */}
      <line x1="10" y1="4" x2="18" y2="4" stroke="white" strokeWidth="2" strokeLinecap="round" />
      {/* Bottom serif */}
      <line x1="10" y1="24" x2="18" y2="24" stroke="white" strokeWidth="2" strokeLinecap="round" />
      {/* Outline strokes for legibility */}
      <line x1="14" y1="4" x2="14" y2="24" stroke="black" strokeWidth="3.5" strokeLinecap="round" style={{ mixBlendMode: "normal" }} />
      <line x1="14" y1="4" x2="14" y2="24" stroke="white" strokeWidth="2" strokeLinecap="round" />
      <line x1="10" y1="4" x2="18" y2="4" stroke="black" strokeWidth="3.5" strokeLinecap="round" />
      <line x1="10" y1="4" x2="18" y2="4" stroke="white" strokeWidth="2" strokeLinecap="round" />
      <line x1="10" y1="24" x2="18" y2="24" stroke="black" strokeWidth="3.5" strokeLinecap="round" />
      <line x1="10" y1="24" x2="18" y2="24" stroke="white" strokeWidth="2" strokeLinecap="round" />
    </g>
  </svg>
);

// ── Segment helpers ───────────────────────────────────────────────────────────

interface Segment {
  fromIndex: number;
  toIndex: number;
  startFrame: number;
  endFrame: number;    // excludes delay at the destination
  pauseEnd: number;    // end frame including delay at destination
}

/**
 * Build a timeline of segments from the path array.
 * Each segment = travel from point[i] to point[i+1] + pause at point[i+1].
 */
function buildSegments(path: CursorPoint[], speed: number): Segment[] {
  const segments: Segment[] = [];
  let cursor = 0;

  for (let i = 0; i < path.length - 1; i++) {
    const from = path[i];
    const to = path[i + 1];
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const travelFrames = Math.max(1, Math.round(dist / speed));
    const delayFrames = to.delay ?? 0;

    segments.push({
      fromIndex: i,
      toIndex: i + 1,
      startFrame: cursor,
      endFrame: cursor + travelFrames,
      pauseEnd: cursor + travelFrames + delayFrames,
    });

    cursor += travelFrames + delayFrames;
  }

  return segments;
}

/**
 * Easing: ease-in-out cubic
 */
function easeInOut(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// ── Click / Ring Effect ───────────────────────────────────────────────────────

interface RingEffectProps {
  x: number;
  y: number;
  triggerFrame: number;
  currentFrame: number;
  color: string;
  type: "ring" | "ripple";
}

const ClickEffect: React.FC<RingEffectProps> = ({
  x,
  y,
  triggerFrame,
  currentFrame,
  color,
  type,
}) => {
  const DURATION = 20;
  const elapsed = currentFrame - triggerFrame;

  if (elapsed < 0 || elapsed > DURATION) return null;

  const progress = elapsed / DURATION;

  if (type === "ring") {
    const scale = interpolate(elapsed, [0, DURATION], [0.3, 2.2], {
      extrapolateRight: "clamp",
    });
    const opacity = interpolate(elapsed, [0, DURATION * 0.3, DURATION], [0.9, 0.8, 0], {
      extrapolateRight: "clamp",
    });

    return (
      <div
        style={{
          position: "absolute",
          left: x - 20,
          top: y - 20,
          width: 40,
          height: 40,
          borderRadius: "50%",
          border: `2.5px solid ${color}`,
          transform: `scale(${scale})`,
          opacity,
          pointerEvents: "none",
        }}
      />
    );
  }

  // Ripple: multiple concentric rings
  return (
    <>
      {[0, 6, 12].map((offset, i) => {
        const localElapsed = Math.max(0, elapsed - offset);
        const localProgress = localElapsed / (DURATION - offset);
        const rScale = interpolate(localElapsed, [0, DURATION - offset], [0.2, 2.5], {
          extrapolateRight: "clamp",
        });
        const rOpacity = interpolate(
          localElapsed,
          [0, (DURATION - offset) * 0.4, DURATION - offset],
          [0.7, 0.5, 0],
          { extrapolateRight: "clamp" }
        );

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x - 18,
              top: y - 18,
              width: 36,
              height: 36,
              borderRadius: "50%",
              border: `2px solid ${color}`,
              transform: `scale(${rScale})`,
              opacity: rOpacity,
              pointerEvents: "none",
            }}
          />
        );
      })}
    </>
  );
};

// ── Main Component ────────────────────────────────────────────────────────────

export const AnimatedCursor: React.FC<AnimatedCursorProps> = ({
  path,
  speed = 8,
  clickEffect = "ring",
  cursorStyle = "arrow",
  color = "#fd79a8",
}) => {
  const frame = useCurrentFrame();

  // Need at least 2 points
  if (!path || path.length < 2) {
    const pt = path?.[0];
    if (!pt) return null;
    return (
      <div
        style={{
          position: "absolute",
          left: pt.x,
          top: pt.y,
          pointerEvents: "none",
          zIndex: 50,
          transform: "translate(-4px, -4px)",
        }}
      >
        <ArrowCursor />
      </div>
    );
  }

  const segments = buildSegments(path, speed);
  const totalFrames = segments[segments.length - 1]?.pauseEnd ?? 0;

  // Determine current x, y and which point we're "at"
  let curX = path[0].x;
  let curY = path[0].y;
  let currentPointIndex = 0;

  // Collect all click trigger frames for rendering effects
  const clickTriggers: Array<{ x: number; y: number; frame: number; action: CursorAction }> = [];

  // Mark the start point
  if (path[0].action === "click" || path[0].action === "hover") {
    // Frame 0 trigger
    if (path[0].action === "click") {
      clickTriggers.push({ x: path[0].x, y: path[0].y, frame: 0, action: "click" });
    }
  }

  for (const seg of segments) {
    const pt = path[seg.toIndex];
    if (pt.action === "click") {
      clickTriggers.push({
        x: pt.x,
        y: pt.y,
        frame: seg.endFrame,
        action: "click",
      });
    }
  }

  // Find where we are in the timeline
  const activeSegment = segments.find(
    (seg) => frame >= seg.startFrame && frame < seg.pauseEnd
  );

  if (activeSegment) {
    const { startFrame, endFrame, pauseEnd, fromIndex, toIndex } = activeSegment;
    const from = path[fromIndex];
    const to = path[toIndex];

    if (frame < endFrame) {
      // Travelling between points
      const travelDuration = endFrame - startFrame;
      const t = (frame - startFrame) / travelDuration;
      const easedT = easeInOut(Math.min(1, Math.max(0, t)));
      curX = from.x + (to.x - from.x) * easedT;
      curY = from.y + (to.y - from.y) * easedT;
      currentPointIndex = fromIndex;
    } else {
      // Pausing at destination
      curX = to.x;
      curY = to.y;
      currentPointIndex = toIndex;
    }
  } else if (frame >= totalFrames && segments.length > 0) {
    // Past the end — stay at last point
    const lastPt = path[path.length - 1];
    curX = lastPt.x;
    curY = lastPt.y;
    currentPointIndex = path.length - 1;
  }

  // Determine cursor style: use "hover" points to switch cursor
  const currentAction = path[currentPointIndex]?.action;
  const effectiveCursorStyle =
    currentAction === "hover" ? "pointer" : cursorStyle;

  const CursorSVG =
    effectiveCursorStyle === "pointer"
      ? PointerCursor
      : effectiveCursorStyle === "text"
      ? TextCursor
      : ArrowCursor;

  // Cursor hot-spot offset: arrow tip is at top-left for arrow, top-center for pointer/text
  const offsetX = effectiveCursorStyle === "arrow" ? -4 : -8;
  const offsetY = -4;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        zIndex: 50,
        overflow: "hidden",
      }}
    >
      {/* Click / hover effects */}
      {clickEffect !== "none" &&
        clickTriggers.map((trigger, i) => (
          <ClickEffect
            key={i}
            x={trigger.x}
            y={trigger.y}
            triggerFrame={trigger.frame}
            currentFrame={frame}
            color={color}
            type={clickEffect}
          />
        ))}

      {/* Cursor SVG */}
      <div
        style={{
          position: "absolute",
          left: curX + offsetX,
          top: curY + offsetY,
          filter: "drop-shadow(1px 2px 3px rgba(0,0,0,0.35))",
          pointerEvents: "none",
          willChange: "transform",
        }}
      >
        <CursorSVG size={28} />
      </div>
    </div>
  );
};
