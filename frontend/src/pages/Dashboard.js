import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Languages, 
  FileText, 
  User, 
  Mic, 
  BarChart3, 
  Calendar, 
  Target, 
  Shield, 
  Heart,
  Activity,
  Zap,
  Globe
} from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState(null);
  const [agentsList, setAgentsList] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSystemInfo = async () => {
      try {
        const [statusResponse, agentsResponse] = await Promise.all([
          axios.get('/health'),
          axios.get('/api/agents/list')
        ]);
        
        setSystemStatus(statusResponse.data);
        setAgentsList(agentsResponse.data);
      } catch (error) {
        console.error('Failed to fetch system info:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSystemInfo();
  }, []);

  const agentCards = [
    {
      name: 'Translation Agent',
      path: '/translation',
      icon: Languages,
      description: 'Real-time multilingual translation with confidence scores',
      color: 'bg-blue-500',
      features: ['21 Languages', 'Tone Adjustment', 'Batch Processing']
    },
    {
      name: 'Content Generation',
      path: '/content-generation',
      icon: FileText,
      description: 'AI-powered content generation for multiple platforms',
      color: 'bg-green-500',
      features: ['4 Platforms', 'Multiple Formats', 'SEO Optimized']
    },
    {
      name: 'Personalization',
      path: '/personalization',
      icon: User,
      description: 'User-specific content personalization and optimization',
      color: 'bg-purple-500',
      features: ['User Preferences', 'Context Aware', 'Real-time Adaptation']
    },
    {
      name: 'Text-to-Speech',
      path: '/tts',
      icon: Mic,
      description: 'Text-to-speech simulation with voice quality metrics',
      color: 'bg-orange-500',
      features: ['Voice Quality', 'Duration Estimation', 'Multi-language']
    },
    {
      name: 'Analytics',
      path: '/analytics',
      icon: BarChart3,
      description: 'Content performance analysis and engagement prediction',
      color: 'bg-red-500',
      features: ['Performance Metrics', 'Engagement Prediction', 'Trend Analysis']
    },
    {
      name: 'Scheduler',
      path: '/scheduler',
      icon: Calendar,
      description: 'Intelligent content scheduling and timing optimization',
      color: 'bg-indigo-500',
      features: ['Optimal Timing', 'Audience Analysis', 'Platform Specific']
    },
    {
      name: 'Strategy',
      path: '/strategy',
      icon: Target,
      description: 'AI-driven content strategy recommendations',
      color: 'bg-pink-500',
      features: ['Performance Analysis', 'Trend Prediction', 'Optimization Tips']
    },
    {
      name: 'Security',
      path: '/security',
      icon: Shield,
      description: 'Content security validation and filtering',
      color: 'bg-yellow-500',
      features: ['Content Filtering', 'Safety Scoring', 'Compliance Check']
    },
    {
      name: 'Sentiment Analysis',
      path: '/sentiment',
      icon: Heart,
      description: 'Sentiment analysis and tone adjustment',
      color: 'bg-teal-500',
      features: ['Emotion Detection', 'Tone Modification', 'Sentiment Scoring']
    }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Vaani Sentinel-X Dynamic Agent API
        </h1>
        <p className="text-xl text-gray-600 mb-6">
          Real-time multilingual AI content generation system
        </p>
        
        {/* System Status */}
        {systemStatus && (
          <div className="inline-flex items-center space-x-2 bg-green-100 text-green-800 px-4 py-2 rounded-full">
            <Activity size={16} />
            <span className="font-medium">System Status: {systemStatus.status || 'Healthy'}</span>
          </div>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Zap className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Agents</p>
              <p className="text-2xl font-bold text-gray-900">
                {agentsList?.total_agents || 10}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Globe className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Languages Supported</p>
              <p className="text-2xl font-bold text-gray-900">21</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Target className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Platforms</p>
              <p className="text-2xl font-bold text-gray-900">4</p>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agentCards.map((agent) => {
          const Icon = agent.icon;
          return (
            <Link
              key={agent.path}
              to={agent.path}
              className="block bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200"
            >
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <div className={`p-3 rounded-lg ${agent.color}`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="ml-3 text-lg font-semibold text-gray-900">
                    {agent.name}
                  </h3>
                </div>
                
                <p className="text-gray-600 mb-4 text-sm">
                  {agent.description}
                </p>
                
                <div className="space-y-1">
                  {agent.features.map((feature, index) => (
                    <div key={index} className="flex items-center text-sm text-gray-500">
                      <div className="w-1.5 h-1.5 bg-gray-400 rounded-full mr-2"></div>
                      {feature}
                    </div>
                  ))}
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* API Information */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">API Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Base URL</h3>
            <code className="bg-gray-100 px-3 py-2 rounded text-sm">
              http://localhost:8000
            </code>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">API Version</h3>
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
              v2.0.0
            </span>
          </div>
        </div>
        
        <div className="mt-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Documentation</h3>
          <div className="flex space-x-4">
            <a 
              href="/docs" 
              target="_blank"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              Interactive API Docs
            </a>
            <a 
              href="/redoc" 
              target="_blank"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              ReDoc Documentation
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
