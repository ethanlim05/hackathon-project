import React from "react";

export default function CarSection({ t, car, setCar, onValid }) {
  function setField(k, v){ setCar(c => ({ ...c, [k]: v })); }

  return (
    <div className="car">
      <div className="row-3">
        <div className="field">
          <label>Brand</label>
          <input
            placeholder="Brand..."
            value={car.brand || ""}
            onChange={(e)=>setField('brand', e.target.value)}
          />
        </div>
        <div className="field">
          <label>Model</label>
          <input value={car.model || ""} onChange={(e)=>setField('model', e.target.value)} placeholder="e.g., Myvi, Saga, City" />
        </div>
        <div className="field">
          <label>Year</label>
          <input value={car.year || ""} onChange={(e)=>setField('year', e.target.value)} placeholder="YYYY" />
        </div>
      </div>

      {/* Buttons are rendered in App.jsx to trigger confirmation modal and validation. */}
    </div>
  );
}
