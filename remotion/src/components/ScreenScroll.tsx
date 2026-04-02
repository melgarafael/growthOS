import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

// ── Types ────────────────────────────────────────────────────────────────────

interface PausePoint {
  position: number;  // Y scroll position (px) at which to pause
  duration: number;  // How many frames to hold at this position
}

interface ScreenScrollProps {
  scrollDistance: number;
  scrollSpeed?: number;
  pausePoints?: PausePoint[];
  easing?: "linear" | "ease-in-out" | "spring";
  children: React.ReactNode;
}

// ── Timeline helpers ─────────────────────────────────────────────────────────

interface ScrollSection {
  fromPos: number;
  toPos: number;
  startFrame: number;
  travelEndFrame: number;  // frame when travel reaches toPos
  pauseEndFrame: number;   // frame after pause duration
}

/**
 * Build a frame timeline from 0 → scrollDistance, accounting for pauses.
 * startDelay: initial hold frames before any scrolling begins.
 */
function buildScrollTimeline(
  scrollDistance: number,
  speed: number,
  pausePoints: PausePoint[],
  startDelay: number
): ScrollSection[] {
  // Sort pause points by position ascending, filter to valid range
  const sorted = [...pausePoints]
    .filter((p) => p.position > 0 && p.position < scrollDistance)
    .sort((a, b) => a.position - b.position);

  // Build waypoints: [0, ...pausePositions, scrollDistance]
  const waypoints = [0, ...sorted.map((p) => p.position), scrollDistance];

  const sections: ScrollSection[] = [];
  let cursor = startDelay;

  for (let i = 0; i < waypoints.length - 1; i++) {
    const fromPos = waypoints[i];
    const toPos = waypoints[i + 1];
    const dist = toPos - fromPos;
    const travelFrames = Math.max(1, Math.round(dist / speed));

    // Is there a pause at toPos?
    const pauseAtDest = sorted.find((p) => p.position === toPos);
    const pauseFrames = pauseAtDest?.duration ?? 0;

    sections.push({
      fromPos,
      toPos,
      startFrame: cursor,
      travelEndFrame: cursor + travelFrames,
      pauseEndFrame: cursor + travelFrames + pauseFrames,
    });

    cursor += travelFrames + pauseFrames;
  }

  return sections;
}

// ── Easing functions ─────────────────────────────────────────────────────────

function easeInOutCubic(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function applyEasing(t: number, easingType: ScreenScrollProps["easing"]): number {
  switch (easingType) {
    case "linear":
      return t;
    case "ease-in-out":
      return easeInOutCubic(t);
    // "spring" is handled specially at call site; fall back to ease-in-out for t-based calc
    default:
      return easeInOutCubic(t);
  }
}

// ── Main component ────────────────────────────────────────────────────────────

const START_DELAY = 15;

export const ScreenScroll: React.FC<ScreenScrollProps> = ({
  scrollDistance,
  scrollSpeed = 2,
  pausePoints = [],
  easing = "ease-in-out",
  children,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  // Available scroll time: total frames minus start delay
  const availableFrames = durationInFrames - START_DELAY;

  // Determine scroll progress in pixels
  let scrollProgress = 0;

  if (pausePoints.length === 0) {
    // ── Simple path: no pauses ─────────────────────────────────────────────
    if (frame < START_DELAY) {
      scrollProgress = 0;
    } else {
      const scrollFrame = frame - START_DELAY;

      if (easing === "spring") {
        // Spring-based scroll: use spring value mapped to scrollDistance
        // We drive a "virtual" spring that settles at 1 over the available frames
        const springVal = spring({
          frame: scrollFrame,
          fps,
          config: {
            damping: 18,
            stiffness: 60,
            mass: 1.2,
          },
          durationInFrames: availableFrames,
        });
        scrollProgress = Math.min(scrollDistance, springVal * scrollDistance);
      } else {
        // Interpolate with chosen easing
        const t = Math.min(1, scrollFrame / availableFrames);
        const easedT = applyEasing(t, easing);
        scrollProgress = easedT * scrollDistance;
      }
    }
  } else {
    // ── Complex path: pause points ─────────────────────────────────────────
    const sections = buildScrollTimeline(
      scrollDistance,
      scrollSpeed,
      pausePoints,
      START_DELAY
    );

    if (sections.length === 0) {
      scrollProgress = 0;
    } else {
      const lastSection = sections[sections.length - 1];
      const totalTimeline = lastSection.pauseEndFrame;

      if (frame <= START_DELAY) {
        scrollProgress = 0;
      } else if (frame >= totalTimeline) {
        scrollProgress = scrollDistance;
      } else {
        // Find the active section
        const active = sections.find(
          (sec) => frame >= sec.startFrame && frame < sec.pauseEndFrame
        );

        if (active) {
          if (frame < active.travelEndFrame) {
            // Travelling
            const travelDuration = active.travelEndFrame - active.startFrame;
            const t = Math.max(0, Math.min(1, (frame - active.startFrame) / travelDuration));
            const easedT = applyEasing(t, easing === "spring" ? "ease-in-out" : easing);
            scrollProgress = active.fromPos + (active.toPos - active.fromPos) * easedT;
          } else {
            // Pausing
            scrollProgress = active.toPos;
          }
        }
      }
    }
  }

  // Clamp to valid range
  const clampedProgress = Math.max(0, Math.min(scrollDistance, scrollProgress));

  return (
    <div
      style={{
        position: "relative",
        overflow: "hidden",
        width: "100%",
        height: "100%",
      }}
    >
      <div
        style={{
          transform: `translateY(${-clampedProgress}px)`,
          willChange: "transform",
          position: "relative",
        }}
      >
        {children}
      </div>
    </div>
  );
};
