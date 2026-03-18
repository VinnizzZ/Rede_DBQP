import React from 'react';
import Avatar from '../components/Avatar';
import Button from '../components/Button';
import { Search, CheckCircle2 } from 'lucide-react';
import Input from '../components/Input';
import { mockConnections } from '../data/mockData';

export default function Conexoes() {
  return (
    <div>
      <div style={{ marginBottom: '20px', paddingTop: '8px' }}>
        <h1 className="title" style={{ marginBottom: '16px' }}>Conexões</h1>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {mockConnections.map(user => (
          <div key={user.id} style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between',
            padding: '16px 0',
            borderBottom: '1px solid var(--color-border)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <Avatar src={user.avatar} name={user.name} size="md" />
              <div>
                <div style={{ fontSize: '15px', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  {user.name}
                  {user.verified && <CheckCircle2 size={12} fill="var(--color-primary)" color="white" />}
                </div>
              </div>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <Button variant="secondary" size="sm">
                Mensagem
              </Button>
              <Button variant="outline" size="sm" style={{ borderColor: 'transparent', backgroundColor: 'transparent', color: 'var(--color-text-secondary)' }}>
                Ver perfil
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
