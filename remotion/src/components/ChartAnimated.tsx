import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

interface ChartAnimatedProps {
  type: "bar" | "line" | "donut";
  data: ChartDataPoint[];
  animationStyle?: "grow" | "draw" | "reveal";
  showLabels?: boolean;
  showValues?: boolean;
  highlightIndex?: number;
  duration?: number;
  accentColor?: string;
  textColor?: string;
}

const DEFAULT_COLORS = [
  "#6c5ce7",
  "#00cec9",
  "#fd79a8",
  "#fdcb6e",
  "#55efc4",
  "#74b9ff",
  "#a29bfe",
  "#fab1a0",
];

export const ChartAnimated: React.FC<ChartAnimatedProps> = ({
  type,
  data,
  animationStyle = "grow",
  showLabels = true,
  showValues = true,
  highlightIndex,
  duration = 60,
  accentColor = "#6c5ce7",
  textColor = "#ffffff",
}) => {
  const frame = useCurrentFrame();

  const animationDelay = 10;
  const localFrame = Math.max(0, frame - animationDelay);
  const rawProgress = interpolate(localFrame, [0, duration], [0, 1], {
    extrapolateRight: "clamp",
  });
  // Cubic ease-out: 1 - (1-t)^3
  const progress = 1 - Math.pow(1 - rawProgress, 3);

  const maxValue = Math.max(...data.map((d) => d.value));

  const getColor = (index: number) => {
    if (index === highlightIndex) return accentColor;
    return data[index].color ?? DEFAULT_COLORS[index % DEFAULT_COLORS.length];
  };

  if (type === "bar") {
    return <BarChart
      data={data}
      progress={progress}
      maxValue={maxValue}
      showLabels={showLabels}
      showValues={showValues}
      highlightIndex={highlightIndex}
      accentColor={accentColor}
      textColor={textColor}
      getColor={getColor}
    />;
  }

  if (type === "line") {
    return <LineChart
      data={data}
      progress={progress}
      maxValue={maxValue}
      showLabels={showLabels}
      showValues={showValues}
      highlightIndex={highlightIndex}
      accentColor={accentColor}
      textColor={textColor}
      getColor={getColor}
    />;
  }

  if (type === "donut") {
    return <DonutChart
      data={data}
      progress={progress}
      showLabels={showLabels}
      showValues={showValues}
      highlightIndex={highlightIndex}
      accentColor={accentColor}
      textColor={textColor}
      getColor={getColor}
    />;
  }

  return null;
};

// ─── Bar Chart ───────────────────────────────────────────────────────────────

interface InternalChartProps {
  data: ChartDataPoint[];
  progress: number;
  maxValue: number;
  showLabels: boolean;
  showValues: boolean;
  highlightIndex?: number;
  accentColor: string;
  textColor: string;
  getColor: (index: number) => string;
}

