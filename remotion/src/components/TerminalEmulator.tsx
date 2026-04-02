import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface TerminalCommand {
  text: string;
  type: "input" | "output" | "spinner" | "success" | "error" | "blank";
  color?: string;
  delay?: number;
  typeSpeed?: number;
}

interface TerminalEmulatorProps {
  commands: TerminalCommand[];
  theme?: "dark" | "light";
  prompt?: string;
  title?: string;
  fontSize?: number;
}

const SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];

export const TerminalEmulator: React.FC<TerminalEmulatorProps> = ({
  commands,
  theme = "dark",
  prompt = "~ $",
  title = "Terminal",
  fontSize = 14,
}) => {
  const frame = useCurrentFrame();

  const isDark = theme === "dark";
  const bg = isDark ? "#1e1e2e" : "#fafafa";
  const textColor = isDark ? "#cdd6f4" : "#1e1e2e";
  const promptColor = "#89b4fa";
  const successColor = "#a6e3a1";
  const errorColor = "#f38ba8";
  const outputColor = isDark ? "#a6adc8" : "#5c5f77";
  const borderColor = isDark ? "#313244" : "#dce0e8";
  const titleBarBg = isDark ? "#181825" : "#eff1f5";
  const cursorColor = "#f5c2e7";

  // Build timeline: calculate start frame for each command
  const timeline: number[] = [];
  let currentFrame = 0;
  for (const cmd of commands) {
    const delay = cmd.delay ?? 8;
    currentFrame += delay;
    timeline.push(currentFrame);
    // Advance past this command's rendering time
    if (cmd.type === "input") {
      const typeSpeed = cmd.typeSpeed ?? 2;
      currentFrame += cmd.text.length * typeSpeed + 10;
    } else if (cmd.type === "blank") {
      // blank just takes the delay
    } else {
      currentFrame += 20; // time for output/success/error/spinner to show
    }
  }

  const renderLine = (cmd: TerminalCommand, startF: number, index: number) => {
    const localFrame = Math.max(0, frame - startF);

    if (cmd.type === "blank") {
      return <div key={index} style={{ height: fontSize * 1.6 }} />;
    }

    if (cmd.type === "input") {
      const typeSpeed = cmd.typeSpeed ?? 2;
      const totalChars = cmd.text.length;
      const charsToShow = Math.min(
        totalChars,
        Math.floor(localFrame / typeSpeed)
      );
      const isTyping = charsToShow < totalChars;
      const typingDone = localFrame > totalChars * typeSpeed;
      const showCursor = isTyping || (typingDone && localFrame % 30 < 15);

      if (localFrame < 0) return null;

      return (
        <div
          key={index}
          style={{
            display: "flex",
            alignItems: "center",
            fontFamily: '"Fira Code", "Courier New", monospace',
            fontSize,
            lineHeight: 1.6,
            color: textColor,
            whiteSpace: "pre",
          }}
        >
          <span style={{ color: promptColor, marginRight: 8 }}>{prompt}</span>
          <span>{cmd.text.slice(0, charsToShow)}</span>
          {showCursor && (
            <span
              style={{
                display: "inline-block",
                width: fontSize * 0.6,
                height: fontSize * 1.2,
                background: cursorColor,
                marginLeft: 1,
                verticalAlign: "middle",
                opacity: localFrame % 20 < 10 ? 1 : 0.3,
              }}
            />
          )}
        </div>
      );
    }

    if (cmd.type === "output") {
      const opacity = interpolate(localFrame, [0, 5], [0, 1], {
        extrapolateRight: "clamp",
      });
      return (
        <div
          key={index}
          style={{
            opacity,
            fontFamily: '"Fira Code", "Courier New", monospace',
            fontSize,
            lineHeight: 1.6,
            color: cmd.color ?? outputColor,
            paddingLeft: 4,
            whiteSpace: "pre-wrap",
          }}
        >
          {cmd.text}
        </div>
      );
    }

    if (cmd.type === "spinner") {
      const opacity = interpolate(localFrame, [0, 3], [0, 1], {
        extrapolateRight: "clamp",
      });
      // spinner completes after text.length * 3 frames (approximate)
      const spinnerDuration = Math.max(30, cmd.text.length * 3);
      const isDone = localFrame > spinnerDuration;
      const spinnerChar = isDone
        ? "✓"
        : SPINNER_CHARS[Math.floor(localFrame / 3) % SPINNER_CHARS.length];
      const spinnerColor = isDone ? successColor : "#89dceb";

      return (
        <div
          key={index}
          style={{
            opacity,
            display: "flex",
            alignItems: "center",
            fontFamily: '"Fira Code", "Courier New", monospace',
            fontSize,
            lineHeight: 1.6,
            color: cmd.color ?? textColor,
            gap: 8,
          }}
        >
          <span style={{ color: spinnerColor }}>{spinnerChar}</span>
          <span>{cmd.text}</span>
        </div>
      );
    }

    if (cmd.type === "success") {
      const opacity = interpolate(localFrame, [0, 5], [0, 1], {
        extrapolateRight: "clamp",
      });
      return (
        <div
          key={index}
          style={{
            opacity,
            display: "flex",
            alignItems: "center",
            fontFamily: '"Fira Code", "Courier New", monospace',
            fontSize,
            lineHeight: 1.6,
            color: cmd.color ?? successColor,
            gap: 8,
          }}
        >
          <span>✓</span>
          <span>{cmd.text}</span>
        </div>
      );
    }

    if (cmd.type === "error") {
      const opacity = interpolate(localFrame, [0, 5], [0, 1], {
        extrapolateRight: "clamp",
      });
      return (
        <div
          key={index}
          style={{
            opacity,
            display: "flex",
            alignItems: "center",
            fontFamily: '"Fira Code", "Courier New", monospace',
            fontSize,
            lineHeight: 1.6,
            color: cmd.color ?? errorColor,
            gap: 8,
          }}
        >
          <span>✗</span>
          <span>{cmd.text}</span>
        </div>
      );
    }

    return null;
  };

  return (
    <div
      style={{
        background: bg,
        borderRadius: 12,
        overflow: "hidden",
        border: `1px solid ${borderColor}`,
        boxShadow: isDark
          ? "0 20px 60px rgba(0,0,0,0.5)"
          : "0 20px 60px rgba(0,0,0,0.15)",
        fontFamily: '"Fira Code", "Courier New", monospace',
      }}
    >
      {/* Title bar */}
      <div
        style={{
          background: titleBarBg,
          padding: "12px 16px",
          display: "flex",
          alignItems: "center",
          gap: 8,
          borderBottom: `1px solid ${borderColor}`,
        }}
      >
        {/* Traffic lights */}
        <div style={{ display: "flex", gap: 6 }}>
          <div
            style={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              background: "#ff5f57",
              boxShadow: "0 0 0 1px rgba(0,0,0,0.15)",
            }}
          />
          <div
            style={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              background: "#febc2e",
              boxShadow: "0 0 0 1px rgba(0,0,0,0.15)",
            }}
          />
          <div
            style={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              background: "#28c840",
              boxShadow: "0 0 0 1px rgba(0,0,0,0.15)",
            }}
          />
        </div>
        {/* Title */}
        <div
          style={{
            flex: 1,
            textAlign: "center",
            fontSize: 12,
            color: isDark ? "#6c7086" : "#9ca0b0",
            fontFamily:
              '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            fontWeight: 500,
          }}
        >
          {title}
        </div>
        {/* Spacer to balance traffic lights */}
        <div style={{ width: 54 }} />
      </div>

      {/* Terminal body */}
      <div
        style={{
          padding: "16px 20px",
          minHeight: 200,
          background: bg,
        }}
      >
        {commands.map((cmd, index) => {
          const startF = timeline[index];
          if (frame < startF) return null;
          return renderLine(cmd, startF, index);
        })}
      </div>
    </div>
  );
};
