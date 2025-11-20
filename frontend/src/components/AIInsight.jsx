import React, { useState } from "react";

export default function AIInsight({ aiInfo, loading }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="ai-insight">
      <button onClick={() => setOpen(!open)}>
        {open ? "Hide AI Suggestion" : "Show AI Suggestion"}
      </button>

      {open && (
        <div style={{ marginTop: 10, padding: 10, border: "1px solid #ddd" }}>
          {loading && <p>Loading prediction...</p>}

          {!loading && aiInfo && (
            <div>
              <p><strong>AI Prediction:</strong> {aiInfo.prediction}</p>
              <p><strong>Confidence:</strong> {(aiInfo.confidence * 100).toFixed(1)}%</p>
              {aiInfo.reasoning && aiInfo.reasoning.length > 0 && (
                <div style={{ marginTop: 10 }}>
                  <p><strong>Key Reasoning:</strong> {aiInfo.reasoning.join(", ")}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
