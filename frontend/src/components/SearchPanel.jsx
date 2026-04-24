import { useState } from "react";
import { TextInput, Button, GroupBox } from "react95";

export default function SearchPanel({ onSearch, onClear, loading }) {
  const [musicalVibeDescription, setMusicalVibeDescription] = useState("");

  return (
    <GroupBox label="Search">
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <span>Describe your vibe:</span>
        <TextInput
          value={musicalVibeDescription}
          onChange={(e) => setMusicalVibeDescription(e.target.value)}
          placeholder="e.g. chill study music..."
          style={{ flex: 1 }}
        />
        <Button onClick={() => onSearch(musicalVibeDescription)} disabled={loading}>
          {loading ? "Searching..." : "Find Songs"}
        </Button>
        <Button
          onClick={() => {
            setMusicalVibeDescription("");
            onClear();
          }}
        >
          Clear
        </Button>
      </div>
    </GroupBox>
  );
}
