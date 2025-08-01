import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Languages, 
  FileText, 
  User, 
  Mic, 
  BarChart3, 
  Calendar, 
  Target, 
  Shield, 
  Heart 
} from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', name: 'Dashboard', icon: Home },
    { path: '/translation', name: 'Translation', icon: Languages },
    { path: '/content-generation', name: 'Content Gen', icon: FileText },
    { path: '/personalization', name: 'Personalize', icon: User },
    { path: '/tts', name: 'TTS', icon: Mic },
    { path: '/analytics', name: 'Analytics', icon: BarChart3 },
    { path: '/scheduler', name: 'Scheduler', icon: Calendar },
    { path: '/strategy', name: 'Strategy', icon: Target },
    { path: '/security', name: 'Security', icon: Shield },
    { path: '/sentiment', name: 'Sentiment', icon: Heart },
  ];

  return (
    <nav className="bg-white shadow-lg border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">V</span>
            </div>
            <span className="text-xl font-bold text-gray-800">Vaani Sentinel-X</span>
            <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">v2.0</span>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon size={16} />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button className="text-gray-600 hover:text-gray-900 focus:outline-none">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
