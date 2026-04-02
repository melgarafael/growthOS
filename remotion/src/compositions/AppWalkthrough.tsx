import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
  AbsoluteFill,
} from "remotion";
import { AnimatedText } from "../components/AnimatedText";
import { AnimatedCursor } from "../components/AnimatedCursor";
import { BrowserFrame } from "../components/BrowserFrame";
import { ScreenScroll } from "../components/ScreenScroll";
import { BackgroundGradient } from "../components/BackgroundGradient";
import { ProgressBar } from "../components/ProgressBar";
import { BrandWatermark } from "../components/BrandWatermark";

// ── Design tokens ─────────────────────────────────────────────────────────────
const COLORS = {
  bg: "#0a0a0a",
  sidebar: "#111827",
  card: "#1a1a2e",
  cardBorder: "#2d2d4e",
  accent: "#6c5ce7",
  accentHover: "#7d6ff0",
  accentLight: "#a29bfe",
  teal: "#00cec9",
  pink: "#fd79a8",
  textPrimary: "#ffffff",
  textSecondary: "#9ca3af",
  textMuted: "#6b7280",
  green: "#00b894",
  orange: "#fdcb6e",
  red: "#e17055",
};

const FONT =
  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';

// ── Inline Tooltip ─────────────────────────────────────────────────────────────
const InlineTooltip: React.FC<{
  x: number;
  y: number;
  text: string;
  visible: boolean;
}> = ({ x, y, text, visible }) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 8], visible ? [0, 1] : [1, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: "translate(-50%, -100%)",
        opacity,
        pointerEvents: "none",
        zIndex: 60,
      }}
    >
      {/* Tooltip box */}
      <div
        style={{
          background: "rgba(15, 15, 30, 0.95)",
          backdropFilter: "blur(8px)",
          border: `1px solid ${COLORS.accent}60`,
          borderRadius: 8,
          padding: "8px 14px",
          whiteSpace: "nowrap",
          boxShadow: `0 4px 20px rgba(108, 92, 231, 0.3)`,
        }}
      >
        <span
          style={{
            fontSize: 13,
            fontFamily: FONT,
            color: COLORS.textPrimary,
            fontWeight: 500,
          }}
        >
          {text}
        </span>
      </div>
      {/* Arrow pointing down */}
      <div
        style={{
          position: "absolute",
          bottom: -7,
          left: "50%",
          transform: "translateX(-50%)",
          width: 0,
          height: 0,
          borderLeft: "7px solid transparent",
          borderRight: "7px solid transparent",
          borderTop: `7px solid rgba(108, 92, 231, 0.6)`,
        }}
      />
    </div>
  );
};

// ── Inline Hotspot ─────────────────────────────────────────────────────────────
const InlineHotspot: React.FC<{
  x: number;
  y: number;
  color: string;
  visible: boolean;
}> = ({ x, y, color, visible }) => {
  const frame = useCurrentFrame();

  const pulseScale = 1 + Math.sin(frame * 0.15) * 0.25;
  const pulseOpacity = 0.4 + Math.sin(frame * 0.15) * 0.2;
  const opacity = interpolate(frame, [0, 6], visible ? [0, 1] : [1, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: "translate(-50%, -50%)",
        opacity,
        pointerEvents: "none",
        zIndex: 45,
      }}
    >
      {/* Outer pulsing ring */}
      <div
        style={{
          position: "absolute",
          width: 32,
          height: 32,
          borderRadius: "50%",
          border: `2px solid ${color}`,
          opacity: pulseOpacity,
          transform: `scale(${pulseScale}) translate(-50%, -50%)`,
          left: 0,
          top: 0,
        }}
      />
      {/* Inner solid dot */}
      <div
        style={{
          position: "absolute",
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: color,
          transform: "translate(-50%, -50%)",
          left: 0,
          top: 0,
          boxShadow: `0 0 10px ${color}`,
        }}
      />
    </div>
  );
};

