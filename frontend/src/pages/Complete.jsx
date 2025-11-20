import { useNavigate } from "react-router-dom";

export default function Complete() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: 40 }}>
      <h2>Study Complete</h2>
      <p>Thank you for participating!</p>
      <p style={{ marginTop: 20 }}>
        Here's a short post-task survey:{" "}
        <a 
          href="https://forms.gle/M9jf9gjRGyUPtH9M8" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ color: "#646cff" }}
        >
          https://forms.gle/M9jf9gjRGyUPtH9M8
        </a>
      </p>
      <button 
        onClick={() => navigate("/")}
        style={{ marginTop: 20 }}
      >
        Back to Home
      </button>
    </div>
  );
}
  