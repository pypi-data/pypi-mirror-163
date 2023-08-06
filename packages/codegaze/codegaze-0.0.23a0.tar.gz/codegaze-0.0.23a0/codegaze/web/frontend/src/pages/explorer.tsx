import * as React from "react";
import SearchView from "../components/search";
import Layout from "../components/layout";
import { graphql } from "gatsby";
import ExperimentView from "../components/views/experiments/experiments";
import DatasetView from "../components/views/datasets";
import { Alert } from "antd";
import { MessageBox } from "../components/atoms";
import DataExplorer from "../components/views/dataexplorer";

// markup
const DataExplorePage = ({ data }: any) => {
  const pageTitle = "Data Explorer";
  return (
    <Layout
      meta={data.site.siteMetadata}
      link={"/explorer"}
      title="Data Explorer"
    >
      <main className="">
        <div className="mb-6">
          {/* <MessageBox title={`Welcome to ${data.site.siteMetadata.title}`}>
            <div>
              Explore data view
              <a href="#">here</a>.
            </div>
          </MessageBox> */}
        </div>
        <DataExplorer />
        {/* <ExperimentView /> */}
      </main>
    </Layout>
  );
};

export const query = graphql`
  query ExplorePageQuery {
    site {
      siteMetadata {
        description
        title
      }
    }
  }
`;

export default DataExplorePage;
