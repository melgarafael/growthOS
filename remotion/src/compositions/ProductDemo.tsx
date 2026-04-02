import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { AnimatedText } from "../components/AnimatedText";
import { BackgroundGradient } from "../components/BackgroundGradient";
import { ProgressBar } from "../components/ProgressBar";
import { BrandWatermark } from "../components/BrandWatermark";
import { BrowserFrame } from "../components/BrowserFrame";
import { AnimatedCursor } from "../components/AnimatedCursor";
import { ScreenScroll } from "../components/ScreenScroll";
import { ZoomReveal } from "../components/ZoomReveal";

// ── Color palette ─────────────────────────────────────────────────────────────
const COLORS = {
  bg: "#0a0a0a",
  card: "#1a1a2e",
  cardLight: "#16213e",
  accent: "#6c5ce7",
  secondary: "#00cec9",
  pink: "#fd79a8",
  text: "#ffffff",
  textMuted: "rgba(255,255,255,0.6)",
  textDim: "rgba(255,255,255,0.35)",
  green: "#00b894",
  orange: "#e17055",
  yellow: "#fdcb6e",
};

// ── Shared font ───────────────────────────────────────────────────────────────
const FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';

// ── Mock UI: Dashboard View ───────────────────────────────────────────────────

const DashboardView: React.FC = () => {
  const deals = [
    {
      name: "Empresa Alpha Ltda",
      value: "R$ 48.000",
      stage: "Proposta",
      color: COLORS.accent,
      contact: "Marcos Lima",
      prob: "75%",
    },
    {
      name: "Beta Soluções S.A.",
      value: "R$ 120.000",
      stage: "Negociação",
      color: COLORS.secondary,
      contact: "Ana Souza",
      prob: "60%",
    },
    {
      name: "Gamma Tech ME",
      value: "R$ 22.500",
      stage: "Qualificado",
      color: COLORS.pink,
      contact: "Felipe Neto",
      prob: "90%",
    },
  ];

  return (
    <div
      style={{
        background: COLORS.bg,
        width: "100%",
        height: "100%",
        padding: "32px 40px",
        boxSizing: "border-box",
        fontFamily: FONT,
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 32,
        }}
      >
        <div>
          <div
            style={{
              fontSize: 22,
              fontWeight: 700,
              color: COLORS.text,
              marginBottom: 4,
            }}
          >
            Pipeline de Vendas
          </div>
          <div style={{ fontSize: 13, color: COLORS.textMuted }}>
            3 negócios ativos • R$ 190.500 em aberto
          </div>
        </div>
        <div
          style={{
            background: COLORS.accent,
            color: COLORS.text,
            padding: "8px 20px",
            borderRadius: 8,
            fontSize: 13,
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          + Novo Negócio
        </div>
      </div>

      {/* Stats row */}
      <div
        style={{
          display: "flex",
          gap: 16,
          marginBottom: 32,
        }}
      >
        {[
          { label: "Total de Leads", value: "142", delta: "+12%", color: COLORS.accent },
          { label: "Taxa de Conversão", value: "28%", delta: "+3%", color: COLORS.secondary },
          { label: "Ticket Médio", value: "R$ 63.500", delta: "+8%", color: COLORS.green },
        ].map((stat) => (
          <div
            key={stat.label}
            style={{
              flex: 1,
              background: COLORS.card,
              borderRadius: 12,
              padding: "16px 20px",
              border: `1px solid rgba(255,255,255,0.06)`,
            }}
          >
            <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 6, textTransform: "uppercase", letterSpacing: 1 }}>
              {stat.label}
            </div>
            <div style={{ fontSize: 24, fontWeight: 700, color: COLORS.text, marginBottom: 4 }}>
              {stat.value}
            </div>
            <div style={{ fontSize: 12, color: COLORS.green, fontWeight: 600 }}>{stat.delta} este mês</div>
          </div>
        ))}
      </div>

      {/* Deal cards */}
      <div style={{ display: "flex", gap: 16 }}>
        {deals.map((deal) => (
          <div
            key={deal.name}
            style={{
              flex: 1,
              background: COLORS.card,
              borderRadius: 14,
              padding: "20px 22px",
              border: `1px solid rgba(255,255,255,0.07)`,
              cursor: "pointer",
              position: "relative",
              overflow: "hidden",
            }}
          >
            {/* Accent top bar */}
            <div
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                height: 3,
                background: deal.color,
                borderRadius: "14px 14px 0 0",
              }}
            />
            <div style={{ marginTop: 8 }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: COLORS.text, marginBottom: 6 }}>
                {deal.name}
              </div>
              <div style={{ fontSize: 22, fontWeight: 800, color: deal.color, marginBottom: 12 }}>
                {deal.value}
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
                <div
                  style={{
                    background: `${deal.color}22`,
                    color: deal.color,
                    padding: "3px 10px",
                    borderRadius: 20,
                    fontSize: 11,
                    fontWeight: 600,
                  }}
                >
                  {deal.stage}
                </div>
                <div style={{ fontSize: 11, color: COLORS.textMuted }}>{deal.contact}</div>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <div
                  style={{
                    flex: 1,
                    height: 4,
                    background: "rgba(255,255,255,0.1)",
                    borderRadius: 2,
                  }}
                >
                  <div
                    style={{
                      width: deal.prob,
                      height: "100%",
                      background: deal.color,
                      borderRadius: 2,
                    }}
                  />
                </div>
                <div style={{ fontSize: 11, color: COLORS.textMuted, flexShrink: 0 }}>
                  {deal.prob}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ── Mock UI: Deal Detail View ─────────────────────────────────────────────────

const DealDetailView: React.FC<{ tall?: boolean }> = ({ tall = false }) => {
  const timeline = [
    { date: "Hoje, 14:32", event: "Email de proposta enviado", icon: "📧", color: COLORS.accent },
    { date: "Ontem, 10:15", event: "Reunião de apresentação realizada", icon: "🤝", color: COLORS.secondary },
    { date: "15/03, 09:00", event: "Lead qualificado pelo SDR", icon: "✅", color: COLORS.green },
    { date: "12/03, 16:45", event: "Primeiro contato via LinkedIn", icon: "💼", color: COLORS.yellow },
    { date: "10/03, 11:20", event: "Lead cadastrado no sistema", icon: "📋", color: COLORS.textMuted },
  ];

  return (
    <div
      style={{
        background: COLORS.bg,
        width: "100%",
        minHeight: tall ? 900 : "100%",
        padding: "28px 40px",
        boxSizing: "border-box",
        fontFamily: FONT,
      }}
    >
      {/* Breadcrumb */}
      <div style={{ fontSize: 12, color: COLORS.textMuted, marginBottom: 20 }}>
        Pipeline de Vendas &rsaquo; <span style={{ color: COLORS.accent }}>Empresa Alpha Ltda</span>
      </div>

      {/* Deal header */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          marginBottom: 28,
        }}
      >
        <div>
          <div style={{ fontSize: 24, fontWeight: 800, color: COLORS.text, marginBottom: 6 }}>
            Empresa Alpha Ltda
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span
              style={{
                background: `${COLORS.accent}22`,
                color: COLORS.accent,
                padding: "4px 14px",
                borderRadius: 20,
                fontSize: 12,
                fontWeight: 600,
              }}
            >
              Proposta
            </span>
            <span style={{ fontSize: 13, color: COLORS.textMuted }}>Marcos Lima • marcos@alpha.com.br</span>
          </div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 30, fontWeight: 800, color: COLORS.accent }}>R$ 48.000</div>
          <div style={{ fontSize: 12, color: COLORS.textMuted }}>Valor do contrato</div>
        </div>
      </div>

      {/* Info cards row */}
      <div style={{ display: "flex", gap: 14, marginBottom: 28 }}>
        {[
          { label: "Responsável", value: "João Santos", icon: "👤" },
          { label: "Empresa", value: "Alpha Ltda", icon: "🏢" },
          { label: "Telefone", value: "(11) 99999-0000", icon: "📱" },
          { label: "Probabilidade", value: "75%", icon: "📊" },
        ].map((info) => (
          <div
            key={info.label}
            style={{
              flex: 1,
              background: COLORS.card,
              borderRadius: 10,
              padding: "12px 16px",
              border: "1px solid rgba(255,255,255,0.06)",
            }}
          >
            <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 4 }}>
              {info.icon} {info.label}
            </div>
            <div style={{ fontSize: 14, fontWeight: 600, color: COLORS.text }}>{info.value}</div>
          </div>
        ))}
      </div>

      {/* Timeline */}
      <div
        style={{
          background: COLORS.card,
          borderRadius: 14,
          padding: "20px 24px",
          border: "1px solid rgba(255,255,255,0.06)",
          marginBottom: 28,
        }}
      >
        <div style={{ fontSize: 14, fontWeight: 700, color: COLORS.text, marginBottom: 18 }}>
          Histórico de Atividades
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          {timeline.map((item, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div
                style={{
                  width: 34,
                  height: 34,
                  borderRadius: "50%",
                  background: `${item.color}22`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 15,
                  flexShrink: 0,
                }}
              >
                {item.icon}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, color: COLORS.text, fontWeight: 500 }}>{item.event}</div>
                <div style={{ fontSize: 11, color: COLORS.textMuted }}>{item.date}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Fechar Negócio button (zoom target) */}
      <div style={{ display: "flex", gap: 12, justifyContent: "flex-end" }}>
        <button
          style={{
            background: "rgba(255,255,255,0.08)",
            color: COLORS.textMuted,
            border: "1px solid rgba(255,255,255,0.12)",
            padding: "12px 28px",
            borderRadius: 10,
            fontSize: 14,
            fontWeight: 600,
            cursor: "pointer",
            fontFamily: FONT,
          }}
        >
          Agendar Follow-up
        </button>
        <button
          style={{
            background: `linear-gradient(135deg, ${COLORS.green}, ${COLORS.secondary})`,
            color: COLORS.text,
            border: "none",
            padding: "12px 32px",
            borderRadius: 10,
            fontSize: 14,
            fontWeight: 700,
            cursor: "pointer",
            fontFamily: FONT,
            boxShadow: `0 4px 20px ${COLORS.green}44`,
          }}
        >
          Fechar Negócio
        </button>
      </div>
    </div>
  );
};

