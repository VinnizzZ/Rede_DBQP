import React from 'react';
import Avatar from '../components/Avatar';
import Button from '../components/Button';
import Tag from '../components/Tag';
import { Edit3 } from 'lucide-react';
import './Profile.css';

export default function Profile() {
  const user = {
    name: 'João Victor',
    bio: 'Desenvolvedor Full Stack apaixonado por criar interfaces incríveis e resolver problemas complexos.',
    avatar: 'https://i.pravatar.cc/150?u=99',
    interests: ['React', 'UX/UI', 'Startups', 'Tecnologia'],
    skills: ['JavaScript', 'Node.js', 'Figma', 'CSS']
  };

  return (
    <div className="profile-page">
      <div className="profile-header">
        <Avatar src={user.avatar} name={user.name} size="lg" className="profile-avatar" />
        <h1 className="title">{user.name}</h1>
        <p className="body-text profile-bio">{user.bio}</p>
        <Button variant="outline" className="edit-btn">
          <Edit3 size={16} style={{ marginRight: '8px' }} />
          Editar perfil
        </Button>
      </div>

      <section className="profile-section">
        <h2 className="subtitle">Interesses</h2>
        <div className="profile-tags">
          {user.interests.map((tag, idx) => (
            <Tag key={idx} variant="primary">{tag}</Tag>
          ))}
        </div>
      </section>

      <section className="profile-section">
        <h2 className="subtitle">Habilidades</h2>
        <div className="profile-tags">
          {user.skills.map((skill, idx) => (
            <Tag key={idx} variant="secondary">{skill}</Tag>
          ))}
        </div>
      </section>
    </div>
  );
}
