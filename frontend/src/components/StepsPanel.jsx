import { GroupBox } from "react95";

export default function StepsPanel({ steps }) {
  return (
    <GroupBox label="Agent Steps">
      <ol style={{ margin: 0, paddingLeft: 20, fontFamily: "inherit" }}>
        {steps.map((s, i) => (
          <li key={i} style={{ marginBottom: 4 }}>
            <strong>{s.step}</strong>
          </li>
        ))}
      </ol>
    </GroupBox>
  );
}
