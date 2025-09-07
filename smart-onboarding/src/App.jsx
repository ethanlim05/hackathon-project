import React, { useMemo, useState } from 'react';
import './styles.css';
import Stepper from './components/Stepper';
import { AccordionItem } from './components/Accordion';
import PlateSection from './components/PlateSection';
import PersonalSection from './components/PersonalSection';
import CarSection from './components/CarSection';
import FundingSection from './components/FundingSection';
<<<<<<< Updated upstream
=======
import Modal from './components/Modal';
>>>>>>> Stashed changes
import Benefits from './components/Benefits';
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
<<<<<<< Updated upstream
=======
  const [confirmPersonalOpen, setConfirmPersonalOpen] = useState(false);
  const [confirmCarOpen, setConfirmCarOpen] = useState(false);
  const [personalSubmitAttempt, setPersonalSubmitAttempt] = useState(false);
  const [carSubmitAttempt, setCarSubmitAttempt] = useState(false);
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
=======
  // -------------------- Validation helpers --------------------
  function isValidEmail(v){ return /.+@.+\..+/.test(String(v||"")); }
  function isValidPostcode(v){ return /^\d{5}$/.test(String(v||"")); }
  function isValidMobile(v){ return /^\d{9,12}$/.test(String(v||"").replace(/\D/g, "")); }
  function isValidNRIC(v){
    const d = String(v||"").replace(/\D/g, "");
    if (d.length !== 12) return false;
    const yy = d.slice(0,2), mm = d.slice(2,4), dd = d.slice(4,6);
    const m = Number(mm), day = Number(dd);
    if (m < 1 || m > 12) return false;
    const maxDay = new Date(Number(`20${yy}`), m, 0).getDate();
    return day >= 1 && day <= maxDay;
  }

  function validatePersonal(){
    const idOk = personal.idType === 'NRIC' ? isValidNRIC(personal.idValue) : (personal.idValue && personal.idValue.length >= 3);
    return (
      (personal.fullName||'').trim().length > 1 &&
      idOk &&
      isValidEmail(personal.email) &&
      isValidMobile(personal.phone) &&
      (personal.addressLine1||'').trim().length > 3 &&
      isValidPostcode(personal.postcode) &&
      (personal.city||'').trim().length > 1 &&
      (personal.state||'').trim().length > 1
    );
  }

  function validateCar(){
    const y = Number(car.year);
    const current = new Date().getFullYear()+1;
    const yearOk = /^\d{4}$/.test(String(car.year||'')) && y >= 1990 && y <= current;
    return (
      (car.brand||'').trim().length > 1 &&
      (car.model||'').trim().length > 1 &&
      yearOk
    );
  }

  function onPersonalSave(){
    setPersonalSubmitAttempt(true);
    if (validatePersonal()) {
      setConfirmPersonalOpen(true);
    } else {
      // keep user on section and rely on red hints already wired in PersonalSection via submitted flag
      requestAnimationFrame(()=>{
        const firstError = document.querySelector('.personal input.error');
        if (firstError) firstError.scrollIntoView({ behavior:'smooth', block:'center' });
      });
    }
  }

  function onCarSave(){
    setCarSubmitAttempt(true);
    if (validateCar()) {
      setConfirmCarOpen(true);
    } else {
      requestAnimationFrame(()=>{
        const carEl = document.querySelector('.car input.error');
        if (carEl) carEl.scrollIntoView({ behavior:'smooth', block:'center' });
      });
    }
  }

>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
              <PersonalSection
                t={t}
                personal={personal}
                setPersonal={setPersonal}
              />
              <div className="actions">
                <button className="btn ghost" onClick={() => setOpenId('plate')}>{t("back")}</button>
                <button className="btn primary" onClick={() => setOpenId('car')}>{t("save_continue")}</button>
=======
              <PersonalSection t={t} personal={personal} setPersonal={setPersonal} submitted={personalSubmitAttempt} />
              <div className="right-actions" style={{ marginTop: 18 }}>
                <button className="btn ghost" onClick={()=>setOpenId('plate')}>{t("back")}</button>
                <button className="btn primary" onClick={onPersonalSave}>{t("save_continue")}</button>
>>>>>>> Stashed changes
              </div>
            </AccordionItem>

          <AccordionItem id="car" openId={openId} setOpenId={setOpenId} title={t("car_title")}>
<<<<<<< Updated upstream
            <CarSection
              t={t}
              car={car}
              setCar={setCar}
              onValid={onCarValid}
            />
            <div className="actions">
              <button className="btn ghost" onClick={() => setOpenId('personal')}>{t("back")}</button>
=======
            <CarSection t={t} car={car} setCar={setCar} />
            <div className="right-actions" style={{ marginTop: 18 }}>
              <button className="btn ghost" onClick={()=>setOpenId('personal')}>{t("back")}</button>
              <button className="btn primary" onClick={onCarSave}>{t("save_continue")}</button>
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======

      {/* Confirmation Modals */}
      <Modal
        open={confirmPersonalOpen}
        title="Confirm Personal Information"
        onClose={()=>setConfirmPersonalOpen(false)}
        secondary={<button className="btn ghost" onClick={()=>setConfirmPersonalOpen(false)}>Edit</button>}
        primary={<button className="btn primary" onClick={()=>{ setConfirmPersonalOpen(false); setOpenId('car'); }}>Confirm & Continue</button>}
      >
        <div className="confirm-grid">
          <div className="kv"><label>Name</label><span>{personal.fullName}</span></div>
          <div className="kv"><label>NRIC/ID</label><span>{personal.idValue || personal.nric}</span></div>
          <div className="kv"><label>Email</label><span>{personal.email}</span></div>
          <div className="kv"><label>Mobile</label><span>{personal.phone}</span></div>
          <div className="kv col-2"><label>Address</label><span>{personal.addressLine1}, {personal.postcode} {personal.city}, {personal.state}</span></div>
          <div className="kv"><label>E‑Hailing</label><span>{personal.eHailing ? 'Yes' : 'No'}</span></div>
        </div>
      </Modal>

      <Modal
        open={confirmCarOpen}
        title="Confirm Car Information"
        onClose={()=>setConfirmCarOpen(false)}
        secondary={<button className="btn ghost" onClick={()=>setConfirmCarOpen(false)}>Edit</button>}
        primary={<button className="btn primary" onClick={()=>{ setConfirmCarOpen(false); setOpenId('funding'); }}>Confirm & Continue</button>}
      >
        <div className="confirm-grid">
          <div className="kv"><label>Brand</label><span>{car.brand}</span></div>
          <div className="kv"><label>Model</label><span>{car.model}</span></div>
          <div className="kv"><label>Year</label><span>{car.year}</span></div>
        </div>
      </Modal>
>>>>>>> Stashed changes
    </div>
  );
}