// ── Mock Sidebar ──────────────────────────────────────────────────────────────
const AppSidebar: React.FC<{ activeItem?: string }> = ({
  activeItem = "Dashboard",
}) => {
  const menuItems = [
    { icon: "🏠", label: "Dashboard" },
    { icon: "📊", label: "Pipeline" },
    { icon: "👥", label: "Contatos" },
    { icon: "🔀", label: "Funis" },
    { icon: "📈", label: "Relatórios" },
    { icon: "⚙️", label: "Config" },
  ];

  return (
    <div
      style={{
        width: 200,
        minWidth: 200,
        height: "100%",
        background: COLORS.sidebar,
        borderRight: `1px solid ${COLORS.cardBorder}`,
        display: "flex",
        flexDirection: "column",
        padding: "20px 0",
        flexShrink: 0,
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: "0 20px 24px",
          borderBottom: `1px solid ${COLORS.cardBorder}`,
          marginBottom: 12,
        }}
      >
        <div
          style={{
            fontSize: 18,
            fontWeight: 800,
            fontFamily: FONT,
            color: COLORS.textPrimary,
            letterSpacing: "-0.5px",
          }}
        >
          Tomi<span style={{ color: COLORS.accent }}>KOS</span>
        </div>
        <div
          style={{
            fontSize: 10,
            color: COLORS.textMuted,
            fontFamily: FONT,
            marginTop: 2,
          }}
        >
          Growth Platform
        </div>
      </div>

      {/* Menu items */}
      {menuItems.map((item) => {
        const isActive = item.label === activeItem;
        return (
          <div
            key={item.label}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              padding: "10px 20px",
              margin: "1px 8px",
              borderRadius: 8,
              background: isActive ? `${COLORS.accent}20` : "transparent",
              borderLeft: isActive
                ? `3px solid ${COLORS.accent}`
                : "3px solid transparent",
              cursor: "pointer",
            }}
          >
            <span style={{ fontSize: 14 }}>{item.icon}</span>
            <span
              style={{
                fontSize: 13,
                fontFamily: FONT,
                color: isActive ? COLORS.textPrimary : COLORS.textSecondary,
                fontWeight: isActive ? 600 : 400,
              }}
            >
              {item.label}
            </span>
          </div>
        );
      })}

      {/* User avatar at bottom */}
      <div style={{ marginTop: "auto", padding: "0 20px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "12px",
            background: `${COLORS.cardBorder}50`,
            borderRadius: 10,
          }}
        >
          <div
            style={{
              width: 30,
              height: 30,
              borderRadius: "50%",
              background: `linear-gradient(135deg, ${COLORS.accent}, ${COLORS.pink})`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 14,
              fontWeight: 700,
              color: "#fff",
              fontFamily: FONT,
            }}
          >
            R
          </div>
          <div>
            <div
              style={{
                fontSize: 12,
                fontFamily: FONT,
                color: COLORS.textPrimary,
                fontWeight: 600,
              }}
            >
              Rafael M.
            </div>
            <div
              style={{ fontSize: 10, fontFamily: FONT, color: COLORS.textMuted }}
            >
              Admin
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ── Scene 1: Hook ─────────────────────────────────────────────────────────────
const HookScene: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 20,
      }}
    >
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#1a0a2e"
        colorMid="#0d1a2e"
        direction={135}
        animated
      />

      {/* Decorative grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(108, 92, 231, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(108, 92, 231, 0.04) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />

      <div
        style={{
          position: "relative",
          zIndex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
        }}
      >
        {/* Step badge */}
        <div
          style={{
            background: `${COLORS.accent}20`,
            border: `1px solid ${COLORS.accent}40`,
            borderRadius: 20,
            padding: "6px 18px",
          }}
        >
          <AnimatedText
            text="Tutorial Passo a Passo"
            animation="fade-in"
            fontSize={13}
            color={COLORS.accentLight}
            fontWeight={600}
          />
        </div>

        <AnimatedText
          text="Como configurar"
          animation="scale-in"
          delay={8}
          fontSize={72}
          color={COLORS.textPrimary}
          fontWeight={800}
          style={{ textAlign: "center", lineHeight: 1.1 }}
        />
        <AnimatedText
          text="seu primeiro funil"
          animation="scale-in"
          delay={14}
          fontSize={72}
          color={COLORS.textPrimary}
          fontWeight={800}
          style={{ textAlign: "center", lineHeight: 1.1 }}
        />

        <AnimatedText
          text="Passo a passo no TomiKOS"
          animation="fade-in"
          delay={24}
          fontSize={26}
          color={COLORS.teal}
          fontWeight={500}
          style={{ textAlign: "center", marginTop: 8 }}
        />
      </div>

      <ProgressBar color={COLORS.accent} height={3} />
    </AbsoluteFill>
  );
};

