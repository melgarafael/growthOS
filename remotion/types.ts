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
}

export interface SceneProps {
  type: "hook" | "point" | "cta" | "transition";
  startFrame: number;
  durationFrames: number;
  text: string;
  subtext?: string;
  icon?: string;
  animation: "fade-in" | "fade-out" | "slide-left" | "slide-right" | "slide-up" | "scale-in" | "bounce" | "typewriter" | "counter-up" | "wipe";
  transition?: "crossfade" | "wipe" | "cut" | "slide";
  style?: Record<string, unknown>;
}

export interface CompositionProps {
  brand: BrandProps;
  scenes: SceneProps[];
  showProgressBar: boolean;
  showWatermark: boolean;
}
