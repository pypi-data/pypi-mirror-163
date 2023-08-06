import * as React from "react";
import { Empty, List, Switch, Tabs } from "antd";
import { Card, CollapseBox, LoadBox } from "../../atoms";
import { orderBy } from "lodash";
import SankeyPlot from "./sankey";
import { QrcodeIcon, SparklesIcon } from "@heroicons/react/outline";
import DataExplorerView from "./dataexplorer";
import { ModelSelectorView } from "./metricselector";
import { ModelCards } from "./modelcards";
import HeatmapPlot from "./heatmap";
import { Tab } from "@headlessui/react";

const { TabPane } = Tabs;

const ExperimentResultView = ({ results, rankings }: any) => {
  // const [sortedResults, setSortedResults] = React.useState<any[]>([]);
  // const [modelDetails, setModelDetails] = React.useState({});
  // const [selectedModel, setSelectedModel] = React.useState("");
  const [advanced, setAdvanced] = React.useState(false);

  React.useEffect(() => {
    console.log("result view loaded");
  }, [results]);

  console.log("rankings", rankings);

  // agreement ranking and color grading
  const agg: any = {};
  let maxAgg = 0;
  let minAgg = 10000;
  let metricAgg = {};
  let matrixData = [];

  // construct sankey plot data
  let sankeyData: any = [];
  if (results) {
    for (const ranking of Object.keys(rankings)) {
      const models = ranking.split(":");

      for (const metric of rankings[ranking]) {
        const aggreement = rankings[ranking].length;
        agg[metric] = aggreement;
        if (aggreement > maxAgg) {
          maxAgg = aggreement;
        }
        if (aggreement < minAgg) {
          minAgg = aggreement;
        }
        sankeyData.push({
          source: metric,
          target: ranking.split(":").join("\n"),
          value: aggreement,
        });

        for (const [i, model] of models.entries()) {
          matrixData.push({
            metric: metric,
            model: model,
            ranking: i + 1,
          });
        }
      }
    }

    // console.log("models", models);

    sankeyData = orderBy(sankeyData, "value", "desc");
    metricAgg = { agg: agg, minAgg: minAgg, maxAgg: maxAgg };
    console.log(matrixData);

    results.forEach((result: any) => {
      Object.keys(agg).forEach((metric: any) => {
        sankeyData.push({
          source: result.model.name,
          target: metric,
          value: 5,
        });
      });
    });
  }

  const RankingSummary = () => {
    let bestRanking = "";
    let numBestRanking = 0;
    let numMetrcs = 0;

    Object.keys(rankings).forEach((ranking) => {
      if (rankings[ranking].length > numBestRanking) {
        bestRanking = ranking;
        numBestRanking = rankings[ranking].length;
      }
      numMetrcs += rankings[ranking].length;
    });

    const modelDetails: any = {};
    results.forEach((result: any) => {
      modelDetails[result.model.name] = result;
    });

    const rankingResults = bestRanking
      .split(":")
      .map((model) => modelDetails[model]);
    // console.log(results);

    return (
      <div key={"ranking"} className=" mb-8">
        <div className="mb-3 mt-4">
          <span className="text-xl text-gray-600">
            {" "}
            Aggregate Model Ranking
          </span>{" "}
          Based on aggreement of {numBestRanking} out of {numMetrcs} metrics.{" "}
        </div>

        <div className="">
          <ModelCards results={rankingResults} showMetrics={false} />{" "}
        </div>
        <div className="mt-2 text-gray-500 text-xs"> </div>
      </div>
    );
  };

  const MetricModelView = ({ metricAgg, results }: any) => {
    const [selectedMetric, setSelectedMetric] = React.useState("");

    const sortFunction = (a: any, b: any) => {
      for (const metricType of Object.keys(a.metrics)) {
        for (const metric of Object.keys(a.metrics[metricType])) {
          const combinedMetric = [metricType, metric].join(":");
          if (combinedMetric === selectedMetric) {
            return (
              b.metrics[metricType][metric] - a.metrics[metricType][metric]
            );
          }
        }
      }
    };

    return (
      <div>
        <div className="py-3 ">
          <ModelSelectorView
            data={results[0].metrics}
            metricAgg={metricAgg}
            selectedMetric={selectedMetric}
            setSelectedMetric={setSelectedMetric}
          />
        </div>

        {results && (
          <ModelCards
            results={results.sort(sortFunction)}
            showMetrics={false}
          />
        )}
      </div>
    );
  };

  return (
    <div className="">
      {results && results.length == 0 && (
        <LoadBox subtitle={"loading experiment data"} />
      )}
      {results && results.length > 0 && (
        <>
          <div className="mb-3 border-b pb-2">
            <div className="flex">
              <div className="flex-1">
                <span className="text-xl text-gray-600"> Results </span>
                {results?.length} models evaluated.
              </div>
              <div className="hidden    ">
                <span> Advanced view </span>
                <span>
                  {" "}
                  <Switch
                    onChange={() => {
                      setAdvanced(!advanced);
                    }}
                    checked={advanced}
                  />{" "}
                </span>
              </div>
            </div>
          </div>

          {results && results.length > 0 && <RankingSummary />}

          <div className="mb-3 ">
            <span className="text-xl text-gray-600">
              {" "}
              Metrics and Model Rankings
            </span>{" "}
            all metrics and models in experiment.
          </div>

          {results && results.length > 0 && (
            <MetricModelView metricAgg={metricAgg} results={results} />
          )}

          {/* <CollapseBox open={true} title={"Metrics and Model Rankings"}>
           
          </CollapseBox> */}
          <div className="mb-3 ">
            <span className="text-xl text-gray-600">
              {" "}
              Ranking Visualization
            </span>{" "}
            all metrics and models in experiment.
          </div>
          <>
            <div className="mb-2  ">
              Visualization of model ranking by metrics.
            </div>
            {/* <Tabs className="hidden" defaultActiveKey="1">
              <TabPane tab="Ranking Plot" key="1">
                <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
                  <SankeyPlot data={sankeyData} />
                </div>
              </TabPane>
              <TabPane tab="Ranking Matrix" key="2">
                <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
                  <HeatmapPlot data={matrixData} />
                </div>
              </TabPane>
            </Tabs> */}

            <div className="  mb-2  mt-2">
              <div className=" ">
                <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                  <div>
                    <div className="mb-2  ">Modified Sankey diagram</div>

                    <SankeyPlot data={sankeyData} />
                  </div>
                  <div>
                    <div className="mb-2  ">Ranking matrix</div>
                    <HeatmapPlot data={matrixData} />
                  </div>
                </div>
              </div>
            </div>
          </>

          {/* <>
            <div className="mb-2  mt-2">
              <div className=" ">
                <div className="mb-2  ">Heatmap plot</div>
                <div className="grid grid-cols-1 xl:grid-cols-2">
                  <HeatmapPlot data={matrixData} />
                </div>
              </div>
            </div>
          </> */}
        </>
      )}
    </div>
  );
};
export default ExperimentResultView;
