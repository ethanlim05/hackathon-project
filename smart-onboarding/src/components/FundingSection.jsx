import React from 'react';

export default function FundingSection({ t, plate, personal, derived, car, onSubmit, submitting, submitRes }){
  return (
    <div>
      <div className="summary">
        <div><strong>Plate:</strong> {plate.toUpperCase().replace(/\s+/g, '')}</div>
        <div><strong>Name:</strong> {personal.fullName}</div>
        <div><strong>NRIC:</strong> {personal.nric} ({derived.gender}{derived.dobISO ? `, DOB ${derived.dobISO}` : ''})</div>
        <div><strong>Address:</strong> {personal.addressLine1}, {personal.postcode} {personal.city}, {personal.state}</div>
        <div><strong>{t("vehicle")}:</strong> {car.brand} {car.model} ({car.year})</div>
        <div><strong>E-Hailing:</strong> {personal.eHailing ? 'Yes' : 'No'}</div>
      </div>

      <div className="card" style={{ marginTop: 12 }}>
        <div className="small">Funding plan (placeholder): choose to pay in full or monthly. Hook to pricing later.</div>
        <div className="actions">
          <button className="btn">Pay in Full</button>
          <button className="btn">Monthly Plan</button>
        </div>
      </div>

      <div className="actions">
        <span></span>
        <button className="btn primary" onClick={onSubmit} disabled={submitting}>{submitting ? '…' : t("submit")}</button>
      </div>

      {submitRes && (
        <div className="alert" style={{ borderColor: submitRes.ok ? '#c7f9cc' : '#fee2e2', background: submitRes.ok ? '#f0fff4' : '#fef2f2', color: submitRes.ok ? '#065f46' : '#991b1b' }}>
          {submitRes.ok ? (
            <div><strong>{t("submitted")}</strong> Application ID {submitRes.applicationId}</div>
          ) : (
            <div><strong>{t("failed")}</strong> {submitRes.message || 'Please try again.'}</div>
          )}
        </div>
      )}
    </div>
  );
}