const BarChart: React.FC<InternalChartProps> = ({
  data,
  progress,
  maxValue,
  showLabels,
  showValues,
  textColor,
  getColor,
}) => {
  const chartHeight = 220;
  const barAreaHeight = 180;
  const barGap = 12;
  const containerWidth = 560;
  const barWidth = Math.min(
    60,
    (containerWidth - barGap * (data.length + 1)) / data.length
  );

  return (
    <div style={{ width: containerWidth, height: chartHeight + 40, position: "relative" }}>
      {/* Bars */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          gap: barGap,
          height: barAreaHeight,
          padding: `0 ${barGap}px`,
          position: "relative",
        }}
      >
        {data.map((point, i) => {
          const barHeightRatio = point.value / maxValue;
          const animatedHeight = barAreaHeight * barHeightRatio * progress;
          const color = getColor(i);
          const valueOpacity = progress > 0.5
            ? interpolate(progress, [0.5, 0.8], [0, 1], { extrapolateRight: "clamp" })
            : 0;

          return (
            <div
              key={i}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "flex-end",
                flex: 1,
                height: barAreaHeight,
              }}
            >
              {/* Value above bar */}
              {showValues && (
                <div
                  style={{
                    fontSize: 13,
                    fontWeight: 700,
                    color: textColor,
                    opacity: valueOpacity,
                    marginBottom: 6,
                    fontFamily:
                      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                    fontVariantNumeric: "tabular-nums",
                  }}
                >
                  {Math.round(point.value * progress)}
                </div>
              )}
              {/* Bar */}
              <div
                style={{
                  width: barWidth,
                  height: animatedHeight,
                  background: color,
                  borderRadius: "6px 6px 0 0",
                  boxShadow: `0 0 20px ${color}55`,
                  transition: "none",
                }}
              />
            </div>
          );
        })}
      </div>

      {/* Baseline */}
      <div
        style={{
          width: "100%",
          height: 1,
          background: `${textColor}30`,
          marginTop: 0,
        }}
      />

      {/* Labels */}
      {showLabels && (
        <div
          style={{
            display: "flex",
            gap: barGap,
            padding: `8px ${barGap}px 0`,
          }}
        >
          {data.map((point, i) => (
            <div
              key={i}
              style={{
                flex: 1,
                textAlign: "center",
                fontSize: 12,
                color: `${textColor}aa`,
                fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
            >
              {point.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ─── Line Chart ───────────────────────────────────────────────────────────────

const LineChart: React.FC<InternalChartProps> = ({
  data,
  progress,
  maxValue,
  showLabels,
  showValues,
  highlightIndex,
  accentColor,
  textColor,
  getColor,
}) => {
  const svgWidth = 560;
  const svgHeight = 220;
  const padding = { top: 24, right: 24, bottom: 40, left: 24 };
  const chartW = svgWidth - padding.left - padding.right;
  const chartH = svgHeight - padding.top - padding.bottom;

  const points = data.map((point, i) => ({
    x: padding.left + (i / (data.length - 1)) * chartW,
    y: padding.top + (1 - point.value / maxValue) * chartH,
    value: point.value,
    label: point.label,
    color: getColor(i),
  }));

  // Build the full SVG path
  const pathD = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`)
    .join(" ");

  // Approximate path length for strokeDasharray
  let pathLength = 0;
  for (let i = 1; i < points.length; i++) {
    const dx = points[i].x - points[i - 1].x;
    const dy = points[i].y - points[i - 1].y;
    pathLength += Math.sqrt(dx * dx + dy * dy);
  }

  const drawnLength = pathLength * progress;

  return (
    <div style={{ width: svgWidth, height: svgHeight, position: "relative" }}>
      <svg width={svgWidth} height={svgHeight} style={{ overflow: "visible" }}>
        {/* Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((t) => {
          const y = padding.top + (1 - t) * chartH;
          return (
            <line
              key={t}
              x1={padding.left}
              y1={y}
              x2={svgWidth - padding.right}
              y2={y}
              stroke={`${textColor}18`}
              strokeWidth={1}
            />
          );
        })}

        {/* Line path */}
        <path
          d={pathD}
          fill="none"
          stroke={accentColor}
          strokeWidth={3}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray={`${drawnLength} ${pathLength}`}
          strokeDashoffset={0}
        />

        {/* Area fill (subtle) */}
        {progress > 0.05 && (
          <path
            d={`${pathD} L ${points[points.length - 1].x} ${padding.top + chartH} L ${points[0].x} ${padding.top + chartH} Z`}
            fill={`${accentColor}18`}
            strokeDasharray={`${drawnLength + chartH * 2 + (points[points.length - 1].x - points[0].x)} 99999`}
          />
        )}

        {/* Data points */}
        {points.map((p, i) => {
          // Only show point if the drawn line has reached it
          const distToPoint = points
            .slice(0, i)
            .reduce((acc, _, idx) => {
              if (idx === 0) return acc;
              const dx = points[idx].x - points[idx - 1].x;
              const dy = points[idx].y - points[idx - 1].y;
              return acc + Math.sqrt(dx * dx + dy * dy);
            }, 0);
          const pointVisible = drawnLength >= distToPoint;
          if (!pointVisible) return null;

          const isHighlighted = i === highlightIndex;
          const r = isHighlighted ? 7 : 5;
          const pointOpacity = interpolate(
            Math.max(0, drawnLength - distToPoint),
            [0, 20],
            [0, 1],
            { extrapolateRight: "clamp" }
          );

          return (
            <g key={i} opacity={pointOpacity}>
              <circle
                cx={p.x}
                cy={p.y}
                r={r + 3}
                fill={`${p.color}33`}
              />
              <circle
                cx={p.x}
                cy={p.y}
                r={r}
                fill={p.color}
                stroke="#fff"
                strokeWidth={2}
              />
              {showValues && (
                <text
                  x={p.x}
                  y={p.y - r - 8}
                  textAnchor="middle"
                  fill={textColor}
                  fontSize={12}
                  fontWeight={600}
                  fontFamily='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
                >
                  {p.value}
                </text>
              )}
            </g>
          );
        })}

        {/* X-axis labels */}
        {showLabels &&
          points.map((p, i) => (
            <text
              key={i}
              x={p.x}
              y={svgHeight - 4}
              textAnchor="middle"
              fill={`${textColor}88`}
              fontSize={11}
              fontFamily='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            >
              {p.label}
            </text>
          ))}
      </svg>
    </div>
  );
};

// ─── Donut Chart ─────────────────────────────────────────────────────────────

interface DonutChartProps {
  data: ChartDataPoint[];
  progress: number;
  showLabels: boolean;
  showValues: boolean;
  highlightIndex?: number;
  accentColor: string;
  textColor: string;
  getColor: (index: number) => string;
}

const DonutChart: React.FC<DonutChartProps> = ({
  data,
  progress,
  showLabels,
  showValues,
  textColor,
  getColor,
}) => {
  const size = 240;
  const cx = size / 2;
  const cy = size / 2;
  const outerR = 90;
  const innerR = 54;
  const strokeWidth = outerR - innerR;
  const r = (outerR + innerR) / 2; // midpoint radius for stroke
  const circumference = 2 * Math.PI * r;

  const total = data.reduce((sum, d) => sum + d.value, 0);

  // Build segments
  let cumulativeAngle = 0; // in [0,1] fractions
  const segments = data.map((point, i) => {
    const fraction = point.value / total;
    const segmentStart = cumulativeAngle;
    cumulativeAngle += fraction;
    return {
      fraction,
      start: segmentStart,
      color: getColor(i),
      label: point.label,
      value: point.value,
    };
  });

  // Each segment grows as the global progress sweeps through it
  const totalAngleDone = progress; // progress goes 0→1 covering full donut

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 32 }}>
      <svg width={size} height={size} style={{ overflow: "visible" }}>
        {/* Background circle */}
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={`${textColor}12`}
          strokeWidth={strokeWidth}
        />

        {/* Segments */}
        {segments.map((seg, i) => {
          // How much of this segment has been "drawn"
          const segProgress = Math.max(
            0,
            Math.min(
              1,
              (totalAngleDone - seg.start) / seg.fraction
            )
          );
          const dashLength = segProgress * seg.fraction * circumference;
          // offset: rotate so segment starts at the right angle
          // SVG strokes start at 3 o'clock, we want to start at 12 o'clock
          const rotationOffset = -(circumference / 4); // shift to 12 o'clock
          const segmentOffset = -seg.start * circumference; // shift to segment start
          const dashOffset = rotationOffset + segmentOffset;

          return (
            <circle
              key={i}
              cx={cx}
              cy={cy}
              r={r}
              fill="none"
              stroke={seg.color}
              strokeWidth={strokeWidth - 2}
              strokeDasharray={`${dashLength} ${circumference}`}
              strokeDashoffset={dashOffset}
              strokeLinecap="round"
            />
          );
        })}

        {/* Center hole effect */}
        <circle cx={cx} cy={cy} r={innerR - 4} fill="transparent" />
      </svg>

      {/* Legend */}
      {(showLabels || showValues) && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 10,
          }}
        >
          {segments.map((seg, i) => {
            const labelOpacity = interpolate(
              Math.max(0, totalAngleDone - seg.start),
              [0, 0.1],
              [0, 1],
              { extrapolateRight: "clamp" }
            );
            const percentage = Math.round(seg.fraction * 100 * progress);

            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  opacity: labelOpacity,
                }}
              >
                <div
                  style={{
                    width: 12,
                    height: 12,
                    borderRadius: 3,
                    background: seg.color,
                    flexShrink: 0,
                  }}
                />
                <div
                  style={{
                    fontFamily:
                      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                    fontSize: 13,
                    color: textColor,
                    fontWeight: 500,
                  }}
                >
                  {showLabels && seg.label}
                  {showLabels && showValues && " "}
                  {showValues && (
                    <span style={{ opacity: 0.65 }}>{percentage}%</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