// ── Scene 2: Dashboard ─────────────────────────────────────────────────────────
const DashboardScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Show button-pressed state after frame 200, transition at 220
  const buttonPressed = frame >= 200;
  const afterClick = frame >= 230;

  const tooltipVisible = frame >= 220 && frame < 360;
  const hotspotVisible = frame < 220;

  // Cursor path: starts center, moves to "+ Novo Funil" button
  // Button is roughly at x=740, y=170 in the content area (after sidebar 200px + some offset)
  // The BrowserFrame has a toolbar ~44px, so content starts after that
  // Within the 1920x1080 frame: browser content area width = 1920px
  // Sidebar = 200px, main area starts at 200px
  // "+ Novo Funil" button is in the main area, let's say at x=760, y=170 in the absolute frame
  const cursorPath = [
    { x: 960, y: 540, action: "move" as const, delay: 20 },
    { x: 760, y: 185, action: "hover" as const, delay: 40 },
    { x: 760, y: 185, action: "click" as const, delay: 90 },
  ];

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#0d0d1a"
        direction={180}
        animated={false}
      />

      <div
        style={{
          position: "absolute",
          inset: 60,
          zIndex: 1,
        }}
      >
        <BrowserFrame url="tomikos.app/dashboard" darkMode browser="chrome">
          <div style={{ display: "flex", height: "100%" }}>
            <AppSidebar activeItem="Dashboard" />

            {/* Main content */}
            <div
              style={{
                flex: 1,
                background: COLORS.bg,
                padding: "28px 36px",
                overflowY: "auto",
              }}
            >
              {/* Header */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  marginBottom: 28,
                }}
              >
                <div>
                  <h1
                    style={{
                      fontSize: 22,
                      fontWeight: 700,
                      color: COLORS.textPrimary,
                      fontFamily: FONT,
                      margin: 0,
                    }}
                  >
                    Meus Funis
                  </h1>
                  <p
                    style={{
                      fontSize: 13,
                      color: COLORS.textMuted,
                      fontFamily: FONT,
                      margin: "4px 0 0",
                    }}
                  >
                    3 funis ativos
                  </p>
                </div>

                {/* "+ Novo Funil" button — this is the hotspot target */}
                <div style={{ position: "relative" }}>
                  <button
                    style={{
                      background: buttonPressed
                        ? COLORS.accentHover
                        : COLORS.accent,
                      color: "#fff",
                      border: "none",
                      borderRadius: 10,
                      padding: "10px 20px",
                      fontSize: 14,
                      fontWeight: 600,
                      fontFamily: FONT,
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: 6,
                      transform: buttonPressed ? "scale(0.97)" : "scale(1)",
                      boxShadow: buttonPressed
                        ? "none"
                        : `0 4px 14px ${COLORS.accent}50`,
                      transition: "all 0.1s",
                    }}
                  >
                    ＋ Novo Funil
                  </button>
                </div>
              </div>

              {/* Stats row */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(4, 1fr)",
                  gap: 16,
                  marginBottom: 28,
                }}
              >
                {[
                  {
                    label: "Total de Leads",
                    value: "127",
                    icon: "👥",
                    color: COLORS.teal,
                  },
                  {
                    label: "Deals Ativos",
                    value: "34",
                    icon: "🔥",
                    color: COLORS.orange,
                  },
                  {
                    label: "Receita Potencial",
                    value: "R$ 248k",
                    icon: "💰",
                    color: COLORS.green,
                  },
                  {
                    label: "Taxa de Conv.",
                    value: "26.8%",
                    icon: "📈",
                    color: COLORS.accentLight,
                  },
                ].map((stat) => (
                    <div
                      key={stat.label}
                      style={{
                        background: COLORS.card,
                        border: `1px solid ${COLORS.cardBorder}`,
                        borderRadius: 12,
                        padding: "16px 20px",
                      }}
                    >
                      <div
                        style={{
                          fontSize: 22,
                          marginBottom: 6,
                        }}
                      >
                        {stat.icon}
                      </div>
                      <div
                        style={{
                          fontSize: 22,
                          fontWeight: 700,
                          color: stat.color,
                          fontFamily: FONT,
                          lineHeight: 1,
                        }}
                      >
                        {stat.value}
                      </div>
                      <div
                        style={{
                          fontSize: 11,
                          color: COLORS.textMuted,
                          fontFamily: FONT,
                          marginTop: 4,
                        }}
                      >
                        {stat.label}
                      </div>
                    </div>
                ))}
              </div>

              {/* Funnel cards */}
              {[
                {
                  name: "Vendas Q2 2024",
                  leads: 47,
                  conv: "31%",
                  color: COLORS.accent,
                },
                {
                  name: "Onboarding B2B",
                  leads: 28,
                  conv: "18%",
                  color: COLORS.teal,
                },
                {
                  name: "Renovações",
                  leads: 52,
                  conv: "42%",
                  color: COLORS.green,
                },
              ].map((funnel, i) => (
                <div
                  key={funnel.name}
                  style={{
                    background: COLORS.card,
                    border: `1px solid ${COLORS.cardBorder}`,
                    borderRadius: 10,
                    padding: "14px 20px",
                    marginBottom: 10,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <div
                      style={{
                        width: 10,
                        height: 10,
                        borderRadius: "50%",
                        background: funnel.color,
                        boxShadow: `0 0 8px ${funnel.color}`,
                      }}
                    />
                    <span
                      style={{
                        fontSize: 14,
                        fontFamily: FONT,
                        color: COLORS.textPrimary,
                        fontWeight: 600,
                      }}
                    >
                      {funnel.name}
                    </span>
                  </div>
                  <div
                    style={{
                      display: "flex",
                      gap: 24,
                      alignItems: "center",
                    }}
                  >
                    <span
                      style={{
                        fontSize: 12,
                        fontFamily: FONT,
                        color: COLORS.textSecondary,
                      }}
                    >
                      {funnel.leads} leads
                    </span>
                    <span
                      style={{
                        fontSize: 12,
                        fontFamily: FONT,
                        color: funnel.color,
                        fontWeight: 600,
                      }}
                    >
                      {funnel.conv} conv.
                    </span>
                    <div
                      style={{
                        background: `${funnel.color}20`,
                        border: `1px solid ${funnel.color}40`,
                        borderRadius: 6,
                        padding: "4px 10px",
                        fontSize: 11,
                        fontFamily: FONT,
                        color: funnel.color,
                        fontWeight: 600,
                      }}
                    >
                      Ativo
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </BrowserFrame>
      </div>

      {/* Hotspot overlay on the "+ Novo Funil" button */}
      {/* The button is inside the BrowserFrame at absolute position */}
      {/* BrowserFrame starts at inset:60, toolbar=44px, sidebar=200px */}
      {/* Button is in header area at roughly x=760 from main content left */}
      {/* Absolute position: left = 60 + 200 + (1920-60-60-200)*0.82 ≈ 60+200+1312 = ~1350, top = 60+44+42 = ~150 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          zIndex: 10,
        }}
      >
        <InlineHotspot
          x={1370}
          y={188}
          color={COLORS.accent}
          visible={hotspotVisible}
        />
        <InlineTooltip
          x={1370}
          y={165}
          text="Clique para criar um novo funil"
          visible={tooltipVisible}
        />
      </div>

      {/* Animated cursor */}
      <div
        style={{ position: "absolute", inset: 0, pointerEvents: "none", zIndex: 20 }}
      >
        <AnimatedCursor
          path={[
            { x: 960, y: 540, action: "move", delay: 20 },
            { x: 1370, y: 188, action: "hover", delay: 40 },
            { x: 1370, y: 188, action: "click", delay: 90 },
          ]}
          speed={6}
          clickEffect="ripple"
          color={COLORS.accent}
        />
      </div>

      <ProgressBar color={COLORS.accent} height={3} />
    </AbsoluteFill>
  );
};

// ── Scene 3: Transition ────────────────────────────────────────────────────────
const TransitionScene: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, 15, 45, 60],
    [0, 1, 1, 0],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        background: COLORS.bg,
        flexDirection: "column",
        gap: 16,
      }}
    >
      <div style={{ opacity }}>
        <div
          style={{
            width: 48,
            height: 48,
            borderRadius: "50%",
            border: `3px solid ${COLORS.accent}`,
            borderTopColor: "transparent",
            animation: "spin 1s linear infinite",
            margin: "0 auto 20px",
          }}
        />
        <div
          style={{
            fontSize: 24,
            fontFamily: FONT,
            color: "#888",
            textAlign: "center",
          }}
        >
          {text}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── Pipeline Stage Component ───────────────────────────────────────────────────
