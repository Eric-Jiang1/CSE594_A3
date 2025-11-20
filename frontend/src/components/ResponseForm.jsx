import React, { useState } from "react";

export default function ResponseForm({ onSubmit }) {
  const [label, setLabel] = useState(null);
  const [confidence, setConfidence] = useState(5);
  const [startTime] = useState(Date.now());

  function handleSubmit() {
    if (!label) return alert("Please choose real or fake!");

    const time = Date.now() - startTime;

    onSubmit({ label, confidence, time });
  }

  return (
    <div className="response-form">
      <h3>Your Judgement</h3>

      <div>
        <button onClick={() => setLabel("real")} className={label === "real" ? "selected" : ""}>
          Real
        </button>
        <button onClick={() => setLabel("fake")} className={label === "fake" ? "selected" : ""}>
          Fake
        </button>
      </div>

      <div style={{ marginTop: 20 }}>
        <p>Confidence: {confidence}</p>
        <input
          type="range"
          min="1"
          max="10"
          value={confidence}
          onChange={(e) => setConfidence(Number(e.target.value))}
        />
      </div>

      <button 
        style={{ marginTop: 20 }} 
        onClick={handleSubmit}
        disabled={!label}
        className={!label ? "disabled" : ""}
      >
        Next
      </button>
    
    </div>
  );
}
