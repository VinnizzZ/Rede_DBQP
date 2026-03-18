import React from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../components/Input';
import Button from '../components/Button';
import { Network } from 'lucide-react';
import './Login.css';

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    navigate('/home');
  };

  return (
    <div className="login-page">
      <div className="login-logo">
        <div className="logo-icon">
          <Network size={64} fill="var(--color-primary)" />
        </div>
        <h1>Bem-vindo de volta 👋</h1>
      </div>

      <form className="login-form" onSubmit={handleLogin}>
        <Input 
          type="email" 
          placeholder="Email" 
          required
        />
        <Input 
          type="password" 
          placeholder="Senha" 
          required
        />
        
        <Button type="submit" variant="primary" style={{ marginTop: '16px' }}>
          Entrar
        </Button>
      </form>

      <div className="login-divider-text">Criar conta</div>

      <Button variant="secondary" className="btn-google" type="button" style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" alt="Google" width="18" height="18" />
        Continuar com Google
      </Button>
    </div>
  );
}
