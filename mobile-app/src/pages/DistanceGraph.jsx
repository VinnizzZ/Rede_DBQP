import React from 'react';
import Avatar from '../components/Avatar';

export default function DistanceGraph() {
  const nodes = [
    { id: 'me', name: 'Você', avatar: 'https://i.pravatar.cc/150?u=99' },
    { id: '1', name: 'Alice', avatar: 'https://i.pravatar.cc/150?u=1' },
    { id: '2', name: 'Bruno', avatar: 'https://i.pravatar.cc/150?u=2' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', padding: '24px 0' }}>
      <div style={{ marginBottom: '40px', textAlign: 'center' }}>
        <h1 className="title" style={{ marginBottom: '8px' }}>Grafo de Conexões</h1>
        <p className="caption">Veja a distância entre você e outras pessoas.</p>
      </div>

      {/* Very simple linear graph representation */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px', position: 'relative' }}>
        <Avatar src={nodes[0].avatar} name={nodes[0].name} size="lg" />
        <div className="title" style={{ fontSize: '16px' }}>{nodes[0].name}</div>
        
        {/* Connection line */}
        <div style={{ height: '40px', width: '2px', backgroundColor: 'var(--color-primary)' }}></div>
        <div style={{ position: 'absolute', top: '150px', right: 'calc(50% + 16px)', fontSize: '12px', color: 'var(--color-text-secondary)', fontWeight: 'bold' }}>
          1 grau
        </div>

        <Avatar src={nodes[1].avatar} name={nodes[1].name} size="lg" />
        <div className="title" style={{ fontSize: '16px' }}>{nodes[1].name}</div>

        <div style={{ height: '40px', width: '2px', backgroundColor: 'var(--color-border)' }}></div>
        <div style={{ position: 'absolute', top: '310px', right: 'calc(50% + 16px)', fontSize: '12px', color: 'var(--color-text-secondary)' }}>
          2 graus
        </div>

        <Avatar src={nodes[2].avatar} name={nodes[2].name} size="lg" />
        <div className="title" style={{ fontSize: '16px' }}>{nodes[2].name}</div>
      </div>
    </div>
  );
}
