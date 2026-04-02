import React from "react";
import { Composition } from "remotion";
import { ReelTips } from "./compositions/ReelTips";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ReelTips"
        component={ReelTips}
        durationInFrames={1260}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          brand: {
            name: "AutomatikLabs",
            handle: "@automatiklabs",
            colors: {
              primary: "#6c5ce7",
              secondary: "#00cec9",
              background: "#0a0a0a",
              text: "#ffffff",
              accent: "#fd79a8",
            },
          },
          scenes: [],
          showProgressBar: true,
          showWatermark: true,
        }}
      />
    </>
  );
};
