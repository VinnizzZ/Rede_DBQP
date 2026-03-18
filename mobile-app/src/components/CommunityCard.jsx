import React from 'react';
import Button from './Button';
import { Check, CheckCircle2 } from 'lucide-react';
import './CommunityCard.css';

export default function CommunityCard({ community, onJoin }) {
  // Use first letter and color as generic icon replace
  const iconLetter = community.name.substring(0, 2).toUpperCase();

  return (
    <div className="community-card">
      <div className="cc-icon-wrapper" style={{ backgroundColor: community.color || 'var(--color-primary)' }}>
        {community.id === 1 ? 'XX' : iconLetter}
      </div>
      <div className="cc-info">
        <div className="cc-name-row">
          <div className="cc-name">{community.name}</div>
        </div>
        <div className="cc-members">
           {community.verified && <CheckCircle2 size={14} color="var(--color-primary)" fill="white" />}
           {community.members} membros
        </div>
      </div>
      <div className="cc-action">
        <Button variant="primary" size="sm" onClick={() => onJoin && onJoin(community)}>
          Entrar
        </Button>
      </div>
    </div>
  );
}
