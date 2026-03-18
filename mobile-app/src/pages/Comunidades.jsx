import React, { useState } from 'react';
import Input from '../components/Input';
import CommunityCard from '../components/CommunityCard';
import { Search } from 'lucide-react';
import { mockCommunities } from '../data/mockData';

export default function Comunidades() {
  const [search, setSearch] = useState('');

  return (
    <div>
      <div style={{ marginBottom: '20px', paddingTop: '8px' }}>
        <h1 className="title" style={{ marginBottom: '16px' }}>Comunidades</h1>
        <Input 
          placeholder="Buscar comunidades" 
          icon={<Search size={20} />} 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '16px' }}>
        {mockCommunities.map(comm => (
          <CommunityCard 
            key={comm.id} 
            community={comm}
            onJoin={() => {}}
          />
        ))}
      </div>
    </div>
  );
}
