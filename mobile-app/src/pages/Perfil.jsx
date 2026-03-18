import React from 'react';
import Avatar from '../components/Avatar';
import Button from '../components/Button';
import Tag from '../components/Tag';
import { ArrowLeft, CheckCircle2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Perfil() {
  const navigate = useNavigate();

  return (
    <div>
      <div className="top-nav">
        <ArrowLeft className="top-nav-back" onClick={() => navigate(-1)} />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', marginTop: '16px' }}>
        <div style={{ position: 'relative', marginBottom: '16px' }}>
          <Avatar src="https://i.pravatar.cc/150?u=99" name="Lucas Almeida" size="lg" style={{ width: '100px', height: '100px' }} />
          <div style={{ position: 'absolute', bottom: '4px', right: '4px', backgroundColor: 'white', borderRadius: '50%', padding: '2px' }}>
             <CheckCircle2 size={24} fill="var(--color-primary)" color="white" />
          </div>
        </div>
        
        <h1 className="title" style={{ fontSize: '24px' }}>Lucas Almeida</h1>
        <p className="body-text" style={{ color: 'var(--color-text-secondary)', marginTop: '8px', maxWidth: '80%' }}>
          Entusiasta de tecnologia e desenvolvimento web
        </p>
      </div>

      <div style={{ marginTop: '32px' }}>
        <h2 className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <span style={{ fontSize: '20px' }}>👏</span> Interesses
        </h2>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <Tag variant="outline-primary" style={{ fontSize: '13px', padding: '6px 16px' }}>Programação</Tag>
          <Tag variant="outline-primary" style={{ fontSize: '13px', padding: '6px 16px' }}>Design</Tag>
          <Tag variant="outline-primary" style={{ fontSize: '13px', padding: '6px 16px' }}>Música</Tag>
        </div>
      </div>

      <div style={{ marginTop: '32px', marginBottom: '40px' }}>
        <h2 className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <span style={{ fontSize: '20px' }}>✨</span> Habilidades
        </h2>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <Tag style={{ fontSize: '13px', padding: '6px 16px' }}>JavaScript</Tag>
          <Tag style={{ fontSize: '13px', padding: '6px 16px' }}>UI Design</Tag>
        </div>
      </div>

      <Button variant="primary">
        Editar Perfil
      </Button>
    </div>
  );
}