const PipelineStage: React.FC<{
  label: string;
  count?: number;
  color: string;
  isNew?: boolean;
}> = ({ label, count = 0, color, isNew = false }) => {
  const frame = useCurrentFrame();
  const slideIn = isNew
    ? interpolate(frame, [0, 20], [40, 0], { extrapolateRight: "clamp" })
    : 0;
  const fadeIn = isNew
    ? interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" })
    : 1;

  return (
    <div
      style={{
        transform: `translateX(${slideIn}px)`,
        opacity: fadeIn,
      }}
    >
      <div
        style={{
          background: COLORS.card,
          border: `1px solid ${isNew ? color : COLORS.cardBorder}`,
          borderTop: `3px solid ${color}`,
          borderRadius: 10,
          padding: "16px 20px",
          minWidth: 140,
          boxShadow: isNew ? `0 0 20px ${color}30` : "none",
        }}
      >
        <div
          style={{
            fontSize: 12,
            fontFamily: FONT,
            color: COLORS.textMuted,
            marginBottom: 8,
            textTransform: "uppercase",
            letterSpacing: "0.5px",
          }}
        >
          {label}
        </div>
        <div
          style={{
            fontSize: 26,
            fontWeight: 700,
            color: color,
            fontFamily: FONT,
          }}
        >
          {count}
        </div>
        <div
          style={{
            fontSize: 11,
            color: COLORS.textMuted,
            fontFamily: FONT,
            marginTop: 4,
          }}
        >
          leads
        </div>
      </div>
    </div>
  );
};

