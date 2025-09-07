import React from "react";

export default function LanguageToggle({ lang, setLang }) {
  return (
    <div className="lang-toggle" role="group" aria-label="Language">
      <button
        className={`chip ${lang === "en" ? "active" : ""}`}
        onClick={() => setLang("en")}
      >
        EN
      </button>
      <button
        className={`chip ${lang === "bm" ? "active" : ""}`}
        onClick={() => setLang("bm")}
      >
        BM
      </button>
      <button
        className={`chip ${lang === "zh" ? "active" : ""}`}
        onClick={() => setLang("zh")}
      >
        ZH
      </button>
    </div>
  );
}
