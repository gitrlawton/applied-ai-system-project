import { useState } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { Window, WindowHeader, WindowContent, Separator, Frame } from "react95";
import SearchPanel from "./components/SearchPanel";
import ResultsTable from "./components/ResultsTable";
import StepsPanel from "./components/StepsPanel";

export default function App() {
  const [results, setResults] = useState([]);
  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("Ready.");
  const [showSteps, setShowSteps] = useState(false);

  async function handleSearch(musicalVibeDescription) {
    setLoading(true);
    setStatus("Searching...");
    try {
      const res = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: musicalVibeDescription }),
      });
      const data = await res.json();
      setResults(data.recommendations);
      setSteps(data.steps);
      setStatus(`Returned ${data.recommendations.length} results.`);
    } catch (err) {
      setStatus(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function handleStreamingSearch(musicalVibeDescription) {
    setLoading(true);
    setSteps([]);
    setResults([]);
    setStatus("Thinking...");

    await fetchEventSource("/recommend/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: musicalVibeDescription }),
      onmessage(ev) {
        const event = JSON.parse(ev.data);
        if (event.type === "step") {
          setSteps((prev) => [...prev, event]);
        } else if (event.type === "done") {
          setResults(event.recommendations);
          setStatus(`Returned ${event.recommendations.length} results.`);
          setLoading(false);
        }
      },
    });
  }

  return (
    <div style={{ display: "flex", justifyContent: "center", padding: 40 }}>
      <Window style={{ width: "calc(100vw - 80px)" }}>
        <WindowHeader>Recster 1.0</WindowHeader>
        <WindowContent>
          <SearchPanel
            onSearch={showSteps ? handleStreamingSearch : handleSearch}
            onClear={() => {
              setResults([]);
              setSteps([]);
              setStatus("Ready.");
            }}
            loading={loading}
            showSteps={showSteps}
            onToggleSteps={() => setShowSteps((v) => !v)}
          />
          <Separator />
          {showSteps && steps.length > 0 && (
            <>
              <StepsPanel steps={steps} />
              <Separator />
            </>
          )}
          <div style={{ overflowX: "auto" }}>
            <ResultsTable results={results} />
          </div>
          <Separator />
          <Frame variant="status" style={{ padding: "4px 8px" }}>
            {status}
          </Frame>
        </WindowContent>
      </Window>
    </div>
  );
}
