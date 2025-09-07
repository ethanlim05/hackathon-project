import React from 'react';

export default function Stepper({ active, t }) {
  const steps = [t('step_carPlate'), t('step_personal'), t('step_car'), t('step_funding')];
  return (
    <div className="stepper">
      {steps.map((label, i) => {
        const n = i + 1;
        const isActive = active === i;
        return (
          <div className={`step ${isActive ? 'active' : ''}`} key={label}>
            <div className={`dot ${isActive ? 'active' : ''}`}>{n}</div>
            <span>{label}</span>
          </div>
        );
      })}
    </div>
  );
}
