import { useState } from "react";
import { Window, WindowHeader, WindowContent, Separator, Frame } from "react95";
import SearchPanel from "./components/SearchPanel";
import ResultsTable from "./components/ResultsTable";

export default function App() {
  const [results, setResults] = useState([]);
  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("Ready.");

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

  return (
    <div style={{ display: "flex", justifyContent: "center", padding: 40 }}>
      <Window style={{ width: "calc(100vw - 80px)" }}>
        <WindowHeader>Recster 1.0</WindowHeader>
        <WindowContent>
          <SearchPanel
            onSearch={handleSearch}
            onClear={() => {
              setResults([]);
              setStatus("Ready.");
            }}
            loading={loading}
          />
          <Separator />
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
