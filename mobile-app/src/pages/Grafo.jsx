import React from 'react';
import Avatar from '../components/Avatar';
import Button from '../components/Button';
import { ArrowLeft, CheckCircle2, ArrowRight, ArrowDown } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Grafo() {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', paddingBottom: '24px' }}>
      <div className="top-nav">
        <ArrowLeft className="top-nav-back" onClick={() => navigate(-1)} />
        <h1 className="top-nav-title">Distância entre Usuários</h1>
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', marginTop: '32px' }}>
        
        {/* Node: João (Top) */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative' }}>
          <div style={{ position: 'relative' }}>
             <Avatar src="https://i.pravatar.cc/150?u=11" name="João" size="lg" style={{ width: '64px', height: '64px' }} />
             <CheckCircle2 size={18} fill="var(--color-primary)" color="white" style={{ position: 'absolute', bottom: 0, right: 0, backgroundColor: 'white', borderRadius: '50%' }} />
          </div>
          <p style={{ fontWeight: 'bold', marginTop: '8px', fontSize: '14px' }}>João</p>
          
          {/* Vertical Arrow Down */}
          <ArrowDown size={24} color="var(--color-primary)" style={{ margin: '8px 0' }} />
        </div>

        {/* Middle row: João, Maria, Pedro */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', position: 'relative' }}>
          {/* Node 1 */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ position: 'relative' }}>
               <Avatar src="https://i.pravatar.cc/150?u=13" name="João" size="md" />
               <CheckCircle2 size={14} fill="var(--color-primary)" color="white" style={{ position: 'absolute', bottom: 0, right: 0, backgroundColor: 'white', borderRadius: '50%' }} />
            </div>
            <p style={{ fontWeight: 'bold', marginTop: '4px', fontSize: '12px' }}>João</p>
          </div>

          <div style={{ height: '2px', width: '40px', backgroundColor: 'var(--color-primary)' }}></div>

          {/* Node 2 - Hidden behind the vertical arrow in mockup, but connecting logically */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ position: 'relative', backgroundColor: 'white', padding: '4px', borderRadius: '50%' }}>
               <span style={{color: 'var(--color-text-secondary)', fontSize: '12px'}}>Maria</span>
            </div>
            <p style={{ fontWeight: 'bold', marginTop: '4px', fontSize: '12px' }}>Maria</p>
          </div>

          <div style={{ height: '2px', width: '40px', backgroundColor: 'var(--color-primary)' }}></div>

          {/* Node 3 */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ position: 'relative' }}>
               <Avatar src="https://i.pravatar.cc/150?u=14" name="Pedro" size="md" />
               <CheckCircle2 size={14} fill="var(--color-primary)" color="white" style={{ position: 'absolute', bottom: 0, right: 0, backgroundColor: 'white', borderRadius: '50%' }} />
            </div>
            <p style={{ fontWeight: 'bold', marginTop: '4px', fontSize: '12px' }}>Pedro</p>
          </div>
        </div>

        {/* Distance Indicator Box */}
        <div style={{ 
          marginTop: '40px', 
          backgroundColor: 'var(--color-input-bg)', 
          padding: '16px 32px', 
          borderRadius: 'var(--border-radius-pill)',
          fontWeight: 'bold',
          color: 'var(--color-text-primary)'
        }}>
          Distância: 3 graus
        </div>

      </div>

      <div style={{ marginTop: 'auto', paddingTop: '32px' }}>
        <Button variant="primary">
          Entrar
        </Button>
      </div>

    </div>
  );
}
