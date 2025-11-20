import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  function start(condition) {
    const workerId = `W${Math.floor(Math.random()*9999)}`;
    navigate(`/task?workerId=${workerId}&condition=${condition}`);
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Job Posting Classification Study</h1>
      <p>Click below to begin.</p>

      <button onClick={() => start("baseline")}>Start (Baseline)</button>
      <button onClick={() => start("ai")}>Start (AI-Assisted)</button>
    </div>
  );
}
