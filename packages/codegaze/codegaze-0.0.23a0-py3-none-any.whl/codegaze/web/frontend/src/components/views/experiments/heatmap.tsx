import { Heatmap } from "@ant-design/charts";
import * as React from "react";

const HeatmapPlot = ({ data }: any) => {
  const config = {
    autoFit: true,
    data,
    xField: "metric",
    yField: "model",
    // sizeField: "ranking",
    // shape: "square",
    colorField: "ranking",
    color: ["#16a34a", "#22c55e", "#4ade80"],
    meta: {
      metric: {
        type: "cat",
      },
    },
    label: {
      style: {
        fill: "#fff",
        shadowBlur: 2,
        shadowColor: "rgba(0, 0, 0, .45)",
      },
    },
  };

  return (
    <div className="">
      <div className="bg-gray-50 rounded ">
        <Heatmap {...config} />
      </div>
    </div>
  );
};
export default HeatmapPlot;
