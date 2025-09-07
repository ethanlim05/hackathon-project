import React, { useState } from 'react';
import { verifyPlate } from '../api';
import Modal from './Modal';

export default function PlateSection({ t, plate, setPlate, onVerified, setPrefill, onHelperSelectId }) {
  const [loading, setLoading] = useState(false);
  const [inlineError, setInlineError] = useState("");
  const [selectedHelper, setSelectedHelper] = useState("");  // 'noPlate' | 'passport' | 'company' | ''

  // modals
  const [ownOpen, setOwnOpen] = useState(false);
  const [newOpen, setNewOpen] = useState(false);
  const [last4, setLast4] = useState("");
  const [attempts, setAttempts] = useState(3);
  const [last4Error, setLast4Error] = useState("");
  const [hint, setHint] = useState("");

  const clean = plate.toUpperCase().replace(/\s+/g, '');
  const isValid = /^([A-Z]{1,3}\d{1,4}[A-Z]{0,2})$/.test(clean);

  async function handleVerify() {
    setInlineError("");
    if (!isValid) { setInlineError("Please enter a valid plate number."); return; }
    setLoading(true);
    try {
      const res = await verifyPlate(plate);
      if (res.status === "existing") setOwnOpen(true);
      else setNewOpen(true);
    } catch (e) {
      setInlineError(e.message || "Verification failed.");
    } finally { setLoading(false); }
  }

  async function confirmLast4() {
    try{
      const res = await confirmOwnership(plate, last4);
      if (!res.ok) {
        const left = attempts - 1;
        setAttempts(left);
        setLast4Error(`Invalid IC number. ${left} ${left === 1 ? "try" : "tries"} left`);
        if (left <= 0) { setOwnOpen(false); setInlineError("Too many failed attempts. Please restart verification."); }
        return;
      }
      if (res.personal) setPrefill(res.personal);
      if (res.car) setPrefill(res.car);
      setOwnOpen(false); setAttempts(3); setLast4Error(""); setLast4("");
      onVerified('existing', { plate: clean });
    }catch{ setLast4Error("Something went wrong. Try again."); }
  }

  function chooseHelper(key, msg){
    setSelectedHelper(key);
    setHint(msg);
  }

  return (
    <>
      {/* Input + Verify stay together */}
      <div className="row">
        <div className="field">
          <label>{t("plate_label")}</label>
          <input
            value={plate}
            onChange={(e) => setPlate(e.target.value)}
            placeholder="E.G., BJK1234"
            style={{ textTransform: 'uppercase' }}
          />
          <div className="small">{t("plate_help")}</div>
          {inlineError && <div className="alert" style={{marginTop:8}}>{inlineError}</div>}
        </div>

        <div className="field" style={{ alignSelf: 'end' }}>
          <button className="btn primary" onClick={handleVerify} disabled={!isValid || loading} style={{ minWidth: 170 }}>
            {loading ? 'Verifying…' : t("verify")}
          </button>
        </div>
      </div>

      {/* Helper pills */}
      <div className="helper-links">
      <button
          className={`pill ${selectedHelper==='passport' ? 'active' : ''}`}
          onClick={()=>{
            chooseHelper('passport', "Prefer Passport? Switch ID type in Personal Info.");
            onHelperSelectId && onHelperSelectId("Passport"); // set type, no navigation
          }}
        >
          <span className="dot" /> Use Passport instead of NRIC
        </button>

        <button
          className={`pill ${selectedHelper==='company' ? 'active' : ''}`}
          onClick={()=>{
            chooseHelper('company', "Company vehicle? Use Business Reg No. (SSM) in Personal Info.");
            onHelperSelectId && onHelperSelectId("BRN"); // set type, no navigation
          }}
        >
          <span className="dot" /> Company car (SSM / BRN)
        </button>

        <button
          className={`pill ${selectedHelper==='noPlate' ? 'active' : ''}`}
          onClick={()=>{
            chooseHelper('noPlate', "No plate yet? We’ll register with chassis/engine and update later.");
            onHelperSelectId && onHelperSelectId("NRIC"); // default to NRIC if they pick this
          }}
        >
          <span className="dot" /> No plate yet? Register new car
        </button>

      </div>

      {/* Hint BELOW the pills so it doesn't break the Verify alignment */}
      {hint && <div className="hint-row">{hint}</div>}

      {/* Existing vehicle modal */}
      <Modal
        open={ownOpen}
        title="We found this vehicle"
        onClose={()=>{ setOwnOpen(false); setLast4Error(""); setAttempts(3); }}
        primary={
          <button className="btn primary" onClick={confirmLast4} disabled={String(last4).length !== 4}>
            Continue
          </button>
        }
        secondary={<button className="btn ghost" onClick={()=>setOwnOpen(false)}>Cancel</button>}
      >
        <p className="modal-text">
          Enter the <strong>last 4 digits of the owner’s NRIC</strong> to confirm ownership and prefill your details.
        </p>
        <div className="field" style={{marginTop:10}}>
          <label>Last 4 NRIC digits</label>
          <input
            className={last4Error ? "error" : ""}
            inputMode="numeric" maxLength={4}
            value={last4}
            onChange={(e)=>{ setLast4Error(""); setLast4(e.target.value.replace(/\D/g,'')); }}
            placeholder="XXXX"
          />
          {last4Error && <div className="error-text">{last4Error}</div>}
        </div>
      </Modal>

      {/* New vehicle modal */}
      <Modal
        open={newOpen}
        title="No existing policy found"
        onClose={()=>setNewOpen(false)}
        primary={<button className="btn primary" onClick={()=>{ setNewOpen(false); onVerified('new', { plate: clean }); }}>Start new registration</button>}
        secondary={<button className="btn ghost" onClick={()=>setNewOpen(false)}>Close</button>}
      >
        <p className="modal-text">
          We couldn’t find a matching policy for <strong>{clean}</strong>. You can proceed to create a new insurance application.
        </p>
      </Modal>
    </>
  );
}
