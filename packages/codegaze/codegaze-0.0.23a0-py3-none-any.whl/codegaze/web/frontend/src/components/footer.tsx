import * as React from "react";
import Icon from "./icons";

const Footer = () => {
  return (
    <div className="mt-4 text-gray-500 p-3  mb-6 border-t   bg-opacity-70 bg-white ">
      <div>
        <span className="text-green-500">
          {" "}
          <Icon icon="app" size={4} />
        </span>{" "}
        Built and maintained by the HAX team @MSR.{" "}
      </div>
    </div>
  );
};
export default Footer;
