import React, { useEffect } from "react";
import { Card } from "../../atoms";
// import "./codeblock.css";

export const ModelSelectorView = ({
  data,
  metricAgg,
  selectedMetric,
  setSelectedMetric,
}: any) => {
  const { agg, minAgg, maxAgg } = metricAgg;

  useEffect(() => {
    // console.log(metricAggreement);
    const metric = `${Object.keys(data)[0]}:${
      Object.keys(data[Object.keys(data)[0]])[0]
    }`;
    setSelectedMetric(metric);
  }, []);

  const epsilon = 0.000001;
  const MetricSelectorRow = ({ data, metricType }: any) => {
    const view = Object.keys(data).map((metric: string, i: number) => {
      const combinedMetric = [metricType, metric].join(":");
      const normalizedAgreement =
        (agg[combinedMetric] - minAgg + epsilon) / (maxAgg - minAgg + epsilon);

      return (
        <div
          role={"button"}
          onClick={() => {
            setSelectedMetric(combinedMetric);
          }}
          className="inline-block mr-1 mb-2 select-none"
          key={i}
        >
          <div
            style={{ opacity: normalizedAgreement + 0.2 }}
            className={`h-1 mb-1 rounded bg-green-600`}
          ></div>
          <Card
            active={combinedMetric === selectedMetric}
            subtitle={metric}
            padding={"px-2 p-1"}
          />
        </div>
      );
    });
    return <div className="">{view}</div>;
  };

  const view = Object.keys(data).map((metricType, i) => {
    return (
      <div className={`rounded  pb-1 pt-1 text-xs `} key={i}>
        <>
          <div className="text-gray-500 pb-1 border-dfd ">
            {" "}
            <span className="font-semibold">{metricType}</span> Metrics
          </div>
          <MetricSelectorRow data={data[metricType]} metricType={metricType} />
        </>
      </div>
    );
  });
  return (
    <>
      <div className="text-xs py-1 text-gray-500">
        Bars on each metric indicates how often a metric agrees in ranking with
        other metrics. ( high aggreement{" "}
        <span
          style={{ opacity: 1 }}
          className="p-1 w-6 h-1 inline-block rounded px-2 mt-1  bg-green-600"
        ></span>{" "}
        or low aggreement{" "}
        <span
          // style={{ opacity: 0.4 }}
          className="bg-opacity-30 p-1 w-6 h-1 inline-block rounded px-2 mt-1   bg-green-500"
        ></span>{" "}
        ).
      </div>
      <div className="flex gap-3">{view}</div>
    </>
  );
};
