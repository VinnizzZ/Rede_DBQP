import React from 'react';
import './Avatar.css';

export default function Avatar({ src, name, size = 'md', className = '' }) {
  const initials = name ? name.substring(0, 2).toUpperCase() : '?';

  return (
    <div className={`avatar avatar-${size} ${className}`}>
      {src ? (
        <img src={src} alt={name || 'Avatar'} />
      ) : (
        <span>{initials}</span>
      )}
    </div>
  );
}
