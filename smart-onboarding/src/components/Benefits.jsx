import React from "react";

const items = [
  {
    icon: "⚡",
    title: "Fast Claims Approval",
    desc: "Quick approval for small claims, subject to T&C."
  },
  {
    icon: "🛡️",
    title: "Risk Based Pricing",
    desc: "Potentially lower premiums with safer risk profiles."
  },
  {
    icon: "🔧",
    title: "Repair Warranty",
    desc: "6-month repair warranty from panel workshops."
  },
  {
    icon: "📞",
    title: "24/7 Roadside Assistance",
    desc: "Emergency hotline and assistance, 24 hours daily."
  },
  {
    icon: "⭐",
    title: "More Add-Ons & Benefits",
    desc: "Windscreen, flood, special perils & more."
  },
  {
    icon: "🚗",
    title: "Multi Drive Protector +",
    desc: "Free towing with selected add-ons."
  }
];

export default function Benefits() {
  return (
    <section className="benefits-section">
      <div className="benefits-head">
        <h2>What Does Car Insurance Cover?</h2>
        <p>Real protection, helpful options — and support when you need it.</p>
      </div>

      <div className="benefits-grid">
        {items.map((it, i) => (
          <article key={i} className="benefit-card">
            <div className="benefit-icon">{it.icon}</div>
            <h3>{it.title}</h3>
            <p>{it.desc}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
