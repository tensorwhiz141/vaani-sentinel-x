import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import './App.css';

// Components
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import TranslationAgent from './pages/TranslationAgent';
import ContentGenerationAgent from './pages/ContentGenerationAgent';
import PersonalizationAgent from './pages/PersonalizationAgent';
import TTSAgent from './pages/TTSAgent';
import AnalyticsAgent from './pages/AnalyticsAgent';
import SchedulerAgent from './pages/SchedulerAgent';
import StrategyAgent from './pages/StrategyAgent';
import SecurityAgent from './pages/SecurityAgent';
import SentimentAgent from './pages/SentimentAgent';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App min-h-screen bg-gray-50">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/translation" element={<TranslationAgent />} />
              <Route path="/content-generation" element={<ContentGenerationAgent />} />
              <Route path="/personalization" element={<PersonalizationAgent />} />
              <Route path="/tts" element={<TTSAgent />} />
              <Route path="/analytics" element={<AnalyticsAgent />} />
              <Route path="/scheduler" element={<SchedulerAgent />} />
              <Route path="/strategy" element={<StrategyAgent />} />
              <Route path="/security" element={<SecurityAgent />} />
              <Route path="/sentiment" element={<SentimentAgent />} />
            </Routes>
          </main>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
