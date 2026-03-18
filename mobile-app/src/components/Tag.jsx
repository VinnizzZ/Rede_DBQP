import React from 'react';
import './Tag.css';

export default function Tag({ children, variant = 'default', className = '' }) {
  return (
    <span className={`tag ${variant !== 'default' ? `tag-${variant}` : ''} ${className}`}>
      {children}
    </span>
  );
}
