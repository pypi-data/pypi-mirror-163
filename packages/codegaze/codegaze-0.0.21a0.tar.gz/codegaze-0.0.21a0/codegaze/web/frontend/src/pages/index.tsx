import * as React from "react";
import SearchView from "../components/search";
import Layout from "../components/layout";
import { graphql } from "gatsby";
import ExperimentView from "../components/views/experiments/experiments";
import DatasetView from "../components/views/datasets";
import { Alert } from "antd";
import { MessageBox } from "../components/atoms";

// markup
const IndexPage = ({ data }) => {
  const pageTitle = "Dashboard";
  return (
    <Layout meta={data.site.siteMetadata} title="Home" link={"/"}>
      <main className="">
        <div className="mb-6">
          <MessageBox title={`Welcome to ${data.site.siteMetadata.title}`}>
            <div>
              CodeGaze is a tool for evaluating and benchmarking code generation
              models on datasets. You can run experiments and view performance
              (ranking) for all dataset, models and metrics in the experiment.
              Note: CodeGaze is still in Beta and may contain bugs, contact
              Victor to share
              <a href="#">feedback</a>.
            </div>
          </MessageBox>
        </div>
        <DatasetView />
        <ExperimentView />
      </main>
    </Layout>
  );
};

export const query = graphql`
  query HomePageQuery {
    site {
      siteMetadata {
        description
        title
      }
    }
  }
`;

export default IndexPage;
