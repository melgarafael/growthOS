import React from "react";

// ── Scene & Brand interfaces ──

export type AnimationType =
  | "fade-in"
  | "fade-out"
  | "slide-left"
  | "slide-right"
  | "slide-up"
  | "scale-in"
  | "bounce"
  | "typewriter"
  | "counter-up"
  | "wipe";

export type TransitionType = "crossfade" | "wipe" | "cut" | "slide";

export type SceneType =
  | "hook"
  | "point"
  | "comparison"
  | "number"
  | "step"
  | "demo"
  | "cta";

export type WatermarkPosition = "bottom-right" | "bottom-left" | "top-right";

export interface SceneProps {
  type: SceneType;
  startFrame: number;
  durationFrames: number;
  text: string;
  subtext?: string;
  icon?: string;
  animation: AnimationType;
  transition?: TransitionType;
}

export interface BrandColors {
  primary: string;
  secondary: string;
  background: string;
  text: string;
  accent: string;
}

export interface BrandProps {
  name: string;
  handle: string;
  colors: BrandColors;
  watermark_position: WatermarkPosition;
}

export interface CompositionProps {
  brand: BrandProps;
  scenes: SceneProps[];
  showProgressBar?: boolean;
  showWatermark?: boolean;
}

// ── Per-composition props ──

export interface ReelTipsProps extends CompositionProps {
  /** Tips reel: hook -> points -> CTA */
}

export interface ReelBeforeAfterProps extends CompositionProps {
  /** Before/after comparison reel */
}

export interface ReelNumbersProps extends CompositionProps {
  /** Animated statistics reel; number scenes carry targetValue */
}

export interface ExplainerStepsProps extends CompositionProps {
  /** Step-by-step tutorial (16:9) */
}

export interface ExplainerDemoProps extends CompositionProps {
  /** Product demo showcase (16:9) */
}

export interface CarouselAnimatedProps extends CompositionProps {
  /** Animated carousel slides (4:5) */
}

// ── Component-level props ──

export interface AnimatedTextProps {
  text: string;
  animation: AnimationType;
  delay?: number;
  color?: string;
  fontSize?: number;
}

export interface ProgressBarProps {
  position?: "top" | "bottom";
  color?: string;
  height?: number;
}

export interface BrandWatermarkProps {
  handle: string;
  position?: WatermarkPosition;
  color?: string;
  fontSize?: number;
}

export interface TransitionWipeProps {
  type: TransitionType;
  progress: number; // 0-1
}

export interface BackgroundGradientProps {
  colors: string[];
}

export interface CounterUpProps {
  target: number;
  prefix?: string;
  suffix?: string;
  color?: string;
  fontSize?: number;
}

// ── Wave 2: New Component Props ──

export interface BrowserFrameProps {
  url: string;
  title?: string;
  browser?: "chrome" | "safari" | "arc";
  darkMode?: boolean;
  shadow?: boolean;
  scale?: number;
  rounded?: boolean;
  children: React.ReactNode;
}

export interface MobileFrameProps {
  device?: "iphone15" | "iphone-se" | "pixel8" | "generic";
  orientation?: "portrait" | "landscape";
  darkMode?: boolean;
  scale?: number;
  children: React.ReactNode;
}

export interface CursorPoint {
  x: number;
  y: number;
  action?: "move" | "click" | "hover";
  delay?: number;
}

export interface AnimatedCursorProps {
  path: CursorPoint[];
  speed?: number;
  clickEffect?: "ring" | "ripple" | "none";
  cursorStyle?: "arrow" | "pointer" | "text";
  color?: string;
}

export interface ScreenScrollProps {
  scrollDistance: number;
  scrollSpeed?: number;
  pausePoints?: Array<{ position: number; duration: number }>;
  easing?: "linear" | "ease-in-out" | "spring";
  children: React.ReactNode;
}

export interface TerminalCommand {
  text: string;
  type: "input" | "output" | "spinner" | "success" | "error" | "blank";
  color?: string;
  delay?: number;
  typeSpeed?: number;
}

export interface TerminalEmulatorProps {
  commands: TerminalCommand[];
  theme?: "dark" | "light";
  prompt?: string;
  title?: string;
  fontSize?: number;
}

export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

export interface ChartAnimatedProps {
  type: "bar" | "line" | "donut";
  data: ChartDataPoint[];
  animationStyle?: "grow" | "draw" | "reveal";
  showLabels?: boolean;
  showValues?: boolean;
  highlightIndex?: number;
  duration?: number;
}

export interface GlassmorphismCardProps {
  blur?: number;
  opacity?: number;
  borderColor?: string;
  rounded?: number;
  animateIn?: "fade" | "scale" | "slide-up" | "none";
  children: React.ReactNode;
}

export interface ZoomRevealProps {
  target: { x: number; y: number; width: number; height: number };
  zoomLevel?: number;
  duration?: number;
  highlightBox?: boolean;
  highlightColor?: string;
  children: React.ReactNode;
}

export interface ScreenshotOverlayProps {
  src: string;
  animation?: "fade-in" | "scale-in" | "slide-up" | "none";
  fit?: "contain" | "cover" | "fill";
  rounded?: number;
  shadow?: boolean;
}

// ── Wave 3: Showcase Composition Props ──

export interface ProductDemoScene {
  type: "hook" | "device-intro" | "navigate" | "scroll" | "zoom" | "cta";
  duration: number;
  text?: string;
  subtext?: string;
  screenshot?: string;
  device?: "browser" | "mobile";
  cursorPath?: CursorPoint[];
  scrollDistance?: number;
  zoomTarget?: { x: number; y: number; width: number; height: number };
  animation?: AnimationType;
}

export interface ProductDemoProps {
  brand: BrandProps;
  scenes: ProductDemoScene[];
  deviceType?: "browser" | "mobile";
  deviceConfig?: { browser?: "chrome" | "safari" | "arc"; device?: "iphone15" | "pixel8"; darkMode?: boolean };
  showProgressBar?: boolean;
  showWatermark?: boolean;
}

export interface TechTerminalScene {
  type: "hook" | "terminal" | "output-highlight" | "cta";
  duration: number;
  text?: string;
  subtext?: string;
  commands?: TerminalCommand[];
  animation?: AnimationType;
}

export interface TechTerminalProps {
  brand: BrandProps;
  scenes: TechTerminalScene[];
  terminalTitle?: string;
  terminalTheme?: "dark" | "light";
  showProgressBar?: boolean;
  showWatermark?: boolean;
}

export interface WalkthroughStep {
  screenName: string;
  screenshot: string;
  actions: Array<{
    type: "click" | "scroll" | "hover" | "type";
    target: { x: number; y: number };
    tooltip?: string;
    duration?: number;
  }>;
}

export interface AppWalkthroughScene {
  type: "hook" | "step" | "transition" | "cta";
  duration: number;
  text?: string;
  subtext?: string;
  step?: WalkthroughStep;
  animation?: AnimationType;
}

export interface AppWalkthroughProps {
  brand: BrandProps;
  scenes: AppWalkthroughScene[];
  deviceType?: "browser" | "mobile";
  deviceConfig?: { browser?: "chrome" | "safari" | "arc"; device?: "iphone15" | "pixel8"; darkMode?: boolean };
  showProgressBar?: boolean;
  showWatermark?: boolean;
}
