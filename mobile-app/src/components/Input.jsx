import React from 'react';
import './Input.css';

export default function Input({ 
  label, 
  icon, 
  iconRight,
  className = '', 
  ...props 
}) {
  return (
    <div className={`input-wrapper ${className}`}>
      {label && <label className="input-label">{label}</label>}
      <div className="input-with-icon">
        {icon && <span className="input-icon">{icon}</span>}
        <input 
          className={`input-field ${icon ? 'has-icon' : ''} ${iconRight ? 'has-icon-right' : ''}`} 
          {...props} 
        />
        {iconRight && <span className="input-icon-right">{iconRight}</span>}
      </div>
    </div>
  );
}
