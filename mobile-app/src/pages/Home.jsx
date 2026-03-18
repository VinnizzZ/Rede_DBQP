import React, { useState } from 'react';
import Input from '../components/Input';
import UserCard from '../components/UserCard';
import CommunityCard from '../components/CommunityCard';
import { Search, Mic, UsersRound } from 'lucide-react';
import { mockUsers, mockCommunities } from '../data/mockData';
import './Home.css';

export default function Home() {
  const [search, setSearch] = useState('');

  return (
    <div>
      <div className="home-header">
        <Input 
          placeholder="Buscar pessoas ou interesses" 
          icon={<Search size={20} />} 
          iconRight={<Mic size={20} />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <section>
        <div className="section-header">
          <h2 className="section-title">Sugestões de conexão</h2>
        </div>
        <div className="vertical-list">
          {mockUsers.slice(0, 3).map(user => (
            <UserCard 
              key={user.id} 
              user={user} 
              variant="default"
            />
          ))}
        </div>
      </section>

      <section>
        <div className="section-header">
          <UsersRound size={20} color="var(--color-primary)" />
          <h2 className="section-title">Comunidades</h2>
        </div>
        <div className="vertical-list">
          {mockCommunities.slice(0, 1).map(comm => (
            <CommunityCard 
              key={comm.id} 
              community={comm}
              onJoin={() => {}}
            />
          ))}
        </div>
      </section>
    </div>
  );
}
