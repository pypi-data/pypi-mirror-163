import { Sankey } from "@ant-design/charts";
import * as React from "react";

const SankeyPlot = ({ data }: any) => {
  const config = {
    autoFit: true,
    data: data,
    sourceField: "source",
    targetField: "target",
    weightField: "value",
    nodeWidthRatio: 0.008,
    nodePaddingRatio: 0.03,
    color: ["#16a34a"],
  };

  return (
    <div className="">
      <div className="bg-gray-50 rounded ">
        <Sankey {...config} />
      </div>
    </div>
  );
};
export default SankeyPlot;
