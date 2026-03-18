import React from 'react';
import Card from '../components/Card';
import Avatar from '../components/Avatar';
import Button from '../components/Button';
import { MessageCircle, User } from 'lucide-react';
import { mockUsers } from '../data/mockData';

export default function Connections() {
  const connectedUsers = mockUsers.slice(0, 2);

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 className="title" style={{ marginBottom: '8px' }}>Suas Conexões</h1>
        <p className="caption">Pessoas com quem você já se conectou.</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {connectedUsers.map(user => (
          <Card key={user.id} className="connection-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <Avatar src={user.avatar} name={user.name} />
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '18px', fontWeight: '600' }}>{user.name}</div>
                <div style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>Desde Jan 2024</div>
              </div>
            </div>
            
            <div style={{ display: 'flex', gap: '8px' }}>
              <Button variant="primary" style={{ flex: 1, height: '40px', padding: '0 8px' }}>
                <MessageCircle size={16} style={{ marginRight: '6px' }} />
                Mensagem
              </Button>
              <Button variant="outline" style={{ flex: 1, height: '40px', padding: '0 8px' }}>
                <User size={16} style={{ marginRight: '6px' }} />
                Ver perfil
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
