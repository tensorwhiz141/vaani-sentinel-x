import React from 'react';
import { BarChart3 } from 'lucide-react';

const AnalyticsAgent = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="p-3 bg-red-100 rounded-lg mr-3">
            <BarChart3 className="h-8 w-8 text-red-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics Agent</h1>
        </div>
        <p className="text-gray-600">Content performance analysis and engagement prediction</p>
      </div>
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <BarChart3 className="h-16 w-16 mx-auto mb-4 text-gray-400" />
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">Coming Soon</h2>
        <div className="mt-6">
          <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
            API Endpoint: /api/agents/analyze-content
          </span>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsAgent;
