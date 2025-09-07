import React from "react";

export default function CarSection({ t, car, setCar, onValid }) {
  function setField(k, v){ setCar(c => ({ ...c, [k]: v })); }

  return (
    <div className="car">
      <div className="row-3">
        <div className="field">
          <label>Brand</label>
<<<<<<< Updated upstream
          <select value={car.brand || ""} onChange={(e)=>setField('brand', e.target.value)}>
            <option value="">Brand...</option>
            <option value="Perodua">Perodua</option>
            <option value="Proton">Proton</option>
            <option value="Honda">Honda</option>
            <option value="Toyota">Toyota</option>
          </select>
=======
          <input
            placeholder="Brand..."
            value={car.brand || ""}
            onChange={(e)=>setField('brand', e.target.value)}
          />
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
      <div className="right-actions" style={{ marginTop: 18 }}>
        <button className="btn ghost" onClick={()=>window.scrollTo({ top: 0, behavior: 'smooth' })}>{t("back")}</button>
        <button className="btn primary" onClick={onValid}>{t("save_continue")}</button>
      </div>
=======
      {/* Action buttons are handled in App.jsx so they can open confirmation modal */}
>>>>>>> Stashed changes
    </div>
  );
}
