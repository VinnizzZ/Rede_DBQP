import React, { useState } from 'react';
import Input from '../components/Input';
import CommunityCard from '../components/CommunityCard';
import { Search } from 'lucide-react';
import { mockCommunities } from '../data/mockData';

export default function Communities() {
  const [search, setSearch] = useState('');

  const filtered = mockCommunities.filter(c => 
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 className="title" style={{ marginBottom: '8px' }}>Comunidades</h1>
        <p className="caption">Encontre grupos com os mesmos interesses que você.</p>
      </div>

      <Input 
        placeholder="Buscar comunidades..." 
        icon={<Search size={20} />} 
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
        {filtered.map(comm => (
          <CommunityCard 
            key={comm.id} 
            community={comm}
            onJoin={() => alert(`Entrou na comunidade ${comm.name}`)}
          />
        ))}
      </div>
    </div>
  );
}
