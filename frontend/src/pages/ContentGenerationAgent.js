import React from 'react';
import { FileText } from 'lucide-react';

const ContentGenerationAgent = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="p-3 bg-green-100 rounded-lg mr-3">
            <FileText className="h-8 w-8 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Content Generation Agent</h1>
        </div>
        <p className="text-gray-600">
          AI-powered content generation for multiple platforms and languages
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <FileText className="h-16 w-16 mx-auto mb-4 text-gray-400" />
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">Coming Soon</h2>
        <p className="text-gray-600 mb-4">
          This agent interface is under development. It will provide:
        </p>
        <ul className="text-left max-w-md mx-auto space-y-2 text-gray-600">
          <li>• Platform-specific content generation</li>
          <li>• Multi-language support</li>
          <li>• Tone and style customization</li>
          <li>• SEO optimization</li>
          <li>• Hashtag generation</li>
        </ul>
        <div className="mt-6">
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
            API Endpoint: /api/agents/generate-content
          </span>
        </div>
      </div>
    </div>
  );
};

export default ContentGenerationAgent;
