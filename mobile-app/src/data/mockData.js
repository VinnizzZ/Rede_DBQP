import { CheckCircle2, Zap } from 'lucide-react';

export const mockUsers = [
  { 
    id: 1, 
    name: 'Voete Bamos', 
    distance: 2, 
    tags: [
      { text: 'Programação', match: true },
      { text: 'Design', match: false },
      { text: 'Música', match: false }
    ],
    avatar: 'https://i.pravatar.cc/150?u=1' 
  },
  { 
    id: 2, 
    name: 'Marine Ky', 
    distance: 2, 
    verified: true,
    tags: [
      { text: 'Programação', match: true },
      { text: 'Design', match: false },
      { text: 'Música', match: false }
    ],
    avatar: 'https://i.pravatar.cc/150?u=2' 
  },
  { 
    id: 3, 
    name: 'Michael Sães', 
    distance: 2, 
    verified: true,
    tags: [
      { text: 'Programação', match: false, highlight: true },
      { text: 'UI Design', match: false, highlight: true }
    ],
    avatar: 'https://i.pravatar.cc/150?u=3' 
  },
  { 
    id: 4, 
    name: 'Gabriel Souza', 
    distance: 2, 
    verified: true,
    skills: 'Python, Data Science',
    tags: [
      { text: 'Interesse', match: true },
    ],
    avatar: 'https://i.pravatar.cc/150?u=4' 
  },
  { 
    id: 5, 
    name: 'Mariana Lima', 
    distance: 2, 
    verified: true,
    skills: 'Python, Data Science',
    tags: [
      { text: 'Interesse', match: true },
    ],
    avatar: 'https://i.pravatar.cc/150?u=5' 
  },
];

export const mockConnections = [
  { id: 10, name: 'Cara Pereira', avatar: 'https://i.pravatar.cc/150?u=10' },
  { id: 11, name: 'João Silva', verified: true, avatar: 'https://i.pravatar.cc/150?u=11' },
  { id: 12, name: 'Diana Costa', verified: true, avatar: 'https://i.pravatar.cc/150?u=12' },
];

export const mockCommunities = [
  { id: 1, name: 'Dev Front-End', members: '2.1k', verified: true, color: '#0F766E' },
  { id: 2, name: 'Startups Brasil', members: '11.9k', verified: true, color: '#FCD34D' },
  { id: 3, name: 'Plataformadoras', members: '9.3k', verified: false, color: '#818CF8' },
];
