import React from 'react';
import Avatar from './Avatar';
import Tag from './Tag';
import { X, Check, Search, CheckCircle2 } from 'lucide-react';
import './UserCard.css';

export default function UserCard({ user, variant = 'default' }) {
  // variant: default (Home), search (Busca)

  return (
    <div className="user-card">
      <Avatar src={user.avatar} name={user.name} size="md" />
      <div className="uc-info">
        <div className="uc-name-row">
          <div className="uc-name">{user.name}</div>
          {user.verified && (
            <div className="verified-badge" style={{ width: 12, height: 12 }}>
              <Check size={8} strokeWidth={4} />
            </div>
          )}
        </div>

        {variant === 'default' && (
           <div className="uc-distance">{user.distance} graus de distância</div>
        )}

        {variant === 'search' && (
           <div className="uc-skills">Habilidades: {user.skills}</div>
        )}

        {variant === 'search' && (
           <div className="uc-distance-match">
             <CheckCircle2 size={14} />
             {user.distance} graus de distância
           </div>
        )}

        {user.tags && (
          <div className="uc-tags">
            {user.tags.map((tag, idx) => {
              if (tag.match) {
                return (
                  <Tag key={idx} variant="success">
                    <CheckCircle2 size={12} className="tag-icon" style={{ marginRight: 4 }} />
                    {tag.text}
                  </Tag>
                );
              }
              if (tag.highlight) {
                return (
                 <Tag key={idx} variant="primary">
                    <span className="uc-tag-highlight" style={{marginRight: 4}}>•</span>
                    {tag.text}
                 </Tag>
                );
              }
              return (
                <Tag key={idx} variant="primary">{tag.text}</Tag>
              )
            })}
          </div>
        )}
      </div>

      {variant === 'default' && (
        <div className="uc-close">
          <X size={16} />
        </div>
      )}
    </div>
  );
}
