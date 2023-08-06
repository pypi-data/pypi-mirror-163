import { Empty, List, Slider } from "antd";
import * as React from "react";
import { Card, CollapseBox, LoadBox } from "../../atoms";
import { loadJSONData } from "../../utils";
import { CodeBlock } from "./codeblock";
import { interpolateRgb } from "d3-interpolate";

const DataExplorerView = ({ config, selectedMetric, model }: any) => {
  const serverUrl = process.env.GATSBY_API_URL;

  const problemsUrl = `${serverUrl}/experiment/problems`;
  const problemCompletionsUrl = `${serverUrl}/experiment/problem/results`;

  const [selectedProblem, setSelectedProblem] = React.useState(0);
  const [dataLoading, setDataLoading] = React.useState(false);
  const [completionLoading, setCompletionLoading] = React.useState(false);
  const [problems, setProblems] = React.useState([]);
  const [problemCompletions, setProblemCompletions] = React.useState(undefined);
  const [selectedCompletion, setSelectedCompletion] = React.useState(0);
  const [minMetric, setMinMetric] = React.useState(0);
  const [maxMetric, setMaxMetric] = React.useState(1);

  // const metric = "function";
  // const model = results[0].model;

  const metricType = selectedMetric.split(":")[0];
  const metric = selectedMetric.split(":")[1];

  const colorRange = interpolateRgb("red", "green");

  React.useEffect(() => {
    if (selectedMetric) {
      fetchProblems();
      console.log("Error view loaded. Fetching problems ");
    }
  }, [config.dataset, model]);

  const fetchProblems = () => {
    setDataLoading(true);
    const params: any = { metric_type: metricType, model: model.name };
    var url = problemsUrl + "?" + new URLSearchParams(params);
    const postData = {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    };
    loadJSONData(url, postData).then((data) => {
      setDataLoading(false);
      if (data) {
        // console.log("Got problems", data);
        setProblems(data);
        fetchProblemCompletions(data[selectedProblem]?.name);
      }
    });
  };

  const fetchProblemCompletions = (problem: any) => {
    setCompletionLoading(true);
    // var url = new URL(problemCompletionsUrl);
    const params: any = {
      metric_type: metricType,
      model: model.name,
      problem: problem,
    };
    var url = problemCompletionsUrl + "?" + new URLSearchParams(params);
    const postData = {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    };
    loadJSONData(url, postData)
      .then((data) => {
        setCompletionLoading(false);

        if (data) {
          setProblemCompletions(data);
        }
      })
      .catch((err) => {
        console.log("err", err);
      });
  };

  const CompletionRow = ({ problem, i }: any) => {
    const pass = problem.status;
    const rowClass = pass ? "bg-green-200" : "bg-red-300";
    return (
      <div
        onClick={() => {
          setSelectedCompletion(i);
        }}
        key={"clist" + i}
      >
        <Card
          subtitle={i + " " + (pass ? "pass" : "fail")}
          padding={`${rowClass} px-2 p-1 rounded mb-1 text-gray-500`}
          active={selectedCompletion === i}
        />
      </div>
    );
  };

  const getColor = (metric: number) => {
    if (metric <= 0.3) {
      return "bg-red-600";
    } else if (metric >= 0.3 && metric < 0.8) {
      return "bg-orange-300";
    } else if (metric >= 0.6) {
      return "bg-green-600";
    }
  };

  const ProblemRow = ({ problem, i }: any) => {
    // console.log(problem.metrics[metric], colorRange(problem.metrics[metric]));

    const rowClass = colorRange(problem.metrics[metric]);
    return (
      <div
        onClick={() => {
          setSelectedCompletion(0);
          setSelectedProblem(i);
          fetchProblemCompletions(problem.name);
        }}
        className="mb-1"
      >
        <Card
          active={selectedProblem === i}
          subtitle={
            <div>
              <span
                style={{ backgroundColor: rowClass }}
                className={`${rowClass} rounded-full h-2 w-2 mr-2 inline-block border`}
              ></span>
              {problem.name}
            </div>
          }
          padding={"p-1 px-2"}
        />
      </div>
    );
  };

  const filteredProblems = problems.filter((p: any) => {
    return p.metrics[metric] >= minMetric && p.metrics[metric] <= maxMetric;
  });

  const getOtherMetrics = (metrics: any) => {
    const metricsView = Object.keys(metrics || {}).map(
      (metric: any, i: number) => {
        return (
          <div className="inline-block mr-2" key={"metricrow" + i}>
            {!isNaN(metrics[metric]) && (
              <div className="bg-gray-100 p-1 px-2 mb-1 rounded ">
                {metric} {!isNaN(metrics[metric]) && metrics[metric].toFixed(2)}
              </div>
            )}
          </div>
        );
      }
    );
    return metricsView;
    // return "";
  };

  return (
    <div className="mpb-4 pb-4">
      {/* Select a problem to view completions and solutions. */}

      {dataLoading && (
        <LoadBox
          subtitle={`loading problems for ${metricType} ${metric} metric`}
        />
      )}

      <div className="mb-2">
        Explore completions and results for the
        <span className="font-semiboldm p-1 px-2 bg-gray-100">
          {model.name}
        </span>{" "}
        model when evaluated using the{" "}
        <span className="font-semiboldm p-1 px-2 bg-gray-100">
          {selectedMetric}
        </span>{" "}
        metric. You can change the model and metric above.
      </div>
      <div className="py-3 ">
        {/* <ModelSelectorView
          data={metricData}
          metricAgg={metricAgg}
          selectedMetric={selectedMetric}
          setSelectedMetric={setSelectedMetric}
        /> */}
      </div>

      <div className="mb-2 text-gray-500 p-2 border-b-2 border-gray-300  rounded-b-npone bg-gray-50 rounded ">
        {" "}
        <div className="flex gap-3">
          <div className="bg-gray-100 p-2 rounded flex flex-col">
            <div className="flex-1 text-xl text-center">
              {filteredProblems.length}
            </div>
            <div className="text-xs">problems</div>
          </div>

          <div className="flex-1">
            <div className="mb-2">
              Filter problems by {metric} metric score.
            </div>
            <Slider
              onChange={(e: any) => {
                setMinMetric(e[0]);
                setMaxMetric(e[1]);
              }}
              range={{
                draggableTrack: true,
              }}
              step={0.05}
              max={1}
              min={0}
              defaultValue={[minMetric, maxMetric]}
            />
          </div>
          <div
            style={{ minWidth: "120px" }}
            className="bg-gray-100 p-2 rounded flex flex-col"
          >
            <div className="flex-1 text-xl text-center">
              {minMetric} - {maxMetric}
            </div>
            <div className="text-xs text-center">{metric}</div>
          </div>
        </div>
      </div>

      {problems && problems.length > 0 && (
        <div className="flex   my-4 ">
          <div className="mr-2">
            <div className="mb-2"> Problems</div>
            <List
              locale={{ emptyText: <Empty description="No problems found" /> }}
              className=""
              dataSource={filteredProblems}
              renderItem={(item, i) => <ProblemRow problem={item} i={i} />}
              pagination={{
                pageSize: 15,
                size: "small",
                simple: true,
                hideOnSinglePage: true,
              }}
            />
          </div>
          {filteredProblems.length > 0 && (
            <div className="mr-3">
              <div className="mb-2"> Completions</div>
              {/* {completionListView} */}
              <List
                locale={{
                  emptyText: <Empty description="No completions found" />,
                }}
                className=""
                dataSource={problemCompletions?.completions}
                renderItem={(item, i) => <CompletionRow problem={item} i={i} />}
                pagination={{
                  pageSize: 15,
                  size: "small",
                  simple: true,
                  hideOnSinglePage: true,
                }}
              />
            </div>
          )}

          {filteredProblems.length > 0 &&
            problemCompletions &&
            problemCompletions?.completions && (
              <div className="flex-1 relative ">
                {/* {completionLoading && (
                <div className="absolute bg-white p-2 rounded px-3 w-full">
                  <LoadBox subtitle={"loading completions"} />
                </div>
              )} */}
                <div className=" grid grid-cols-2 gap-4">
                  <div
                    className={completionLoading ? "disabled opacity-90" : ""}
                  >
                    <div className="mb-2"> Completion Details</div>
                    {problemCompletions && (
                      <>
                        <CollapseBox className="" open={true} title={"Prompt"}>
                          <CodeBlock
                            code={problemCompletions?.prompt}
                            language="python"
                          />
                        </CollapseBox>

                        <span className="block mt-2">
                          <CollapseBox
                            className=""
                            open={true}
                            title={"Completion Body"}
                          >
                            {" "}
                            <CodeBlock
                              code={
                                problemCompletions?.completions[
                                  selectedCompletion
                                ]?.completion
                              }
                              language="python"
                            />
                          </CollapseBox>
                        </span>
                      </>
                    )}
                  </div>
                  <div
                    className={completionLoading ? "disabled opacity-90" : ""}
                  >
                    <div className="mb-2"> Canonical Solution</div>

                    <>
                      <CollapseBox className="" open={true} title={"Prompt"}>
                        <CodeBlock
                          code={problemCompletions?.prompt}
                          language="python"
                        />
                      </CollapseBox>

                      <span className="block mt-2">
                        <CollapseBox
                          className=""
                          open={true}
                          title={"Canoical Solution Body"}
                        >
                          <CodeBlock
                            code={problemCompletions?.solution}
                            language="python"
                          />
                        </CollapseBox>
                      </span>
                    </>
                  </div>
                </div>

                <div className="mt-6">
                  <CollapseBox className="" open={true} title={"Test"}>
                    <CodeBlock
                      code={problemCompletions?.test}
                      language="python"
                    />
                  </CollapseBox>
                </div>
                <div className="mt-10">
                  Other metrics :{" "}
                  <div>
                    {getOtherMetrics(
                      problemCompletions?.completions[selectedCompletion]
                        ?.metrics
                    )}
                  </div>
                </div>
              </div>
            )}
        </div>
      )}
    </div>
  );
};

export default DataExplorerView;
