import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Search, Users, User, MessagesSquare } from 'lucide-react';
import './Navbar.css';

export default function Navbar() {
  const navItems = [
    { path: '/home', icon: Home, label: 'Home' },
    { path: '/busca', icon: Search, label: 'Busca' },
    { path: '/conexoes', icon: Users, label: 'Conexões' },
    { path: '/comunidades', icon: MessagesSquare, label: 'Comunidades' },
    { path: '/perfil', icon: User, label: 'Perfil' },
  ];

  return (
    <nav className="navbar">
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <item.icon size={22} className="nav-icon" />
          <span className="nav-label">{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