// ── Scene 4: Funnel Editor ─────────────────────────────────────────────────────
const FunnelEditorScene: React.FC = () => {
  const frame = useCurrentFrame();

  const clickedAddBtn = frame >= 180;
  const newStageVisible = frame >= 200;
  const hotspotVisible = frame < 180;
  const tooltipVisible = frame >= 155 && frame < 360;

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#0d0d1a"
        direction={180}
        animated={false}
      />

      <div style={{ position: "absolute", inset: 60, zIndex: 1 }}>
        <BrowserFrame url="tomikos.app/funis/novo" darkMode browser="chrome">
          <div style={{ display: "flex", height: "100%" }}>
            <AppSidebar activeItem="Funis" />

            {/* Main content */}
            <div
              style={{
                flex: 1,
                background: COLORS.bg,
                padding: "28px 36px",
                overflowY: "auto",
              }}
            >
              {/* Header */}
              <div style={{ marginBottom: 32 }}>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                    marginBottom: 8,
                  }}
                >
                  <span
                    style={{
                      fontSize: 11,
                      fontFamily: FONT,
                      color: COLORS.textMuted,
                    }}
                  >
                    Funis /
                  </span>
                  <span
                    style={{
                      fontSize: 11,
                      fontFamily: FONT,
                      color: COLORS.accentLight,
                    }}
                  >
                    Novo Funil
                  </span>
                </div>
                <h1
                  style={{
                    fontSize: 22,
                    fontWeight: 700,
                    color: COLORS.textPrimary,
                    fontFamily: FONT,
                    margin: 0,
                  }}
                >
                  Editor de Funil
                </h1>
              </div>

              {/* Pipeline visualization */}
              <div style={{ marginBottom: 28 }}>
                <div
                  style={{
                    fontSize: 13,
                    fontFamily: FONT,
                    color: COLORS.textSecondary,
                    marginBottom: 16,
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: "0.5px",
                  }}
                >
                  Etapas do Funil
                </div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 0,
                    flexWrap: "nowrap",
                    overflowX: "auto",
                    paddingBottom: 8,
                  }}
                >
                  {[
                    { label: "Prospecção", count: 18, color: COLORS.teal },
                    { label: "Qualificação", count: 11, color: COLORS.orange },
                    { label: "Fechamento", count: 5, color: COLORS.green },
                  ].map((stage, i) => (
                    <React.Fragment key={stage.label}>
                      <PipelineStage
                        label={stage.label}
                        count={stage.count}
                        color={stage.color}
                      />
                      <div
                        style={{
                          width: 32,
                          height: 2,
                          background: `linear-gradient(90deg, ${stage.color}60, ${COLORS.cardBorder})`,
                          flexShrink: 0,
                        }}
                      />
                    </React.Fragment>
                  ))}

                  {/* New stage appears after click */}
                  {newStageVisible && (
                    <PipelineStage
                      label="Pós-venda"
                      count={0}
                      color={COLORS.pink}
                      isNew
                    />
                  )}
                </div>
              </div>

              {/* Settings row */}
              <div
                style={{
                  background: COLORS.card,
                  border: `1px solid ${COLORS.cardBorder}`,
                  borderRadius: 10,
                  padding: "16px 20px",
                  marginBottom: 20,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: 13,
                      fontFamily: FONT,
                      color: COLORS.textPrimary,
                      fontWeight: 600,
                    }}
                  >
                    Nome do Funil
                  </div>
                  <div
                    style={{
                      fontSize: 12,
                      fontFamily: FONT,
                      color: COLORS.textMuted,
                    }}
                  >
                    Vendas Q3 2024
                  </div>
                </div>
                <div
                  style={{
                    background: `${COLORS.green}20`,
                    border: `1px solid ${COLORS.green}40`,
                    borderRadius: 6,
                    padding: "4px 12px",
                    fontSize: 11,
                    fontFamily: FONT,
                    color: COLORS.green,
                    fontWeight: 600,
                  }}
                >
                  Ativo
                </div>
              </div>

              {/* Add Stage button */}
              <div style={{ position: "relative", display: "inline-block" }}>
                <button
                  style={{
                    background: clickedAddBtn
                      ? `${COLORS.accent}30`
                      : "transparent",
                    color: COLORS.accent,
                    border: `2px dashed ${COLORS.accent}60`,
                    borderRadius: 10,
                    padding: "12px 24px",
                    fontSize: 14,
                    fontWeight: 600,
                    fontFamily: FONT,
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    transform: clickedAddBtn ? "scale(0.97)" : "scale(1)",
                  }}
                >
                  ＋ Adicionar Etapa
                </button>
              </div>
            </div>
          </div>
        </BrowserFrame>
      </div>

      {/* Hotspot + Tooltip overlays */}
      {/* "＋ Adicionar Etapa" button is in lower-left of main content */}
      {/* Absolute: left ≈ 60 + 200 + 36 + ~80 = ~376, top ≈ 60 + 44 + 28 + 32 + 180 + 60 + 60 = ~464 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          zIndex: 10,
        }}
      >
        <InlineHotspot
          x={460}
          y={710}
          color={COLORS.accent}
          visible={hotspotVisible}
        />
        <InlineTooltip
          x={460}
          y={695}
          text="Defina as etapas do seu funil"
          visible={tooltipVisible}
        />
      </div>

      {/* Animated cursor */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          zIndex: 20,
        }}
      >
        <AnimatedCursor
          path={[
            { x: 960, y: 540, action: "move", delay: 20 },
            { x: 460, y: 710, action: "hover", delay: 50 },
            { x: 460, y: 710, action: "click", delay: 60 },
          ]}
          speed={6}
          clickEffect="ripple"
          color={COLORS.accent}
        />
      </div>

      <ProgressBar color={COLORS.accent} height={3} />
    </AbsoluteFill>
  );
};

