import React, { useEffect, useState } from "react";
import { getRandomPostings, getAIPrediction, submitResponse } from "../api/backend";
import JobCard from "../components/JobCard";
import AIInsight from "../components/AIInsight";
import ResponseForm from "../components/ResponseForm";
import ProgressBar from "../components/ProgressBar";
import { useSearchParams, useNavigate } from "react-router-dom";

export default function Task() {
  const [params] = useSearchParams();
  const navigate = useNavigate();

  const workerId = params.get("workerId") ?? "UNKNOWN";
  const condition = params.get("condition") ?? "baseline";

  const [trials, setTrials] = useState([]);
  const [current, setCurrent] = useState(0);
  const [aiInfo, setAIInfo] = useState(null);
  const [loadingAI, setLoadingAI] = useState(false);

  useEffect(() => {
    async function loadTrials() {
      const data = await getRandomPostings(10);
      setTrials(data);
    }
    loadTrials();
  }, []);

  async function fetchAI(postingId) {
    setLoadingAI(true);
    const result = await getAIPrediction(postingId);
    setAIInfo(result);
    setLoadingAI(false);
  }

  // Automatically fetch AI suggestion when posting changes (if in AI condition)
  useEffect(() => {
    if (condition === "ai" && trials.length > 0 && current < trials.length) {
      const posting = trials[current];
      if (posting && posting.id) {
        fetchAI(posting.id);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [current, trials, condition]);

  async function handleNext(response) {
    const posting = trials[current];

    // submit to backend
    await submitResponse({
      worker_id: workerId,
      posting_id: posting.id,
      condition: condition,
      worker_label: response.label,
      worker_confidence: response.confidence,
      time_on_trial_ms: response.time,
      ai_prediction: aiInfo?.prediction ? (aiInfo.prediction === "real" ? 1.0 : 0.0) : null,
      ai_confidence: aiInfo?.confidence ?? null
    });

    // next trial
    if (current + 1 < trials.length) {
      setCurrent(current + 1);
      setAIInfo(null);
    } else {
      navigate("/complete");
    }
  }

  if (trials.length === 0)
    return <div style={{ padding: 40 }}>Loading trials…</div>;

  const posting = trials[current];

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 20 }}>
      <ProgressBar total={trials.length} index={current} />

      <h2>{posting.title}</h2>
      <JobCard posting={posting} />

      {condition === "ai" && (
        <AIInsight
          key={`ai-${current}`}
          aiInfo={aiInfo}
          loading={loadingAI}
        />
      )}

      <ResponseForm key={`form-${current}`} onSubmit={handleNext} />

    </div>
  );
}
