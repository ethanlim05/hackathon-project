import React, { useMemo, useState } from 'react';
import './styles.css';
import Stepper from './components/Stepper';
import { AccordionItem } from './components/Accordion';
import PlateSection from './components/PlateSection';
import PersonalSection from './components/PersonalSection';
import CarSection from './components/CarSection';
import FundingSection from './components/FundingSection';
import Benefits from './components/Benefits';
import Modal from './components/Modal';
import Footer from './components/Footer';
import Header from './components/Header';
import ChatbotWidget from './components/ChatbotWidget';
import ProgressBar from './components/ProgressBar';
import { submitOnboarding } from './api';
import { makeT } from './i18n';

function normalizePlate(v){ return v.toUpperCase().replace(/\s+/g, ''); }
function fmtNRIC(v){ return v.replace(/[^0-9]/g, ''); }
function derive(nric){
  const n = fmtNRIC(nric);
  if (n.length !== 12) return { gender: 'Unknown', dobISO: '' };
  const yy=n.slice(0,2), mm=n.slice(2,4), dd=n.slice(4,6);
  const now = new Date();
  const century = Number(yy) > Number(String(now.getFullYear()).slice(2)) ? '19':'20';
  const dobISO = `${century}${yy}-${mm}-${dd}`;
  const gender = Number(n[n.length-1]) % 2 === 1 ? 'Male':'Female';
  return { gender, dobISO };
}