// ── Scene 1: Hook ─────────────────────────────────────────────────────────────

const SceneHook: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        gap: 20,
      }}
    >
      <AnimatedText
        text="Veja o TomiKOS em ação"
        animation="scale-in"
        fontSize={64}
        fontWeight={800}
        color={COLORS.text}
        textAlign="center"
      />
      <AnimatedText
        text="Sistema comercial inteligente"
        animation="fade-in"
        delay={18}
        fontSize={28}
        fontWeight={400}
        color={COLORS.textMuted}
        textAlign="center"
      />
    </AbsoluteFill>
  );
};

// ── Scene 2: Device Intro ─────────────────────────────────────────────────────

const SceneDeviceIntro: React.FC = () => {
  return (
    <AbsoluteFill style={{ padding: "60px 140px", boxSizing: "border-box" }}>
      <BrowserFrame url="tomikos.app/dashboard" darkMode={true}>
        <DashboardView />
      </BrowserFrame>
    </AbsoluteFill>
  );
};

// ── Scene 3: Navigate (cursor + state swap) ───────────────────────────────────

const SceneNavigate: React.FC = () => {
  const frame = useCurrentFrame();

  // Total scene is 240 frames. Click happens around frame 160.
  // The deal detail fades in after the click.
  const CLICK_FRAME = 160;
  const detailOpacity = interpolate(frame, [CLICK_FRAME, CLICK_FRAME + 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const dashboardOpacity = interpolate(frame, [CLICK_FRAME, CLICK_FRAME + 20], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Cursor path: start center, hover over first card, click
  // The browser frame content area starts around x=140, y=60 in video coords
  // With padding 60px/140px, browser is at x=140, y=60, size ~1640x960
  // Inside content (after 44px toolbar): y offset = 60 + 44 = 104
  // First deal card is roughly at x=340, y=300 in video space
  const cursorPath = [
    { x: 960, y: 540, action: "move" as const, delay: 20 },
    { x: 420, y: 360, action: "hover" as const, delay: 30 },
    { x: 420, y: 360, action: "click" as const, delay: 10 },
  ];

  return (
    <AbsoluteFill style={{ padding: "60px 140px", boxSizing: "border-box" }}>
      <BrowserFrame url="tomikos.app/dashboard" darkMode={true}>
        {/* Dashboard fades out on click */}
        <div style={{ position: "absolute", inset: 0, opacity: dashboardOpacity }}>
          <DashboardView />
        </div>
        {/* Deal detail fades in on click */}
        <div style={{ position: "absolute", inset: 0, opacity: detailOpacity }}>
          <DealDetailView />
        </div>
      </BrowserFrame>

      {/* Cursor rendered at video level (outside browser frame container) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
        }}
      >
        <AnimatedCursor
          path={cursorPath}
          speed={6}
          clickEffect="ripple"
          color={COLORS.accent}
        />
      </div>
    </AbsoluteFill>
  );
};

// ── Scene 4: Scroll ───────────────────────────────────────────────────────────

const SceneScroll: React.FC = () => {
  return (
    <AbsoluteFill style={{ padding: "60px 140px", boxSizing: "border-box" }}>
      <BrowserFrame url="tomikos.app/deal/alpha" darkMode={true}>
        <ScreenScroll
          scrollDistance={380}
          scrollSpeed={3}
          pausePoints={[{ position: 200, duration: 40 }]}
          easing="ease-in-out"
        >
          <DealDetailView tall={true} />
        </ScreenScroll>
      </BrowserFrame>
    </AbsoluteFill>
  );
};

// ── Scene 5: Zoom ─────────────────────────────────────────────────────────────

const SceneZoom: React.FC = () => {
  // The "Fechar Negócio" button is near the bottom of deal detail.
  // In the browser content area (inside 60px/140px padding, 44px toolbar):
  // Content area roughly: 1640w x 916h starting at y=44 inside browser
  // Button row is at ~y=700 in content, button is at x~1100, y~700, w~200, h~44
  const zoomTarget = {
    x: 1070,
    y: 690,
    width: 220,
    height: 48,
  };

  return (
    <AbsoluteFill style={{ padding: "60px 140px", boxSizing: "border-box" }}>
      <BrowserFrame url="tomikos.app/deal/alpha" darkMode={true}>
        <ZoomReveal
          target={zoomTarget}
          zoomLevel={2.5}
          duration={50}
          highlightBox={true}
          highlightColor={COLORS.secondary}
        >
          <DealDetailView />
        </ZoomReveal>
      </BrowserFrame>
    </AbsoluteFill>
  );
};

// ── Scene 6: Feature Cards ────────────────────────────────────────────────────

const FeatureCard: React.FC<{
  icon: string;
  title: string;
  description: string;
  accentColor: string;
  delay: number;
}> = ({ icon, title, description, accentColor, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const adjustedFrame = Math.max(0, frame - delay);

  const cardSpring = spring({
    frame: adjustedFrame,
    fps,
    config: { damping: 14, stiffness: 120, mass: 1 },
  });

  const opacity = interpolate(adjustedFrame, [0, 12], [0, 1], {
    extrapolateRight: "clamp",
  });
  const translateY = interpolate(cardSpring, [0, 1], [60, 0]);

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${translateY}px)`,
        background: `linear-gradient(145deg, ${COLORS.card}, ${COLORS.cardLight})`,
        border: `1px solid ${accentColor}44`,
        borderRadius: 20,
        padding: "36px 32px",
        flex: 1,
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        gap: 16,
        boxShadow: `0 8px 40px rgba(0,0,0,0.4), 0 0 0 1px ${accentColor}22, inset 0 1px 0 rgba(255,255,255,0.08)`,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Glow blob */}
      <div
        style={{
          position: "absolute",
          top: -40,
          right: -40,
          width: 120,
          height: 120,
          background: `radial-gradient(circle, ${accentColor}33, transparent 70%)`,
          borderRadius: "50%",
        }}
      />

      <div
        style={{
          width: 56,
          height: 56,
          borderRadius: 14,
          background: `${accentColor}22`,
          border: `1px solid ${accentColor}55`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 26,
        }}
      >
        {icon}
      </div>

      <div>
        <div
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: COLORS.text,
            marginBottom: 8,
            fontFamily: FONT,
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontSize: 15,
            color: COLORS.textMuted,
            lineHeight: 1.6,
            fontFamily: FONT,
          }}
        >
          {description}
        </div>
      </div>

      <div
        style={{
          marginTop: "auto",
          display: "flex",
          alignItems: "center",
          gap: 8,
          color: accentColor,
          fontSize: 13,
          fontWeight: 600,
          fontFamily: FONT,
        }}
      >
        Saiba mais →
      </div>
    </div>
  );
};

const SceneFeatureCards: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const titleOpacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  const features = [
    {
      icon: "📊",
      title: "Pipeline Visual",
      description: "Visualize todo o funil de vendas em tempo real. Arraste e solte negócios entre etapas com facilidade.",
      color: COLORS.accent,
      delay: 0,
    },
    {
      icon: "🤖",
      title: "IA Integrada",
      description: "Inteligência artificial que sugere próximas ações, prioriza leads e prevê o fechamento de negócios.",
      color: COLORS.secondary,
      delay: 60,
    },
    {
      icon: "⚡",
      title: "Automação Total",
      description: "Fluxos automatizados de follow-up, e-mails, tarefas e notificações sem esforço manual.",
      color: COLORS.pink,
      delay: 120,
    },
  ];

  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        padding: "80px 100px",
        gap: 48,
      }}
    >
      {/* Section title */}
      <div
        style={{
          opacity: titleOpacity,
          transform: `translateY(${interpolate(titleSpring, [0, 1], [30, 0])}px)`,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontSize: 38,
            fontWeight: 800,
            color: COLORS.text,
            fontFamily: FONT,
            marginBottom: 10,
          }}
        >
          Por que o TomiKOS?
        </div>
        <div style={{ fontSize: 18, color: COLORS.textMuted, fontFamily: FONT }}>
          Tudo que você precisa para vender mais, em um só lugar.
        </div>
      </div>

      {/* Cards */}
      <div style={{ display: "flex", gap: 24, width: "100%" }}>
        {features.map((f) => (
          <FeatureCard
            key={f.title}
            icon={f.icon}
            title={f.title}
            description={f.description}
            accentColor={f.color}
            delay={f.delay}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ── Scene 7: CTA ──────────────────────────────────────────────────────────────

const SceneCTA: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgPulse = interpolate(frame, [0, 60, 120, 180, 240], [1, 1.04, 1, 1.04, 1], {
    extrapolateRight: "clamp",
  });

  const dividerOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateRight: "clamp",
  });

  const subtextOpacity = interpolate(frame, [40, 60], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        gap: 24,
      }}
    >
      {/* Glow ring behind CTA */}
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${COLORS.accent}1a 0%, transparent 70%)`,
          transform: `scale(${bgPulse})`,
        }}
      />

      <AnimatedText
        text="Teste grátis por 14 dias"
        animation="bounce"
        fontSize={62}
        fontWeight={800}
        color={COLORS.text}
        textAlign="center"
      />

      {/* Divider */}
      <div
        style={{
          width: 80,
          height: 3,
          background: `linear-gradient(90deg, ${COLORS.accent}, ${COLORS.secondary})`,
          borderRadius: 2,
          opacity: dividerOpacity,
        }}
      />

      <div style={{ opacity: subtextOpacity, textAlign: "center" }}>
        <div
          style={{
            fontSize: 32,
            fontWeight: 700,
            color: COLORS.accent,
            fontFamily: FONT,
            marginBottom: 8,
          }}
        >
          tomikos.app
        </div>
        <div style={{ fontSize: 16, color: COLORS.textMuted, fontFamily: FONT }}>
          Sem cartão de crédito • Sem compromisso • Setup em 5 minutos
        </div>
      </div>

      {/* CTA button */}
      <div
        style={{
          marginTop: 16,
          opacity: interpolate(frame, [60, 90], [0, 1], { extrapolateRight: "clamp" }),
          transform: `scale(${interpolate(
            spring({ frame: Math.max(0, frame - 60), fps, config: { damping: 10, stiffness: 120 } }),
            [0, 1],
            [0.8, 1]
          )})`,
        }}
      >
        <div
          style={{
            background: `linear-gradient(135deg, ${COLORS.accent}, ${COLORS.pink})`,
            color: COLORS.text,
            padding: "18px 52px",
            borderRadius: 14,
            fontSize: 18,
            fontWeight: 700,
            fontFamily: FONT,
            boxShadow: `0 8px 40px ${COLORS.accent}66`,
            letterSpacing: 0.5,
          }}
        >
          Começar agora →
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── Main Composition ──────────────────────────────────────────────────────────

export const ProductDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: COLORS.bg }}>
      {/* Global background gradient */}
      <BackgroundGradient
        colorFrom="#0a0a0a"
        colorTo="#0d0d1a"
        colorMid="#0f0f22"
        direction={135}
        animated={true}
      />

      {/* Scene 1 — Hook (0–90) */}
      <Sequence from={0} durationInFrames={90}>
        <SceneHook />
      </Sequence>

      {/* Scene 2 — Device Intro (90–210) */}
      <Sequence from={90} durationInFrames={120}>
        <SceneDeviceIntro />
      </Sequence>

      {/* Scene 3 — Navigate (210–450) */}
      <Sequence from={210} durationInFrames={240}>
        <SceneNavigate />
      </Sequence>

      {/* Scene 4 — Scroll (450–630) */}
      <Sequence from={450} durationInFrames={180}>
        <SceneScroll />
      </Sequence>

      {/* Scene 5 — Zoom (630–810) */}
      <Sequence from={630} durationInFrames={180}>
        <SceneZoom />
      </Sequence>

      {/* Scene 6 — Feature Cards (810–1110) */}
      <Sequence from={810} durationInFrames={300}>
        <SceneFeatureCards />
      </Sequence>

      {/* Scene 7 — CTA (1110–1350) */}
      <Sequence from={1110} durationInFrames={240}>
        <SceneCTA />
      </Sequence>

      {/* Global overlays */}
      <ProgressBar position="top" color={COLORS.accent} height={3} />
      <BrandWatermark handle="@automatiklabs" position="bottom-right" color="rgba(255,255,255,0.5)" />
    </AbsoluteFill>
  );
};
