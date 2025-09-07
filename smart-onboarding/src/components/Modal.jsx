import React from "react";

export default function Modal({ open, title, children, onClose, primary, secondary }) {
  if (!open) return null;
  return (
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal">
        <div className="modal-head">
          <div className="modal-title">{title}</div>
          <button className="modal-x" onClick={onClose} aria-label="Close">×</button>
        </div>
        <div className="modal-body">{children}</div>
        <div className="modal-foot">
          {secondary}
          {primary}
        </div>
      </div>
    </div>
  );
}