export default function App(){
  const [lang, setLang] = useState("en");
  const t = useMemo(()=>makeT(lang), [lang]);

  const [openId, setOpenId] = useState('plate');
  const [plate, setPlate] = useState('');
  const [personal, setPersonal] = useState({
    fullName: '', nric: '', email: '', phone: '',
    addressLine1: '', postcode: '', city: '', state: '', eHailing: false
  });
  const [car, setCar] = useState({ brand: '', model: '', year: '' });
  const [submitting, setSubmitting] = useState(false);
  const [submitRes, setSubmitRes] = useState(null);
  const [submittedPersonal, setSubmittedPersonal] = useState(false);
  const [submittedCar, setSubmittedCar] = useState(false);
  const [confirmPersonal, setConfirmPersonal] = useState(false);
  const [confirmCar, setConfirmCar] = useState(false);

  const derived = useMemo(()=>derive(personal.nric), [personal.nric]);
  const stepsOrder = ['plate','personal','car','funding'];
  const activeIndex = stepsOrder.indexOf(openId);   // you already have something like this
  const step = Math.max(1, activeIndex + 1);        // 1..4 for the progress bar
  
  function handleSelectIdType(idType){
    setPersonal(p => ({ ...p, idType, idValue: "" }));  // reset the value when switching
    // open Personal section and scroll into view
    setOpenId("personal");
    requestAnimationFrame(() => {
      const el = document.getElementById("personal-section");
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

    // add near your other setters
  function setIdTypeSilent(idType){
    setPersonal(p => ({ ...p, idType, idValue: "" })); // just set; no navigation
  }
  function handlePlateVerified(){ setOpenId('personal'); }
  function setPrefill(profile){ setPersonal(p=>({ ...p, ...profile })); setCar(c=>({ ...c, ...profile })); }
  function onCarValid(){ setOpenId('funding'); }

  // ---- validators used for confirmation gating ----
  function isValidEmail(v){ return /.+@.+\..+/.test(String(v||'')); }
  function isValidPostcode(v){ return /^\d{5}$/.test(String(v||'')); }
  function isValidMobile(v){ return /^\d{9,12}$/.test(String(v||'').replace(/\D/g, '')); }
  function isValidNRIC(v){
    const d = String(v||'').replace(/\D/g, '');
    if (d.length !== 12) return false;
    const yy = d.slice(0,2), mm = d.slice(2,4), dd = d.slice(4,6);
    const m = Number(mm), day = Number(dd);
    if (m < 1 || m > 12) return false;
    const maxDay = new Date(Number(`20${yy}`), m, 0).getDate();
    return day >= 1 && day <= maxDay;
  }
  function validPersonal(){
    const idOk = personal.idType === 'NRIC' ? isValidNRIC(personal.idValue) : (personal.idValue||'').length>2;
    return (
      (personal.fullName||'').trim().length>1 &&
      idOk && isValidEmail(personal.email) && isValidMobile(personal.phone) &&
      (personal.addressLine1||'').trim().length>3 && isValidPostcode(personal.postcode) &&
      (personal.city||'').trim().length>1 && (personal.state||'').trim().length>1
    );
  }
  function validCar(){
    const y = Number(car.year);
    const okYear = /^\d{4}$/.test(String(car.year||'')) && y>=1990 && y<= new Date().getFullYear()+1;
    return ( (car.brand||'').trim().length>1 && (car.model||'').trim().length>1 && okYear );
  }
  function handlePersonalSave(){
    setSubmittedPersonal(true);
    if (validPersonal()) setConfirmPersonal(true);
    else requestAnimationFrame(()=>{
      const el = document.querySelector('.personal input.error');
      if (el) el.scrollIntoView({behavior:'smooth', block:'center'});
    });
  }
  function handleCarSave(){
    setSubmittedCar(true);
    if (validCar()) setConfirmCar(true);
    else requestAnimationFrame(()=>{
      const el = document.querySelector('.car input.error');
      if (el) el.scrollIntoView({behavior:'smooth', block:'center'});
    });
  }

  async function onSubmit(){
    setSubmitting(true); setSubmitRes(null);
    try{
      const payload = { plate: normalizePlate(plate), personal: { ...personal, ...derived }, car };
      const res = await submitOnboarding(payload);
      setSubmitRes(res);
    }catch(e){ setSubmitRes({ ok:false, message: e.message }); }
    finally { setSubmitting(false); }
  }

  return (
    <div className="page">
      <Header t={t} lang={lang} setLang={setLang} />

      {/* HERO CANVAS */}
      <main className="main-single">
        <div className="onboarding-wrapper">
          <Stepper active={activeIndex} t={t} />
          <ProgressBar currentStep={step} totalSteps={stepsOrder.length} />
          <div className="card hero">
            <div className="header">
              <div className="title">{t("app_title")}</div>
              <div className="desc">{t("app_sub")}</div>
            </div>

            <AccordionItem id="plate" openId={openId} setOpenId={setOpenId} title={t("plate_title")}>
              <PlateSection
                t={t}
                plate={plate}
                setPlate={setPlate}
                onVerified={handlePlateVerified}   // your existing handler that opens next section
                setPrefill={setPrefill}
                onHelperSelectId={setIdTypeSilent} // ← NEW: only sets the ID type
              />
            </AccordionItem>

            <AccordionItem id="personal" openId={openId} setOpenId={setOpenId} title={t("personal_title")}>
              <PersonalSection
                t={t}
                personal={personal}
                setPersonal={setPersonal}
                submitted={submittedPersonal}
              />
              <div className="actions">
                <button className="btn ghost" onClick={() => setOpenId('plate')}>{t("back")}</button>
                <button className="btn primary" onClick={handlePersonalSave}>{t("save_continue")}</button>
              </div>
            </AccordionItem>

          <AccordionItem id="car" openId={openId} setOpenId={setOpenId} title={t("car_title")}>
            <CarSection
              t={t}
              car={car}
              setCar={setCar}
              onValid={handleCarSave}
            />
            <div className="actions">
              <button className="btn ghost" onClick={() => setOpenId('personal')}>{t("back")}</button>
            </div>
          </AccordionItem>

            <AccordionItem id="funding" openId={openId} setOpenId={setOpenId} title={t("funding_title")}>
              <FundingSection t={t} plate={plate} personal={personal} derived={derived} car={car} onSubmit={onSubmit} submitting={submitting} submitRes={submitRes} />
            </AccordionItem>
          </div>
        </div>

        {/* Smooth follow-on sections */}
        <Benefits t={t} />
        <Footer t={t} />
      </main>

      <ChatbotWidget />

      {/* confirmation modals */}
      <Modal
        open={confirmPersonal}
        title="Confirm Personal Information"
        onClose={()=>setConfirmPersonal(false)}
        secondary={<button className="btn ghost" onClick={()=>setConfirmPersonal(false)}>Edit</button>}
        primary={<button className="btn primary" onClick={()=>{setConfirmPersonal(false); setOpenId('car');}}>Confirm & Continue</button>}
      >
        <div className="confirm-grid">
          <div className="kv"><label>Name</label><span>{personal.fullName}</span></div>
          <div className="kv"><label>NRIC/ID</label><span>{personal.idValue || personal.nric}</span></div>
          <div className="kv"><label>Email</label><span>{personal.email}</span></div>
          <div className="kv"><label>Mobile</label><span>{personal.phone}</span></div>
          <div className="kv col-2"><label>Address</label><span>{personal.addressLine1}, {personal.postcode} {personal.city}, {personal.state}</span></div>
          <div className="kv"><label>E‑Hailing</label><span>{personal.eHailing? 'Yes':'No'}</span></div>
        </div>
      </Modal>

      <Modal
        open={confirmCar}
        title="Confirm Car Information"
        onClose={()=>setConfirmCar(false)}
        secondary={<button className="btn ghost" onClick={()=>setConfirmCar(false)}>Edit</button>}
        primary={<button className="btn primary" onClick={()=>{setConfirmCar(false); setOpenId('funding');}}>Confirm & Continue</button>}
      >
        <div className="confirm-grid">
          <div className="kv"><label>Brand</label><span>{car.brand}</span></div>
          <div className="kv"><label>Model</label><span>{car.model}</span></div>
          <div className="kv"><label>Year</label><span>{car.year}</span></div>
        </div>
      </Modal>
    </div>
  );
}
