import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useMutation } from 'react-query';
import axios from 'axios';
import toast from 'react-hot-toast';
import { Languages, Send, Copy, Download, Loader } from 'lucide-react';

const TranslationAgent = () => {
  const [results, setResults] = useState(null);
  const { register, handleSubmit, formState: { errors }, watch } = useForm({
    defaultValues: {
      original_text: '',
      source_language: 'en',
      target_languages: ['hi', 'sa'],
      tone: 'neutral',
      preserve_formatting: true,
      include_confidence: true
    }
  });

  const translateMutation = useMutation(
    (data) => axios.post('/api/agents/translate', data),
    {
      onSuccess: (response) => {
        setResults(response.data);
        toast.success('Translation completed successfully!');
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Translation failed');
      }
    }
  );

  const onSubmit = (data) => {
    translateMutation.mutate(data);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const downloadResults = () => {
    if (!results) return;
    
    const dataStr = JSON.stringify(results, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'translation_results.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi' },
    { code: 'sa', name: 'Sanskrit' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'ja', name: 'Japanese' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ar', name: 'Arabic' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'it', name: 'Italian' },
    { code: 'ru', name: 'Russian' },
    { code: 'ko', name: 'Korean' }
  ];

  const tones = [
    { value: 'formal', label: 'Formal' },
    { value: 'casual', label: 'Casual' },
    { value: 'devotional', label: 'Devotional' },
    { value: 'neutral', label: 'Neutral' }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="p-3 bg-blue-100 rounded-lg mr-3">
            <Languages className="h-8 w-8 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Translation Agent</h1>
        </div>
        <p className="text-gray-600">
          Real-time multilingual translation with confidence scores and tone adjustment
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Translation Input</h2>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* Text Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Text to Translate *
              </label>
              <textarea
                {...register('original_text', { required: 'Text is required' })}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter the text you want to translate..."
              />
              {errors.original_text && (
                <p className="text-red-500 text-sm mt-1">{errors.original_text.message}</p>
              )}
            </div>

            {/* Source Language */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Source Language
              </label>
              <select
                {...register('source_language')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {languages.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name} ({lang.code})
                  </option>
                ))}
              </select>
            </div>

            {/* Target Languages */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Languages
              </label>
              <div className="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto border border-gray-300 rounded-md p-2">
                {languages.map(lang => (
                  <label key={lang.code} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      value={lang.code}
                      {...register('target_languages')}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm">{lang.name}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Tone */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tone
              </label>
              <select
                {...register('tone')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {tones.map(tone => (
                  <option key={tone.value} value={tone.value}>
                    {tone.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Options */}
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  {...register('preserve_formatting')}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm">Preserve formatting</span>
              </label>
              
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  {...register('include_confidence')}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm">Include confidence scores</span>
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={translateMutation.isLoading}
              className="w-full flex items-center justify-center space-x-2 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {translateMutation.isLoading ? (
                <Loader className="animate-spin h-4 w-4" />
              ) : (
                <Send className="h-4 w-4" />
              )}
              <span>{translateMutation.isLoading ? 'Translating...' : 'Translate'}</span>
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-800">Translation Results</h2>
            {results && (
              <button
                onClick={downloadResults}
                className="flex items-center space-x-1 text-blue-600 hover:text-blue-800"
              >
                <Download className="h-4 w-4" />
                <span>Download</span>
              </button>
            )}
          </div>

          {!results ? (
            <div className="text-center text-gray-500 py-8">
              <Languages className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>Translation results will appear here</p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Summary */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Total Translations:</span> {results.total_translations}
                  </div>
                  <div>
                    <span className="font-medium">Processing Time:</span> {results.processing_time}s
                  </div>
                </div>
              </div>

              {/* Translations */}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {results.translations?.map((translation, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-gray-800">
                          {translation.language_name}
                        </span>
                        <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                          {translation.target_language}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-500">
                          Confidence: {(translation.confidence_score * 100).toFixed(1)}%
                        </span>
                        <button
                          onClick={() => copyToClipboard(translation.translated_text)}
                          className="text-gray-400 hover:text-gray-600"
                        >
                          <Copy className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                    
                    <p className="text-gray-700 mb-2">{translation.translated_text}</p>
                    
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <span>Tone: {translation.tone_applied}</span>
                      <span>Words: {translation.word_count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TranslationAgent;