// ── Lead Card Component ───────────────────────────────────────────────────────
const LeadCard: React.FC<{
  name: string;
  company: string;
  value: string;
  stage: string;
  stageColor: string;
  avatar: string;
  isHighlighted?: boolean;
}> = ({ name, company, value, stage, stageColor, avatar, isHighlighted }) => {
  return (
    <div
      style={{
        background: isHighlighted
          ? `${COLORS.accent}10`
          : COLORS.card,
        border: `1px solid ${isHighlighted ? COLORS.accent : COLORS.cardBorder}`,
        borderRadius: 10,
        padding: "14px 18px",
        marginBottom: 10,
        display: "flex",
        alignItems: "center",
        gap: 14,
        boxShadow: isHighlighted ? `0 0 16px ${COLORS.accent}20` : "none",
        transition: "all 0.2s",
      }}
    >
      <div
        style={{
          width: 36,
          height: 36,
          borderRadius: "50%",
          background: `linear-gradient(135deg, ${stageColor}60, ${stageColor}30)`,
          border: `1px solid ${stageColor}40`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 16,
          flexShrink: 0,
        }}
      >
        {avatar}
      </div>
      <div style={{ flex: 1 }}>
        <div
          style={{
            fontSize: 14,
            fontFamily: FONT,
            color: COLORS.textPrimary,
            fontWeight: 600,
          }}
        >
          {name}
        </div>
        <div
          style={{
            fontSize: 12,
            fontFamily: FONT,
            color: COLORS.textMuted,
          }}
        >
          {company}
        </div>
      </div>
      <div
        style={{
          background: `${stageColor}15`,
          border: `1px solid ${stageColor}30`,
          borderRadius: 6,
          padding: "4px 10px",
          fontSize: 11,
          fontFamily: FONT,
          color: stageColor,
          fontWeight: 600,
        }}
      >
        {stage}
      </div>
      <div
        style={{
          fontSize: 15,
          fontWeight: 700,
          color: COLORS.green,
          fontFamily: FONT,
          minWidth: 70,
          textAlign: "right",
        }}
      >
        {value}
      </div>
    </div>
  );
};

