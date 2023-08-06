import { QrcodeIcon } from "@heroicons/react/outline";
import { Empty, List } from "antd";
import React, { useEffect } from "react";
import { Card, CollapseBox } from "../../atoms";
// import "./codeblock.css";

export const ModelCards = ({ results, showMetrics = true }: any) => {
  const MetricsView = ({ data, metricType }: any) => {
    const view = Object.keys(data).map((metric, i) => {
      const combinedMetric = [metricType, metric].join(":");
      const rowClass = " border-b border-dashed";
      return (
        <div className={`${rowClass} rounded pl-2 pb-1 pt-1 text-xs `} key={i}>
          <span className="text-gray-500"> {metric}: </span>
          <span className="font-semibold">{data[metric].toFixed(5)}</span>
        </div>
      );
    });
    return <div className="">{view}</div>;
  };

  const ModelMetricsView = ({ data }: any) => {
    const view = Object.keys(data).map((metricType, i) => {
      return (
        <div className={`rounded pl-2 pb-1 pt-1 text-xs `} key={i}>
          <div className="text-gray-500 pb-1 border-b "> {metricType} </div>
          <MetricsView data={data[metricType]} metricType={metricType} />
        </div>
      );
    });
    return <div className="">{view}</div>;
  };

  const ModelCard = ({ data, i }: any) => {
    return (
      <div key={"row" + i}>
        <Card
          cursor={""}
          hoverable={false}
          title={
            <div className="text-xl mb-2 text-gray-500">
              {" "}
              <QrcodeIcon className="mr-1 inline-block h-5 w-5" /> {i + 1}
              <span className="mr-2 ml-1">|</span>
              {data.model.name}
            </div>
          }
          subtitle={
            <div>
              <div className="mb-2">
                <div className="border inline-block text-xs border-yellow-600 rounded p-1 px-2">
                  {data.model.type}
                </div>
                <div className="mt-1   text-xs  rounded  py-1">
                  {data.model.description}.
                </div>

                <div className="mt-1   text-xs  rounded ">
                  Temperature:{data.model.temperature}
                </div>
              </div>
              <CollapseBox className="p-2" title={"Metrics"} open={showMetrics}>
                <ModelMetricsView data={data.metrics} />
              </CollapseBox>
            </div>
          }
          // active={data.model.name === selectedModel}
        />
      </div>
    );
  };

  return (
    <div>
      {results && results.length > 0 && (
        <div className=" ">
          <div className="mb-2"> Models and metrics.</div>
          <List
            locale={{
              emptyText: <Empty description="No results found" />,
            }}
            className=""
            grid={{
              gutter: 16,
              xs: 1,
              sm: 2,
              md: 4,
              lg: 4,
              xl: 5,
              xxl: 6,
            }}
            dataSource={results}
            renderItem={(item, i) => (
              <List.Item>
                {" "}
                <ModelCard data={item} i={i} />{" "}
              </List.Item>
            )}
            pagination={{
              pageSize: 10,
              size: "small",
              hideOnSinglePage: true,
            }}
          />
        </div>
      )}
    </div>
  );
};
