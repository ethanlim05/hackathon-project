import React, { useMemo } from "react";

function deriveFromNRIC(nric){
  const n = (nric || "").replace(/[^0-9]/g, "");
  if (n.length !== 12) return { gender: "Unknown", dobISO: "" };
  const yy=n.slice(0,2), mm=n.slice(2,4), dd=n.slice(4,6);
  const now = new Date(); const cy = String(now.getFullYear()).slice(2);
  const century = Number(yy) > Number(cy) ? "19" : "20";
  const dobISO = `${century}${yy}-${mm}-${dd}`;
  const gender = Number(n[n.length-1]) % 2 === 1 ? "Male" : "Female";
  return { gender, dobISO };
}

export default function PersonalSection({ t, personal, setPersonal }) {
  const idType = personal.idType || "NRIC"; // 'NRIC' | 'Passport' | 'BRN'
  const idValue = personal.idValue || "";

  const derived = useMemo(()=> idType==="NRIC" ? deriveFromNRIC(idValue) : { gender:"Unknown", dobISO:"" }, [idType, idValue]);

  function setField(k, v){ setPersonal(p => ({ ...p, [k]: v })); }
  function setIdType(v){ setPersonal(p => ({ ...p, idType: v, idValue: "" })); }

  return (
    <div className="personal">
      {/* ID Type Switcher */}
      <div className="row-3">
        <div className="field">
          <label>Identification Type</label>
          <select value={idType} onChange={(e)=>setIdType(e.target.value)}>
            <option>NRIC</option>
            <option>Passport</option>
            <option value="BRN">Business Reg No.</option>
          </select>
        </div>
        <div className="field">
          <label>{idType === "NRIC" ? "NRIC" : idType === "Passport" ? "Passport No." : "Business Reg No. (SSM)"}</label>
          <input
            value={idValue}
            onChange={(e)=>setField('idValue', e.target.value)}
            placeholder={idType === "NRIC" ? "12 digits" : idType === "Passport" ? "e.g., A1234567" : "e.g., 201901234567"}
          />
          {idType === "NRIC" && (
            <div className="small">Gender: {derived.gender}{derived.dobISO ? ` • DOB: ${derived.dobISO}` : ""}</div>
          )}
        </div>
        <div className="field">
          <label>Mobile Number</label>
          <input value={personal.phone || ""} onChange={(e)=>setField('phone', e.target.value)} placeholder="e.g., 01X-XXXXXXX" />
        </div>
      </div>

      <div className="row-2" style={{ marginTop: 10 }}>
        <div className="field">
          <label>Full Name (as per ID)</label>
          <input value={personal.fullName || ""} onChange={(e)=>setField('fullName', e.target.value)} />
        </div>
        <div className="field">
          <label>Email</label>
          <input value={personal.email || ""} onChange={(e)=>setField('email', e.target.value)} placeholder="you@email.com" />
        </div>
      </div>

      <div className="field" style={{ marginTop: 10 }}>
        <label>Address</label>
        <input value={personal.addressLine1 || ""} onChange={(e)=>setField('addressLine1', e.target.value)} />
      </div>

      <div className="row-3" style={{ marginTop: 10 }}>
        <div className="field">
          <label>Postcode</label>
          <input value={personal.postcode || ""} onChange={(e)=>setField('postcode', e.target.value)} />
        </div>
        <div className="field">
          <label>City</label>
          <input value={personal.city || ""} onChange={(e)=>setField('city', e.target.value)} />
        </div>
        <div className="field">
          <label>State</label>
          <input value={personal.state || ""} onChange={(e)=>setField('state', e.target.value)} />
        </div>
      </div>

      <div className="row-2" style={{ marginTop: 10 }}>
        <div className="field">
          <label>E-Hailing?</label>
          <select value={personal.eHailing ? "Yes" : "No"} onChange={(e)=>setField('eHailing', e.target.value === "Yes")}>
            <option>No</option><option>Yes</option>
          </select>
        </div>
        <div className="field">
          <label>Notes (optional)</label>
          <input value={personal.note || ""} onChange={(e)=>setField('note', e.target.value)} placeholder="Anything we should know?" />
        </div>
      </div>
    </div>
  );
}
