import React from 'react';

export function AccordionItem({ id, openId, setOpenId, title, children }) {
  const open = openId === id;
  return (
    <div className="accordion-item">
      <div className="acc-header" onClick={() => setOpenId(open ? null : id)}>
        <span>{title}</span>
        <span>{open ? '–' : '+'}</span>
      </div>
      {open && <div className="acc-content">{children}</div>}
    </div>
  );
}
