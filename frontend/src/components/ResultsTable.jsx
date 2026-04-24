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
  return <span style={{ color, fontSize: 18 }}>●</span>;
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
          <TableHeadCell>Tempo BPM</TableHeadCell>
          <TableHeadCell>Genre / Mood</TableHeadCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {results.map((song) => (
          <TableRow key={song.title}>
            <TableDataCell>
              <MatchDot score={song.score} maxScore={maxScore} />
            </TableDataCell>
            <TableDataCell>
              {song.title} — {song.artist}
            </TableDataCell>
            <TableDataCell>
              {song.score} / {maxScore}
            </TableDataCell>
            <TableDataCell>
              <ProgressBar value={Math.round(song.energy * 100)} />
            </TableDataCell>
            <TableDataCell>
              <ProgressBar value={Math.round(song.valence * 100)} />
            </TableDataCell>
            <TableDataCell>
              <ProgressBar value={Math.round(song.acousticness * 100)} />
            </TableDataCell>
            <TableDataCell>{song.tempo}</TableDataCell>
            <TableDataCell>
              {song.genre} / {song.mood}
            </TableDataCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
