import {
  Table,
  TableBody,
  TableDataCell,
  TableHead,
  TableHeadCell,
  TableRow,
  ProgressBar,
} from "react95";

function MatchDot({ score, maxScore }) {
  const pct = score / maxScore;
  const color = pct >= 0.8 ? "green" : pct >= 0.55 ? "gold" : "red";
  return <span style={{ color, fontSize: 18, position: "relative", top: "-2px" }}>●</span>;
}

export default function ResultsTable({ results }) {
  if (!results.length) return null;
  const maxScore = results[0]?.max_score ?? 17.5;

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableHeadCell>●</TableHeadCell>
          <TableHeadCell>Title / Artist</TableHeadCell>
          <TableHeadCell>Score</TableHeadCell>
          <TableHeadCell>Energy</TableHeadCell>
          <TableHeadCell>Valence</TableHeadCell>
          <TableHeadCell>Acousticness</TableHeadCell>
          <TableHeadCell>Danceability</TableHeadCell>
          <TableHeadCell>Liveness</TableHeadCell>
          <TableHeadCell>Instrumentalness</TableHeadCell>
          <TableHeadCell>Speechiness</TableHeadCell>
          <TableHeadCell>BPM</TableHeadCell>
          <TableHeadCell>Decade</TableHeadCell>
          <TableHeadCell>Genre / Mood</TableHeadCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {results.map((song) => (
          <TableRow key={song.title}>
            <TableDataCell style={{ verticalAlign: "middle", textAlign: "center", lineHeight: "normal" }}>
              <MatchDot score={song.score} maxScore={maxScore} />
            </TableDataCell>
            <TableDataCell style={{ verticalAlign: "middle", lineHeight: "normal", maxWidth: 200, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {song.title} — {song.artist}
            </TableDataCell>
            <TableDataCell style={{ verticalAlign: "middle", lineHeight: "normal" }}>
              {song.score.toFixed(2)}
            </TableDataCell>
            <TableDataCell>
              <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                <ProgressBar value={Math.round(song.energy * 100)} />
              </div>
            </TableDataCell>
            <TableDataCell>
              <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                <ProgressBar value={Math.round(song.valence * 100)} />
              </div>
            </TableDataCell>
            <TableDataCell>
              <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                <ProgressBar value={Math.round(song.acousticness * 100)} />
              </div>
            </TableDataCell>
            <TableDataCell>
              <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                <ProgressBar value={Math.round(song.danceability * 100)} />
              </div>
            </TableDataCell>
            <TableDataCell>
              <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                <ProgressBar value={Math.round(song.liveness * 100)} />
              </div>
            </TableDataCell>
            <TableDataCell>
              <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                <ProgressBar value={Math.round(song.instrumentalness * 100)} />
              </div>
            </TableDataCell>
            <TableDataCell>
              <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                <ProgressBar value={Math.round(song.speechiness * 100)} />
              </div>
            </TableDataCell>
            <TableDataCell style={{ verticalAlign: "middle", textAlign: "center", lineHeight: "normal" }}>{Math.round(song.tempo)}</TableDataCell>
            <TableDataCell style={{ verticalAlign: "middle", textAlign: "center", lineHeight: "normal" }}>{song.release_decade}</TableDataCell>
            <TableDataCell style={{ verticalAlign: "middle", lineHeight: "normal", maxWidth: 140, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {song.genre} / {song.mood}
            </TableDataCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
