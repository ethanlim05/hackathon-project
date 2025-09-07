import React from "react";

export default function ProgressBar({ currentStep, totalSteps }) {
  const pct = Math.max(0, Math.min(100, Math.round((currentStep / totalSteps) * 100)));
  return (
    <div className="progress-wrapper">
      <div className="progress-fill" style={{ width: `${pct}%` }} />
    </div>
  );
}
