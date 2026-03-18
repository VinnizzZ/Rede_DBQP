import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Layout from './components/Layout';

import Home from './pages/Home';
import Busca from './pages/Busca';
import Conexoes from './pages/Conexoes';
import Comunidades from './pages/Comunidades';
import Perfil from './pages/Perfil';
import Grafo from './pages/Grafo';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/home" element={<Home />} />
          <Route path="/busca" element={<Busca />} />
          <Route path="/conexoes" element={<Conexoes />} />
          <Route path="/comunidades" element={<Comunidades />} />
          <Route path="/perfil" element={<Perfil />} />
          {/* Grafo could be a subpage, we'll route it directly for now */}
          <Route path="/grafo" element={<Grafo />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
