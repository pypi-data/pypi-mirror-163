import {
  AdjustmentsIcon,
  BeakerIcon,
  ColorSwatchIcon,
} from "@heroicons/react/outline";
import { Empty, List, Slider } from "antd";
import * as React from "react";
import { SectionHeader } from "../../atoms";
import SelectorView from "./dataselector";

const DataExplorer = ({ data }: any) => {
  return (
    <div className="mpb-4 pb-4">
      <SectionHeader
        icon={
          <ColorSwatchIcon className="inline-block h-7 text-green-600 -mt-1 mr-1" />
        }
        title={"Data Selector"}
      ></SectionHeader>
      <div className="py-2 text-gray-500">
        {" "}
        Select a dataset, experiment and model to view data.{" "}
      </div>
      <SelectorView />
    </div>
  );
};
export default DataExplorer;