// ── Scene 6: Active Funnel ────────────────────────────────────────────────────
const ActiveFunnelScene: React.FC = () => {
  const frame = useCurrentFrame();
  const highlightedCard = frame >= 150;
  const tooltipVisible = frame >= 160;

  const leads = [
    {
      name: "Ana Souza",
      company: "TechBR Ltda.",
      value: "R$ 12k",
      stage: "Qualificação",
      stageColor: COLORS.orange,
      avatar: "👩‍💼",
    },
    {
      name: "Carlos Lima",
      company: "Inova Digital",
      value: "R$ 8.5k",
      stage: "Prospecção",
      stageColor: COLORS.teal,
      avatar: "👨‍💻",
    },
    {
      name: "Mariana Rocha",
      company: "StartupX",
      value: "R$ 22k",
      stage: "Fechamento",
      stageColor: COLORS.green,
      avatar: "👩‍🚀",
    },
    {
      name: "Pedro Alves",
      company: "Grupo Alfa",
      value: "R$ 6k",
      stage: "Prospecção",
      stageColor: COLORS.teal,
      avatar: "👨‍💼",
    },
    {
      name: "Julia Ferreira",
      company: "NextLevel Co.",
      value: "R$ 15.5k",
      stage: "Qualificação",
      stageColor: COLORS.orange,
      avatar: "👩‍🎨",
    },
    {
      name: "Ricardo Neves",
      company: "CloudSoft",
      value: "R$ 31k",
      stage: "Fechamento",
      stageColor: COLORS.green,
      avatar: "🧑‍💻",
    },
    {
      name: "Beatriz Santos",
      company: "Vendas Pro",
      value: "R$ 9.2k",
      stage: "Qualificação",
      stageColor: COLORS.orange,
      avatar: "👩‍📊",
    },
  ];

  return (
    <AbsoluteFill>
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#0d0d1a"
        direction={180}
        animated={false}
      />

      <div style={{ position: "absolute", inset: 60, zIndex: 1 }}>
        <BrowserFrame
          url="tomikos.app/funis/vendas-q2"
          darkMode
          browser="chrome"
        >
          <div style={{ display: "flex", height: "100%" }}>
            <AppSidebar activeItem="Funis" />

            {/* Main content with scroll */}
            <div
              style={{
                flex: 1,
                background: COLORS.bg,
                overflow: "hidden",
                position: "relative",
              }}
            >
              <ScreenScroll
                scrollDistance={300}
                scrollSpeed={2}
                easing="ease-in-out"
              >
                <div style={{ padding: "28px 36px", minHeight: "150%" }}>
                  {/* Header */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      marginBottom: 24,
                    }}
                  >
                    <div>
                      <h1
                        style={{
                          fontSize: 22,
                          fontWeight: 700,
                          color: COLORS.textPrimary,
                          fontFamily: FONT,
                          margin: 0,
                        }}
                      >
                        Funil: Vendas Q2
                      </h1>
                      <p
                        style={{
                          fontSize: 12,
                          color: COLORS.textMuted,
                          fontFamily: FONT,
                          margin: "4px 0 0",
                        }}
                      >
                        Atualizado há 2 horas
                      </p>
                    </div>
                    <div
                      style={{
                        background: `${COLORS.green}20`,
                        border: `1px solid ${COLORS.green}40`,
                        borderRadius: 8,
                        padding: "6px 16px",
                        fontSize: 12,
                        fontFamily: FONT,
                        color: COLORS.green,
                        fontWeight: 600,
                      }}
                    >
                      🟢 Ativo
                    </div>
                  </div>

                  {/* Stats row */}
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "repeat(3, 1fr)",
                      gap: 16,
                      marginBottom: 28,
                    }}
                  >
                    {[
                      {
                        label: "Leads",
                        value: "47",
                        icon: "👥",
                        color: COLORS.teal,
                      },
                      {
                        label: "Deals",
                        value: "12",
                        icon: "🤝",
                        color: COLORS.accent,
                      },
                      {
                        label: "Receita",
                        value: "R$ 84k",
                        icon: "💎",
                        color: COLORS.green,
                      },
                    ].map((stat) => (
                      <div
                        key={stat.label}
                        style={{
                          background: COLORS.card,
                          border: `1px solid ${COLORS.cardBorder}`,
                          borderRadius: 12,
                          padding: "18px 22px",
                          display: "flex",
                          alignItems: "center",
                          gap: 14,
                        }}
                      >
                        <span style={{ fontSize: 24 }}>{stat.icon}</span>
                        <div>
                          <div
                            style={{
                              fontSize: 24,
                              fontWeight: 800,
                              color: stat.color,
                              fontFamily: FONT,
                              lineHeight: 1,
                            }}
                          >
                            {stat.value}
                          </div>
                          <div
                            style={{
                              fontSize: 11,
                              color: COLORS.textMuted,
                              fontFamily: FONT,
                              marginTop: 3,
                            }}
                          >
                            {stat.label}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Leads header */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      marginBottom: 14,
                    }}
                  >
                    <div
                      style={{
                        fontSize: 13,
                        fontFamily: FONT,
                        color: COLORS.textSecondary,
                        fontWeight: 600,
                        textTransform: "uppercase",
                        letterSpacing: "0.5px",
                      }}
                    >
                      Lista de Leads
                    </div>
                    <div
                      style={{
                        fontSize: 11,
                        fontFamily: FONT,
                        color: COLORS.textMuted,
                      }}
                    >
                      47 resultados
                    </div>
                  </div>

                  {/* Lead cards */}
                  {leads.map((lead, i) => (
                    <LeadCard
                      key={lead.name}
                      {...lead}
                      isHighlighted={
                        i === 2 && highlightedCard
                          ? highlightedCard
                          : undefined
                      }
                    />
                  ))}
                </div>
              </ScreenScroll>
            </div>
          </div>
        </BrowserFrame>
      </div>

      {/* Tooltip on lead card — Mariana Rocha is 3rd card */}
      {/* Approx position: left = 60 + 200 + ~300 = 560, top = 60 + 44 + 28 + 24 + 80 + 130 = ~370 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          zIndex: 10,
        }}
      >
        <InlineTooltip
          x={900}
          y={420}
          text="Clique para ver detalhes do lead"
          visible={tooltipVisible}
        />
      </div>

      {/* Cursor hovering over the Mariana Rocha lead card */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          zIndex: 20,
        }}
      >
        <AnimatedCursor
          path={[
            { x: 1200, y: 700, action: "move", delay: 30 },
            { x: 900, y: 435, action: "hover", delay: 120 },
          ]}
          speed={5}
          clickEffect="ring"
          color={COLORS.teal}
        />
      </div>

      <ProgressBar color={COLORS.accent} height={3} />
    </AbsoluteFill>
  );
};

