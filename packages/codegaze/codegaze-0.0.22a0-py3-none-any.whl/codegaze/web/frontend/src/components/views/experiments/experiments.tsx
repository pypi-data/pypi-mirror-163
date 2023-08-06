import * as React from "react";
import { Empty, List } from "antd";
import { loadJSONData } from "../../utils";
import { Card, LoadBox, SectionHeader } from "../../atoms";
import ExperimentResultView from "./results";
import { BeakerIcon } from "@heroicons/react/outline";
import { log } from "console";

const ExperimentView = () => {
  const serverUrl = process.env.GATSBY_API_URL;
  const [experiments, setExperiments] = React.useState([]);
  const [selectedExperiment, setSelectedExperiment] = React.useState(0);
  const [experimentResults, setExperimentResults] = React.useState({});
  const [configLoading, setConfigLoading] = React.useState(false);
  const [resultLoading, setResultLoading] = React.useState(true);

  React.useEffect(() => {
    const experimentUrl = `${serverUrl}/experiments`;
    setConfigLoading(true);
    loadJSONData(experimentUrl)
      .then((data) => {
        setConfigLoading(false);
        if (data) {
          setExperiments(data);
          getExperimentResults(data[selectedExperiment]);
          // console.log("data", data);
        }
      })
      .catch((err) => {
        console.log("err", err);
      });
  }, []);

  function getExperimentResults(config: any) {
    // setExperimentResults({});
    const resultsUrl = `${serverUrl}/experiment/results`;
    const postData = {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    };
    setResultLoading(true);
    loadJSONData(resultsUrl, postData)
      .then((data) => {
        setResultLoading(false);

        if (data) {
          setExperimentResults(data);
        }
      })
      .catch((err) => {
        console.log("err", err);
        setExperimentResults({});
        setResultLoading(false);
      });
  }

  const ExperimentCard = ({ config, i }: any) => {
    const description = `dataset: ${config.dataset} `;
    return (
      <div
        onClick={() => {
          setSelectedExperiment(i);
          getExperimentResults(config);
        }}
        key={"row" + i}
      >
        <Card
          title={config.name}
          subtitle={
            <>
              <div>{config.description}</div>
              <div className="mt-1">{description}</div>
            </>
          }
          active={i === selectedExperiment}
        />
      </div>
    );
  };
  return (
    <div className="">
      <SectionHeader
        icon={
          <BeakerIcon className="inline-block h-7 text-green-600 -mt-1 mr-1" />
        }
        count={experiments?.length || 0}
        title={experiments.length === 1 ? "Experiment" : "Experiments"}
      ></SectionHeader>

      {configLoading && (
        <LoadBox subtitle={"loading experiment configs"} padding={"pb-4"} />
      )}
      <div>
        <List
          locale={{ emptyText: <Empty description="No experiments found" /> }}
          className=""
          grid={{
            gutter: 16,
            xs: 1,
            sm: 2,
            md: 4,
            lg: 4,
            xl: 6,
            xxl: 8,
          }}
          dataSource={experiments}
          renderItem={(item, i) => (
            <List.Item>
              <ExperimentCard config={item} i={i} />
            </List.Item>
          )}
          pagination={{
            pageSize: 20,
            size: "small",
            hideOnSinglePage: true,
          }}
        />
      </div>
      {resultLoading && (
        <LoadBox subtitle={"loading experiment results"} padding={"pb-4"} />
      )}
      {experimentResults && !resultLoading && (
        <div className="">
          <ExperimentResultView
            results={experimentResults.results}
            config={experiments[selectedExperiment]}
            rankings={experimentResults.rankings}
          />
        </div>
      )}
    </div>
  );
};
export default ExperimentView;
