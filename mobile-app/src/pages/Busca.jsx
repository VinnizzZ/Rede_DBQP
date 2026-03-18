import React, { useState } from 'react';
import Input from '../components/Input';
import UserCard from '../components/UserCard';
import { Search } from 'lucide-react';
import { mockUsers } from '../data/mockData';

export default function Busca() {
  const [search, setSearch] = useState('');

  return (
    <div>
      <div style={{ marginBottom: '20px', paddingTop: '8px' }}>
        <h1 className="title" style={{ marginBottom: '16px' }}>Quem pode me ajudar?</h1>
        <Input 
          placeholder="Ex: Python, Marketing..." 
          icon={<Search size={20} />} 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {mockUsers.slice(3, 5).map(user => (
          <UserCard 
            key={user.id} 
            user={user} 
            variant="search"
          />
        ))}
      </div>
    </div>
  );
}
