import React from "react";
import BJAKLogo from "../assets/Bjak_logo.png"; // adjust path if needed
import MSCLogo from "../assets/msc_logo.png";

const links = {
  quick: [
    { label: "About Us", href: "#" },
    { label: "How BJAK Works", href: "#" },
    { label: "View Policy", href: "#" },
    { label: "Payment Options", href: "#" },
  ],
  support: [
    { label: "FAQs", href: "#" },
    { label: "Contact Us", href: "#" },
    { label: "Roadtax", href: "#" },
    { label: "Careers", href: "#" },
  ],
};

function SocialIcon({ type, href }) {
  const icons = {
    facebook: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M13.5 22v-8h2.7l.4-3H13.5V8.2c0-.9.3-1.5 1.6-1.5h1.6V4.1c-.3 0-1.3-.1-2.5-.1-2.4 0-4 .9-4 3.6V11H7v3h3.2v8h3.3z" />
      </svg>
    ),
    instagram: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M16.8 2H7.2A5.2 5.2 0 0 0 2 7.2v9.6A5.2 5.2 0 0 0 7.2 22h9.6A5.2 5.2 0 0 0 22 16.8V7.2A5.2 5.2 0 0 0 16.8 2ZM20 16.8A3.2 3.2 0 0 1 16.8 20H7.2A3.2 3.2 0 0 1 4 16.8V7.2A3.2 3.2 0 0 1 7.2 4h9.6A3.2 3.2 0 0 1 20 7.2Zm-8-9.1a5.3 5.3 0 1 0 0 10.6 5.3 5.3 0 0 0 0-10.6Zm0 8.5a3.2 3.2 0 1 1 0-6.5 3.2 3.2 0 0 1 0 6.5Zm5.9-9.8a1.2 1.2 0 1 0 0 2.3 1.2 1.2 0 0 0 0-2.3Z" />
      </svg>
    ),
    tiktok: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M21 8.5a7.1 7.1 0 0 1-4.4-1.5v7.2a6.2 6.2 0 1 1-6.2-6.2c.3 0 .6 0 .9.1v2.8a3.3 3.3 0 1 0 2.3 3.1V2h2.8a4.3 4.3 0 0 0 2.8 3.9A4.2 4.2 0 0 0 21 6.2z" />
      </svg>
    ),
    youtube: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M23 12s0-3.6-.5-5.3a3.2 3.2 0 0 0-2.2-2.2C18.6 4 12 4 12 4s-6.6 0-8.3.5a3.2 3.2 0 0 0-2.2 2.2C1 8.4 1 12 1 12s0 3.6.5 5.3a3.2 3.2 0 0 0 2.2 2.2C5.4 20 12 20 12 20s6.6 0 8.3-.5a3.2 3.2 0 0 0 2.2-2.2C23 15.6 23 12 23 12ZM10 15.5V8.5l6 3.5-6 3.5Z" />
      </svg>
    ),
    linkedin: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4.5 3C3.1 3 2 4.1 2 5.5S3.1 8 4.5 8 7 6.9 7 5.5 5.9 3 4.5 3ZM3 9h3v12H3V9Zm6 0h2.9v1.6h.1c.4-.8 1.5-1.7 3.1-1.7 3.3 0 3.9 2.2 3.9 5v7h-3V15c0-1.2 0-2.7-1.6-2.7s-1.8 1.2-1.8 2.6v6.1H9V9Z" />
      </svg>
    )
  };
  return (
    <a className="social" href={href} target="_blank" rel="noreferrer" aria-label={type}>
      {icons[type]}
    </a>
  );
}

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <>
      {/* CTA STRIP */}
      <section className="cta-strip">
        <div className="cta-item">
          <h4>Customer Support</h4>
          <p>Get the help you need</p>
          <a className="btn ghost" href="#">Get Support</a>
        </div>
        <div className="cta-item">
          <h4>Roadside Assistance</h4>
          <p>Available 24 hours daily</p>
          <a className="btn ghost" href="#">Get Assistance</a>
        </div>
        <div className="cta-item">
          <h4>FAQ</h4>
          <p>Browse common questions</p>
          <a className="btn ghost" href="#">Search the FAQ</a>
        </div>
      </section>

      {/* MAIN FOOTER */}
      <footer className="site-footer">
        <div className="footer-grid">
          <div className="col about">
            <img src={BJAKLogo} alt="BJAK" className="brand" />
            <p className="about-text">
              Bjak Sdn Bhd (“BJAK”) is Malaysia’s leading online vehicle insurance platform.
              Compare, customize, and purchase in minutes.
            </p>

            <div className="badges">
              <img src={MSCLogo} alt="MSC" />
              {/* Add other trust badges here if needed */}
            </div>

            <div className="social-row">
              <SocialIcon type="facebook" href="#" />
              <SocialIcon type="instagram" href="#" />
              <SocialIcon type="tiktok" href="#" />
              <SocialIcon type="youtube" href="#" />
              <SocialIcon type="linkedin" href="#" />
            </div>
          </div>

          <nav className="col links">
            <h5>Quick Links</h5>
            <ul>
              {links.quick.map((l) => (
                <li key={l.label}><a href={l.href}>{l.label}</a></li>
              ))}
            </ul>
          </nav>

          <nav className="col links">
            <h5>Support</h5>
            <ul>
              {links.support.map((l) => (
                <li key={l.label}><a href={l.href}>{l.label}</a></li>
              ))}
            </ul>
          </nav>

          <div className="col contact">
            <h5>We’re here 24/7</h5>
            <div className="contact-buttons">
              <a className="contact-btn" href="#"><span>🟢</span> WhatsApp</a>
              <a className="contact-btn" href="#"><span>📩</span> Messenger</a>
            </div>
            <div className="mini-legal">
              Bjak Sdn Bhd (1339813-K) <br/> #1 Vehicle Insurance
            </div>
          </div>
        </div>

        {/* LEGAL BAR */}
        <div className="legal-bar">
          <div className="pidm">
            <span className="badge">PIDM</span>
            <a href="#" className="pidm-link">Learn about PIDM’s TIPS</a>
          </div>
          <div className="rights">
            © {year} BJAK SDN BHD — All rights reserved
          </div>
          <div className="policy-links">
            <a href="#">Terms</a>
            <a href="#">Privacy</a>
            <a href="#">Refunds</a>
          </div>
        </div>
      </footer>
    </>
  );
}
