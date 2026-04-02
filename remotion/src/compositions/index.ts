import { ReelTips } from "./ReelTips";
import { ReelBeforeAfter } from "./ReelBeforeAfter";
import { ReelNumbers } from "./ReelNumbers";
import { ExplainerSteps } from "./ExplainerSteps";
import { ExplainerDemo } from "./ExplainerDemo";
import { CarouselAnimated } from "./CarouselAnimated";
import { ComponentShowcase } from "./ComponentShowcase";
import { TechTerminal } from "./TechTerminal";
import { ProductDemo } from "./ProductDemo";
import { AppWalkthrough } from "./AppWalkthrough";
import { TechTerminalPro } from "./TechTerminalPro";

export interface CompositionEntry {
  id: string;
  component: React.FC<any>;
  width: number;
  height: number;
  fps: number;
  defaultDuration: number; // in seconds
  durationRange: [number, number]; // [min, max] in seconds
  aspectRatio: string;
  category: "reel" | "explainer" | "carousel";
}

export const compositions: CompositionEntry[] = [
  {
    id: "ReelTips",
    component: ReelTips,
    width: 1080,
    height: 1920,
    fps: 30,
    defaultDuration: 30,
    durationRange: [15, 60],
    aspectRatio: "9:16",
    category: "reel",
  },
  {
    id: "ReelBeforeAfter",
    component: ReelBeforeAfter,
    width: 1080,
    height: 1920,
    fps: 30,
    defaultDuration: 20,
    durationRange: [15, 30],
    aspectRatio: "9:16",
    category: "reel",
  },
  {
    id: "ReelNumbers",
    component: ReelNumbers,
    width: 1080,
    height: 1920,
    fps: 30,
    defaultDuration: 20,
    durationRange: [15, 30],
    aspectRatio: "9:16",
    category: "reel",
  },
  {
    id: "ExplainerSteps",
    component: ExplainerSteps,
    width: 1920,
    height: 1080,
    fps: 30,
    defaultDuration: 90,
    durationRange: [60, 180],
    aspectRatio: "16:9",
    category: "explainer",
  },
  {
    id: "ExplainerDemo",
    component: ExplainerDemo,
    width: 1920,
    height: 1080,
    fps: 30,
    defaultDuration: 60,
    durationRange: [30, 120],
    aspectRatio: "16:9",
    category: "explainer",
  },
  {
    id: "CarouselAnimated",
    component: CarouselAnimated,
    width: 1080,
    height: 1350,
    fps: 30,
    defaultDuration: 30,
    durationRange: [15, 60],
    aspectRatio: "4:5",
    category: "carousel",
  },
  {
    id: "ComponentShowcase",
    component: ComponentShowcase as React.FC<any>,
    width: 1080,
    height: 1920,
    fps: 30,
    defaultDuration: 35,
    durationRange: [35, 35] as [number, number],
    aspectRatio: "9:16",
    category: "reel" as const,
  },
  {
    id: "TechTerminal",
    component: TechTerminal as React.FC<any>,
    width: 1080,
    height: 1920,
    fps: 30,
    defaultDuration: 35,
    durationRange: [35, 35] as [number, number],
    aspectRatio: "9:16",
    category: "reel" as const,
  },
  {
    id: "ProductDemo",
    component: ProductDemo as React.FC<any>,
    width: 1920,
    height: 1080,
    fps: 30,
    defaultDuration: 45,
    durationRange: [45, 45] as [number, number],
    aspectRatio: "16:9",
    category: "explainer" as const,
  },
  {
    id: "AppWalkthrough",
    component: AppWalkthrough as React.FC<any>,
    width: 1920,
    height: 1080,
    fps: 30,
    defaultDuration: 50,
    durationRange: [50, 50] as [number, number],
    aspectRatio: "16:9",
    category: "explainer" as const,
  },
  {
    id: "TechTerminalPro",
    component: TechTerminalPro as React.FC<any>,
    width: 1080,
    height: 1920,
    fps: 30,
    defaultDuration: 35,
    durationRange: [25, 45] as [number, number],
    aspectRatio: "9:16",
    category: "reel" as const,
  },
];

export {
  ReelTips,
  ReelBeforeAfter,
  ReelNumbers,
  ExplainerSteps,
  ExplainerDemo,
  CarouselAnimated,
  ComponentShowcase,
  TechTerminal,
  ProductDemo,
  AppWalkthrough,
  TechTerminalPro,
};
