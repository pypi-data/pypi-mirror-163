import { BeakerIcon, DatabaseIcon, QrcodeIcon } from "@heroicons/react/outline";
import { Empty, List, Select, Slider } from "antd";
import * as React from "react";
import { LoadBox, SectionHeader } from "../../atoms";
import { loadJSONData, truncateText } from "../../utils";
import { ModelSelectorView } from "../experiments/metricselector";
import DataExplorerView from "./dataexplorer";

const { Option } = Select;
const SelectorView = ({ data }: any) => {
  const serverUrl = process.env.GATSBY_API_URL;

  const [datasets, setDatasets] = React.useState([]);
  const [selectedDataset, setSelectedDataset] = React.useState(0);
  const [experiments, setExperiments] = React.useState([]);
  const [selectedExperiment, setSelectedExperiment] = React.useState(0);
  const [experimentResults, setExperimentResults] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(false);
  const [models, setModels] = React.useState([]);
  const [selectedModel, setSelectedModel] = React.useState(0);
  const [selectedMetric, setSelectedMetric] = React.useState("");

  React.useEffect(() => {
    fetchExperiments(datasets[selectedDataset]);
  }, [datasets, selectedDataset]);

  React.useEffect(() => {
    // getExperimentResults(experiments[selectedExperiment]);
    if (experiments[selectedExperiment]) {
      getExperimentResults(experiments[selectedExperiment]);
    }
  }, [experiments, selectedExperiment]);

  React.useEffect(() => {
    if (experimentResults) {
      setModels(experimentResults.results.map((x: any) => x.model));
    }
  }, [experimentResults]);

  const agg: any = {};
  let maxAgg = 0;
  let minAgg = 10000;
  let metricAgg = {};

  if (experimentResults) {
    const rankings = experimentResults?.rankings;
    for (const ranking of Object.keys(rankings)) {
      for (const metric of rankings[ranking]) {
        const aggreement = rankings[ranking].length;
        agg[metric] = aggreement;
        if (aggreement > maxAgg) {
          maxAgg = aggreement;
        }
        if (aggreement < minAgg) {
          minAgg = aggreement;
        }
      }
    }
    metricAgg = { agg: agg, minAgg: minAgg, maxAgg: maxAgg };
  }

  React.useEffect(() => {
    const datasetUrl = `${serverUrl}/datasets`;
    setLoading(true);
    loadJSONData(datasetUrl)
      .then((data) => {
        setLoading(false);
        if (data) {
          setDatasets(data);
        }
      })
      .catch((err) => {
        setLoading(false);
        console.log("err", err);
      });
  }, []);

  const fetchExperiments = (dataset: any) => {
    const experimentUrl = `${serverUrl}/experiments`;
    const params: any = {
      dataset: dataset,
    };
    var url = experimentUrl + "?" + new URLSearchParams(params);
    setLoading(true);
    loadJSONData(url)
      .then((data) => {
        setLoading(false);
        if (data) {
          setExperiments(data);
          // getExperimentResults(data[0]);
          // setSelectedExperiment(data[0].slug);
        }
      })
      .catch((err) => {
        setLoading(false);
        console.log("err", err);
      });
  };

  function getExperimentResults(config: any) {
    setLoading(true);
    const resultsUrl = `${serverUrl}/experiment/results`;
    const postData = {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    };
    // setResultLoading(true);
    loadJSONData(resultsUrl, postData)
      .then((data) => {
        setLoading(false);
        if (data) {
          setExperimentResults(data);
        }
      })
      .catch((err) => {
        console.log("err", err);
        setExperimentResults({});
        setLoading(false);
      });
  }

  const SelectorBox = ({ data = [], title, selected, setSelected }: any) => {
    return (
      <div className="">
        <div className=" mb-2 text-gray-500">{title}</div>
        <Select
          defaultValue={data[selected].split(":")[0]}
          style={{
            minWidth: 120,
            borderRadius: "5px",
          }}
          className="rounded"
          onChange={(value) => {
            setSelected(value.split(":")[1]);
          }}
        >
          {data.map((item: any, i: number) => {
            return (
              <Option key={i} value={item}>
                {item.split(":")[0]}
              </Option>
            );
          })}
        </Select>
      </div>
    );
  };
  // console.log(models[selectedModel]);

  return (
    <div className="mpb-4 pb-4">
      {loading && <LoadBox subtitle={"fetching data"} />}
      <div className="rounded bg-gray-50 flex gap-4 p-3">
        {datasets.length > 0 && (
          <>
            <SelectorBox
              data={datasets.map((x, i) => x + ":" + i)}
              title={
                <>
                  {" "}
                  <DatabaseIcon className="inline-block h-5 text-green-600 -mt-1 mr-1" />{" "}
                  Datasets
                </>
              }
              selected={selectedDataset}
              setSelected={setSelectedDataset}
            />
          </>
        )}
        {experiments.length > 0 && (
          <SelectorBox
            data={experiments.map(
              (x: any, i: number) => truncateText(x.slug, 20) + ":" + i
            )}
            title={
              <>
                {" "}
                <BeakerIcon className="inline-block h-5 text-green-600 -mt-1 mr-1" />{" "}
                Experiments
              </>
            }
            // selected={setSelectedExperiment}
            selected={selectedExperiment}
            setSelected={setSelectedExperiment}
          />
        )}

        {experimentResults && models.length > 0 && (
          <SelectorBox
            data={models.map(
              (x: any, i: number) => truncateText(x.name, 20) + ":" + i
            )}
            title={
              <>
                {" "}
                <QrcodeIcon className="inline-block h-5 text-green-600 -mt-1 mr-1" />{" "}
                Model
              </>
            }
            selected={selectedModel}
            setSelected={setSelectedModel}
          />
        )}
      </div>
      {/* {models && (
        <div className="mt-4">
          {" "}
          {datasets[selectedDataset]} | {experiments[selectedExperiment]?.slug}|{" "}
          {models[selectedModel] | selectedModel}
        </div>
      )} */}
      {experimentResults && (
        <>
          <div className="py-3 ">
            <ModelSelectorView
              data={experimentResults.results[0].metrics}
              metricAgg={metricAgg}
              selectedMetric={selectedMetric}
              setSelectedMetric={setSelectedMetric}
            />
          </div>

          <div>
            {selectedMetric && (
              <DataExplorerView
                config={experiments[selectedExperiment]}
                selectedMetric={selectedMetric}
                model={models[selectedModel]}
              />
            )}
          </div>
        </>
      )}
    </div>
  );
};
export default SelectorView;
