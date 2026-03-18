import React, { useState } from 'react';
import Input from '../components/Input';
import UserCard from '../components/UserCard';
import { Search } from 'lucide-react';
import { mockUsers } from '../data/mockData';

export default function Help() {
  const [skillSearch, setSkillSearch] = useState('');

  const filteredUsers = mockUsers.filter(user => 
    user.skills.some(skill => skill.toLowerCase().includes(skillSearch.toLowerCase()))
  );

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 className="title" style={{ marginBottom: '8px' }}>Quem pode me ajudar?</h1>
        <p className="caption">Busque pessoas por habilidades específicas e peça ajuda.</p>
      </div>

      <Input 
        placeholder="Buscar habilidades (ex: React, Figma)" 
        icon={<Search size={20} />} 
        value={skillSearch}
        onChange={(e) => setSkillSearch(e.target.value)}
      />

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
        {filteredUsers.length > 0 ? filteredUsers.map(user => (
          <UserCard 
            key={user.id} 
            user={user} 
            actionLabel="Pedir ajuda"
            onConnect={() => alert(`Solicitação de ajuda enviada para ${user.name}`)}
          />
        )) : (
          <p className="caption">Ninguém encontrado com essa habilidade.</p>
        )}
      </div>
    </div>
  );
}