// ── Scene 7: CTA ──────────────────────────────────────────────────────────────
const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Particle-like dots
  const dots = Array.from({ length: 12 }, (_, i) => ({
    x: 10 + (i * 8.5) % 90,
    y: 20 + (i * 13.7) % 60,
    size: 2 + (i % 3) * 2,
    opacity: 0.1 + (i % 4) * 0.06,
    delay: i * 8,
  }));

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 20,
      }}
    >
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#1a0a2e"
        colorMid="#0d1a2e"
        direction={135}
        animated
      />

      {/* Background grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(108, 92, 231, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(108, 92, 231, 0.04) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />

      {/* Floating dots */}
      {dots.map((dot, i) => {
        const floatY = Math.sin((frame + dot.delay) * 0.04) * 8;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `${dot.x}%`,
              top: `${dot.y}%`,
              width: dot.size,
              height: dot.size,
              borderRadius: "50%",
              background: COLORS.accentLight,
              opacity: dot.opacity,
              transform: `translateY(${floatY}px)`,
            }}
          />
        );
      })}

      <div
        style={{
          position: "relative",
          zIndex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
          textAlign: "center",
        }}
      >
        {/* Badge */}
        <div
          style={{
            background: `${COLORS.pink}20`,
            border: `1px solid ${COLORS.pink}40`,
            borderRadius: 20,
            padding: "6px 18px",
          }}
        >
          <AnimatedText
            text="Comece hoje mesmo"
            animation="fade-in"
            fontSize={13}
            color={COLORS.pink}
            fontWeight={600}
          />
        </div>

        <AnimatedText
          text="Crie seu funil agora"
          animation="bounce"
          delay={10}
          fontSize={72}
          color={COLORS.textPrimary}
          fontWeight={800}
          style={{ textAlign: "center" }}
        />

        <AnimatedText
          text="14 dias grátis — tomikos.app"
          animation="fade-in"
          delay={30}
          fontSize={24}
          color={COLORS.pink}
          fontWeight={500}
          style={{ textAlign: "center", letterSpacing: "0.5px" }}
        />

        {/* CTA Button */}
        <div
          style={{
            opacity: interpolate(frame, [40, 55], [0, 1], {
              extrapolateRight: "clamp",
            }),
            transform: `translateY(${interpolate(frame, [40, 55], [20, 0], {
              extrapolateRight: "clamp",
            })}px)`,
            marginTop: 16,
          }}
        >
          <div
            style={{
              background: `linear-gradient(135deg, ${COLORS.accent}, ${COLORS.pink})`,
              borderRadius: 14,
              padding: "16px 40px",
              fontSize: 18,
              fontWeight: 700,
              fontFamily: FONT,
              color: "#fff",
              boxShadow: `0 8px 32px ${COLORS.accent}50, 0 2px 8px rgba(0,0,0,0.3)`,
              letterSpacing: "0.3px",
            }}
          >
            Criar conta gratuita →
          </div>
        </div>
      </div>

      <ProgressBar color={COLORS.pink} height={3} />
      <BrandWatermark handle="tomikos.app" position="bottom-right" color="rgba(255,255,255,0.4)" />
    </AbsoluteFill>
  );
};

// ── Step Indicator ────────────────────────────────────────────────────────────
const StepIndicator: React.FC<{ currentStep: number; totalSteps: number }> = ({
  currentStep,
  totalSteps,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 28,
        left: "50%",
        transform: "translateX(-50%)",
        display: "flex",
        gap: 8,
        zIndex: 100,
        opacity,
      }}
    >
      {Array.from({ length: totalSteps }, (_, i) => (
        <div
          key={i}
          style={{
            width: i === currentStep - 1 ? 24 : 8,
            height: 8,
            borderRadius: 4,
            background:
              i === currentStep - 1
                ? COLORS.accent
                : i < currentStep - 1
                ? `${COLORS.accent}60`
                : `${COLORS.cardBorder}80`,
            transition: "all 0.3s",
          }}
        />
      ))}
    </div>
  );
};

// ── Main Composition ──────────────────────────────────────────────────────────
export const AppWalkthrough: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: COLORS.bg }}>
      {/* Scene 1 — Hook: 0–90 */}
      <Sequence from={0} durationInFrames={90}>
        <HookScene />
      </Sequence>

      {/* Scene 2 — Dashboard: 90–450 */}
      <Sequence from={90} durationInFrames={360}>
        <DashboardScene />
        <StepIndicator currentStep={1} totalSteps={3} />
      </Sequence>

      {/* Scene 3 — Transition: 450–510 */}
      <Sequence from={450} durationInFrames={60}>
        <TransitionScene text="Configurando..." />
      </Sequence>

      {/* Scene 4 — Funnel Editor: 510–870 */}
      <Sequence from={510} durationInFrames={360}>
        <FunnelEditorScene />
        <StepIndicator currentStep={2} totalSteps={3} />
      </Sequence>

      {/* Scene 5 — Transition: 870–930 */}
      <Sequence from={870} durationInFrames={60}>
        <TransitionScene text="Quase lá..." />
      </Sequence>

      {/* Scene 6 — Active Funnel: 930–1260 */}
      <Sequence from={930} durationInFrames={330}>
        <ActiveFunnelScene />
        <StepIndicator currentStep={3} totalSteps={3} />
      </Sequence>

      {/* Scene 7 — CTA: 1260–1500 */}
      <Sequence from={1260} durationInFrames={240}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
