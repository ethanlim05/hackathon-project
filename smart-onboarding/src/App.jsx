import React, { useMemo, useState } from 'react';
import './styles.css';
import Stepper from './components/Stepper';
import { AccordionItem } from './components/Accordion';
import PlateSection from './components/PlateSection';
import PersonalSection from './components/PersonalSection';
import CarSection from './components/CarSection';
import FundingSection from './components/FundingSection';
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
              />
              <div className="actions">
                <button className="btn ghost" onClick={() => setOpenId('plate')}>{t("back")}</button>
                <button className="btn primary" onClick={() => setOpenId('car')}>{t("save_continue")}</button>
              </div>
            </AccordionItem>

          <AccordionItem id="car" openId={openId} setOpenId={setOpenId} title={t("car_title")}>
            <CarSection
              t={t}
              car={car}
              setCar={setCar}
              onValid={onCarValid}
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
    </div>
  );
}
