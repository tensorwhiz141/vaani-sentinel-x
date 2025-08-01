import React from 'react';
import { Shield } from 'lucide-react';

const SecurityAgent = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="p-3 bg-yellow-100 rounded-lg mr-3">
            <Shield className="h-8 w-8 text-yellow-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Security Agent</h1>
        </div>
        <p className="text-gray-600">Content security validation and filtering</p>
      </div>
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <Shield className="h-16 w-16 mx-auto mb-4 text-gray-400" />
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">Coming Soon</h2>
        <div className="mt-6">
          <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
            API Endpoint: /api/agents/validate-content
          </span>
        </div>
      </div>
    </div>
  );
};

export default SecurityAgent;
