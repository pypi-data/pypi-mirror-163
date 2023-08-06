import React from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { atomOneDark } from "react-syntax-highlighter/dist/esm/styles/hljs";

// import "./codeblock.css";

interface ICodeProps {
  code: string;
  language: string;
  title?: string;
  showLineNumbers?: boolean;
  className?: string | undefined;
}

export const CodeBlock = ({
  code,
  language = "python",
  showLineNumbers = false,
  className = " ",
}: ICodeProps) => {
  const codeString = code;
  return (
    <>
      <div
        id="codeDivBox"
        className={`rounded   overflow-x-hidden overflow-y-hidden ${className}`}
        // style={{ maxHeight: "680px" }}
      >
        <SyntaxHighlighter
          id="codeDiv"
          className="rounded-sm h-full"
          language={language}
          showLineNumbers={showLineNumbers}
          style={atomOneDark}
          wrapLines={false}
        >
          {codeString}
        </SyntaxHighlighter>
      </div>
    </>
  );
};
