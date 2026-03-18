import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

export default function Layout() {
  return (
    <div className="page-container" style={{ position: 'relative', minHeight: '100vh', paddingBottom: '70px' }}>
      <Outlet />
      <Navbar />
    </div>
  );
}
