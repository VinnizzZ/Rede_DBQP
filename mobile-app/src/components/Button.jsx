import React from 'react';
import './Button.css';

export default function Button({ 
  children, 
  variant = 'primary', 
  size = 'md', // sm, md
  className = '', 
  fullWidth = false, 
  ...props 
}) {
  return (
    <button 
      className={`btn btn-${variant} ${size === 'sm' ? 'btn-sm' : ''} ${fullWidth ? 'w-full' : ''} ${className}`} 
      {...props}
    >
      {children}
    </button>
  );
}
