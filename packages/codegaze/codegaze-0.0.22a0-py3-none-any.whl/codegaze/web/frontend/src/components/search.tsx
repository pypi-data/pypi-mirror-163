import {
  ExclamationIcon,
  InformationCircleIcon,
} from "@heroicons/react/outline";
import * as React from "react";
import Icon from "./icons";
import { appContext } from "../hooks/provider";

interface ISearchResult {
  trackingId: string;
  name: string;
  date: string;
  type: string;
  sessionId: string;
}

const SearchView = () => {
  const serverUrl = process.env.GATSBY_SERVER_URL;
  const trackingUrl = serverUrl + "telemetry/tracking/";
  const [searchResults, setSearchResults] = React.useState<
    ISearchResult[] | null
  >(null);
  const [trackingId, setTrackingId] = React.useState<string>(
    "bbf42be08e4e9b23724dd77e457790f98572ce2679a19292503abe9e7604478a"
  );
  const trackingInputRef = React.useRef<HTMLInputElement>(null);
  const [events, setEvents] = React.useState<{ [fieldName: string]: string }>(
    {}
  );
  const [numEvents, setNumEvents] = React.useState<number>(0);
  const [loading, setLoading] = React.useState<boolean>(false);
  const [error, setError] = React.useState<string | null>(null);
  const { user } = React.useContext(appContext);

  function fetchResults(trackingId: string, limit = 50) {
    const trackingQueryUrl = trackingUrl + trackingId + "/" + limit;
    setLoading(true);
    setError(null);
    fetch(trackingQueryUrl, {
      method: "GET",
      headers: {
        Authorization: "Bearer token=" + user.token,
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        setLoading(false);
        return response.json();
      })
      .then((response) => {
        // console.log(response);
        if (response.status === "success") {
          const data = response.data;
          setSearchResults(data);
          const eventHolder: any = {};
          let numEventsHolder = 0;
          data.forEach((event: any) => {
            event.sessionData.forEach((el: { event_name: string | number }) => {
              // eventHolder.push(el.event_name);
              if (eventHolder[el.event_name]) {
                eventHolder[el.event_name] = eventHolder[el.event_name] + 1;
              } else {
                eventHolder[el.event_name] = 1;
              }
              numEventsHolder++;
            });
          });
          // console.log(eventHolder);
          setEvents(eventHolder);
          setNumEvents(numEventsHolder);
        } else {
          setSearchResults(null);
          setError(response.statusText);
        }
      });
  }

  function truncateText(text: string, length = 50) {
    if (text.length > length) {
      return text.substring(0, length) + "...";
    }
    return text;
  }

  const eventCountView = Object.keys(events).map(
    (eventName: string, i: number) => {
      return (
        <div
          className="text-xs inline-block mr-2 bg-gray-100 rounded mb-1"
          key={eventName + i}
        >
          <span className="px-2 inline-block bg-green-600 rounded-r-none text-white rounded p-1 mr-1">
            {events[eventName]}
          </span>
          <span className="p-1 inline-block pr-2">{eventName}</span>
        </div>
      );
    }
  );

  const trackignIdView = searchResults?.map((data: any, i: number) => {
    return (
      <div className="bg-gray-100 p-3 rounded" key={"row" + i}>
        {" "}
        {data.date}
        <div className="mt-2 text-sm text-gray-500 break-words">
          <div className="text-xs">
            <span className="pr-2 font-semibold text-green-700">
              session id:
            </span>
            {truncateText(data.sessionId, 40)}
          </div>
          <div>
            <span className="bg-gray-300 p-1 px-2 mt-1 inline-block rounded ">
              {data.sessionData.length}
            </span>{" "}
            events{" "}
          </div>
        </div>
      </div>
    );
  });

  return (
    <div>
      <div className="border border-gray-50 p-3 rounded flex shadow-lg">
        <input
          className="w-full p-3 text-gray-500 rounded border border-gray-200 inline-block rounded-r-none"
          placeholder="Enter trackingId"
          type={"text"}
          defaultValue={trackingId}
          ref={trackingInputRef}
        />
        <input
          type={"button"}
          value={"Search"}
          className=" p-3 px-5 rounded   bg-green-600 rounded-l-none text-white"
          onClick={(e) => {
            // setSearchResults(dummyData)
            const curretValue = trackingInputRef.current!.value;
            setTrackingId(curretValue);
            fetchResults(curretValue);
          }}
        />
      </div>

      {loading && (
        <div className="my-3 p-3 border text-sm text-gray-500 border-green-400 rounded">
          {" "}
          <span className="mr-2 inline-block animate-spin">
            <Icon icon="loading" size={6} />
          </span>{" "}
          loading telemetry from database for user{" "}
          {truncateText(trackingId, 10)}
        </div>
      )}
      {searchResults && searchResults.length > 0 && (
        <div className="mt-6">
          <div className="mb-5 border-b pb-5 text-gray-600">
            {" "}
            Found{" "}
            <span className="bg-green-600 text-white p-2 rounded">
              {" "}
              {numEvents}
            </span>{" "}
            Events for TrackingId
            <span className=" text-gray-400 pl-1">
              {truncateText(trackingId, 10)}
            </span>{" "}
          </div>
          <div className="border rounded p-3">{eventCountView}</div>
          <div className="border rounded mt-6 p-2 grid grid-cols-4 gap-3 ">
            {trackignIdView}
          </div>
        </div>
      )}

      {searchResults && searchResults.length === 0 && trackingId && (
        <div className="my-6 p-5 bordper text-sm bg-gray-100 text-orange-600  border-green-200 rounded">
          <ExclamationIcon className="w-4 text-orange-600 h-4 mr-2 inline-block" />{" "}
          No results found for TrackingId{" "}
          <span className="text-gray-400">{trackingId}</span>
        </div>
      )}

      {error && (
        <div className="my-6 p-5 bordper text-sm bg-gray-100 text-orange-600  border-green-200 rounded">
          <ExclamationIcon className="w-4 text-orange-600 h-4 mr-2 inline-block" />{" "}
          <span className="text-gray-400">{error}</span>
        </div>
      )}
    </div>
  );
};

export default SearchView;
