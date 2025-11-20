export default function ProgressBar({ total, index }) {
    const pct = ((index + 1) / total) * 100;
    return (
      <div style={{ marginBottom: 20 }}>
        <div style={{ height: 8, background: "#eee" }}>
          <div style={{ width: `${pct}%`, height: 8, background: "#3b82f6" }} />
        </div>
        <p>{index + 1} / {total} completed</p>
      </div>
    );
  }
  