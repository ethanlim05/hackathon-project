import React, { useEffect, useState } from "react";
import Logo from "../assets/Bjak_logo.svg";

const LANGS = [
  { code: "en", label: "EN" },
  { code: "bm", label: "BM" },
  { code: "zh", label: "中文" },
];

export default function Header({ t, lang, setLang }) {
  const [isSticky, setIsSticky] = useState(false);
  const [openOffer, setOpenOffer] = useState(false);
  const [openMobile, setOpenMobile] = useState(false);

  useEffect(() => {
    const onScroll = () => setIsSticky(window.scrollY > 6);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={`site-header ${isSticky ? "is-sticky" : ""}`}>
      <div className="header-inner">
        {/* Brand */}
        <a className="brand" href="#">
          <img src={Logo} alt="BJAK" />
          <div className="brand-text">
            <strong>BJAK</strong>
            <span className="tagline">#{t("hdr_rank")} • {t("hdr_open")}</span>
          </div>
        </a>

        {/* Desktop Nav */}
        <nav className="nav-desktop">
          <a href="#about">{t("hdr_about")}</a>

          <div
            className={`dropdown ${openOffer ? "open" : ""}`}
            onMouseEnter={() => setOpenOffer(true)}
            onMouseLeave={() => setOpenOffer(false)}
          >
            <button className="nav-btn" onClick={() => setOpenOffer(v => !v)}>
              {t("hdr_offers")}
              <svg viewBox="0 0 24 24" width="16" height="16">
                <path d="M7 10l5 5 5-5z" fill="currentColor" />
              </svg>
            </button>
            <div className="dropdown-menu">
              <a href="#motor">{t("offer_motor")}</a>
              <a href="#roadtax">{t("offer_roadtax")}</a>
              <a href="#travel">{t("offer_travel")}</a>
            </div>
          </div>

          <div className="auth">
            <a className="btn ghost" href="#login">{t("hdr_login")}</a>
            <a className="btn primary" href="#signup">{t("hdr_signup")}</a>
          </div>

          <div className="lang-switch" role="group" aria-label="Language">
            {LANGS.map(({ code, label }) => (
              <button
                key={code}
                className={`chip ${lang === code ? "active" : ""}`}
                onClick={() => setLang(code)}
              >
                {label}
              </button>
            ))}
          </div>
        </nav>

        {/* Mobile burger */}
        <button
          className="burger"
          aria-label="Toggle Menu"
          onClick={() => setOpenMobile(v => !v)}
        >
          <span />
          <span />
          <span />
        </button>
      </div>

      {/* Mobile sheet */}
      <div className={`mobile-sheet ${openMobile ? "open" : ""}`}>
        <a href="#about" onClick={() => setOpenMobile(false)}>{t("hdr_about")}</a>

        <details>
          <summary>{t("hdr_offers")}</summary>
          <a href="#motor" onClick={() => setOpenMobile(false)}>{t("offer_motor")}</a>
          <a href="#roadtax" onClick={() => setOpenMobile(false)}>{t("offer_roadtax")}</a>
          <a href="#travel" onClick={() => setOpenMobile(false)}>{t("offer_travel")}</a>
        </details>

        <div className="mobile-auth">
          <a className="btn ghost" href="#login" onClick={() => setOpenMobile(false)}>{t("hdr_login")}</a>
          <a className="btn primary" href="#signup" onClick={() => setOpenMobile(false)}>{t("hdr_signup")}</a>
        </div>

        <div className="mobile-lang">
          {LANGS.map(({ code, label }) => (
            <button
              key={code}
              className={`chip ${lang === code ? "active" : ""}`}
              onClick={() => { setLang(code); setOpenMobile(false); }}
            >
              {label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
