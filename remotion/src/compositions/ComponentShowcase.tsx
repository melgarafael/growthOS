import React from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from "remotion";
import { AnimatedText } from "../components/AnimatedText";
import { BackgroundGradient } from "../components/BackgroundGradient";
import { BrowserFrame } from "../components/BrowserFrame";
import { MobileFrame } from "../components/MobileFrame";
import { TerminalEmulator } from "../components/TerminalEmulator";
import { ChartAnimated } from "../components/ChartAnimated";
import { GlassmorphismCard } from "../components/GlassmorphismCard";
import { AnimatedCursor } from "../components/AnimatedCursor";

// ── Scene 1: BrowserFrame (0–150 frames / 5s) ──────────────────────────────

const SceneBrowserFrame: React.FC = () => {
  return (
    <AbsoluteFill>
      <BackgroundGradient colorFrom="#0a0a0a" colorTo="#1a1a2e" animated={false} />
      <AbsoluteFill
        style={{
          padding: 40,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 30,
        }}
      >
        <AnimatedText
          text="BrowserFrame"
          animation="fade-in"
          fontSize={42}
          color="#00cec9"
          fontWeight={700}
        />
        <div style={{ width: "100%", height: 1200 }}>
          <BrowserFrame url="tomikos.app/dashboard" darkMode>
            <div
              style={{
                background: "#141414",
                padding: 40,
                height: "100%",
                fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
              }}
            >
              <div
                style={{
                  fontSize: 28,
                  fontWeight: 700,
                  color: "#ffffff",
                  marginBottom: 16,
                }}
              >
                Dashboard
              </div>
              <div style={{ fontSize: 18, color: "#a0a0a0" }}>
                47 leads ativos
              </div>
            </div>
          </BrowserFrame>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 2: MobileFrame (150–300 frames / 5s) ─────────────────────────────

const SceneMobileFrame: React.FC = () => {
  return (
    <AbsoluteFill>
      <BackgroundGradient colorFrom="#0a0a0a" colorTo="#1a1a2e" animated={false} />
      <AbsoluteFill
        style={{
          padding: 40,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 30,
        }}
      >
        <AnimatedText
          text="MobileFrame"
          animation="fade-in"
          fontSize={42}
          color="#fd79a8"
          fontWeight={700}
        />
        <MobileFrame device="iphone15" darkMode scale={0.8}>
          <div
            style={{
              background: "#0a0a0a",
              padding: 32,
              height: "100%",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            }}
          >
            <div
              style={{
                fontSize: 22,
                fontWeight: 700,
                color: "#ffffff",
                marginBottom: 12,
              }}
            >
              AutomatikClub
            </div>
            <div style={{ fontSize: 14, color: "#a0a0a0" }}>
              Modulo 3 — IA Aplicada
            </div>
          </div>
        </MobileFrame>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 3: TerminalEmulator (300–540 frames / 8s) ────────────────────────

const SceneTerminalEmulator: React.FC = () => {
  return (
    <AbsoluteFill>
      <BackgroundGradient colorFrom="#0a0a0a" colorTo="#1a1a2e" animated={false} />
      <AbsoluteFill
        style={{
          padding: 40,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 30,
        }}
      >
        <AnimatedText
          text="TerminalEmulator"
          animation="fade-in"
          fontSize={42}
          color="#00cec9"
          fontWeight={700}
        />
        <div style={{ width: "100%", padding: "0 20px" }}>
          <TerminalEmulator
            title="Claude Code"
            commands={[
              { text: "/grow create blog sobre IA", type: "input", delay: 10 },
              { text: "Gerando conteudo...", type: "spinner", delay: 5 },
              {
                text: "Blog post criado (1.2k palavras)",
                type: "success",
                delay: 5,
              },
              { text: "SEO score: 94/100", type: "success", delay: 3 },
            ]}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 4: ChartAnimated (540–720 frames / 6s) ───────────────────────────

const SceneChartAnimated: React.FC = () => {
  return (
    <AbsoluteFill>
      <BackgroundGradient colorFrom="#0a0a0a" colorTo="#1a1a2e" animated={false} />
      <AbsoluteFill
        style={{
          padding: 40,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 40,
        }}
      >
        <AnimatedText
          text="ChartAnimated"
          animation="fade-in"
          fontSize={42}
          color="#fdcb6e"
          fontWeight={700}
        />
        <ChartAnimated
          type="bar"
          data={[
            { label: "Jan", value: 120 },
            { label: "Fev", value: 180 },
            { label: "Mar", value: 150 },
            { label: "Abr", value: 310 },
          ]}
          highlightIndex={3}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 5: GlassmorphismCard (720–870 frames / 5s) ───────────────────────

const SceneGlassmorphismCard: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #6c5ce7, #fd79a8)",
      }}
    >
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: 60,
        }}
      >
        <GlassmorphismCard animateIn="scale">
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 16,
              padding: 20,
              fontFamily:
                '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            }}
          >
            <div style={{ fontSize: 48 }}>&#x2728;</div>
            <div
              style={{
                fontSize: 32,
                fontWeight: 700,
                color: "#ffffff",
              }}
            >
              GlassmorphismCard
            </div>
            <div style={{ fontSize: 16, color: "rgba(255,255,255,0.7)" }}>
              Backdrop blur + translucent border
            </div>
          </div>
        </GlassmorphismCard>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 6: AnimatedCursor (870–1050 frames / 6s) ─────────────────────────

const SceneAnimatedCursor: React.FC = () => {
  return (
    <AbsoluteFill>
      <BackgroundGradient colorFrom="#0a0a0a" colorTo="#1a1a2e" animated={false} />
      <AbsoluteFill
        style={{
          padding: 40,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 30,
        }}
      >
        <div style={{ marginTop: 200 }}>
          <AnimatedText
            text="AnimatedCursor"
            animation="fade-in"
            fontSize={42}
            color="#e17055"
            fontWeight={700}
          />
        </div>

        {/* Mock button */}
        <div
          style={{
            position: "absolute",
            left: 100,
            top: 400,
            background: "#6c5ce7",
            borderRadius: 12,
            padding: "16px 40px",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            fontSize: 20,
            fontWeight: 600,
            color: "#ffffff",
          }}
        >
          Clique aqui
        </div>

        {/* Animated cursor */}
        <AnimatedCursor
          path={[
            { x: 500, y: 800, action: "move" },
            { x: 200, y: 420, action: "hover", delay: 15 },
            { x: 200, y: 420, action: "click", delay: 10 },
          ]}
          clickEffect="ring"
          speed={6}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Main Composition ────────────────────────────────────────────────────────

export const ComponentShowcase: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      {/* Scene 1: BrowserFrame — 0 to 150 frames (5s) */}
      <Sequence from={0} durationInFrames={150}>
        <SceneBrowserFrame />
      </Sequence>

      {/* Scene 2: MobileFrame — 150 to 300 frames (5s) */}
      <Sequence from={150} durationInFrames={150}>
        <SceneMobileFrame />
      </Sequence>

      {/* Scene 3: TerminalEmulator — 300 to 540 frames (8s) */}
      <Sequence from={300} durationInFrames={240}>
        <SceneTerminalEmulator />
      </Sequence>

      {/* Scene 4: ChartAnimated — 540 to 720 frames (6s) */}
      <Sequence from={540} durationInFrames={180}>
        <SceneChartAnimated />
      </Sequence>

      {/* Scene 5: GlassmorphismCard — 720 to 870 frames (5s) */}
      <Sequence from={720} durationInFrames={150}>
        <SceneGlassmorphismCard />
      </Sequence>

      {/* Scene 6: AnimatedCursor — 870 to 1050 frames (6s) */}
      <Sequence from={870} durationInFrames={180}>
        <SceneAnimatedCursor />
      </Sequence>
    </AbsoluteFill>
  );
};
