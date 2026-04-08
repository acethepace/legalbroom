"use client";

import React, { useState } from "react";
import { Send, Loader2 } from "lucide-react";

interface AnalysisFormProps {
  onSubmit: (caseDetails: string) => void;
  isLoading: boolean;
}

const AnalysisForm: React.FC<AnalysisFormProps> = ({ onSubmit, isLoading }) => {
  const [details, setDetails] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (details.trim() && !isLoading) {
      onSubmit(details);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-800">Case Analysis</h2>
        <p className="text-sm text-gray-500 mt-1">
          Enter the details of your case below for automated legal analysis and precedent matching.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col flex-1">
        <textarea
          value={details}
          onChange={(e) => setDetails(e.target.value)}
          disabled={isLoading}
          placeholder="Describe the case details, parties involved, key events, and legal questions..."
          className="flex-1 w-full bg-gray-50 border border-gray-300 rounded-xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition disabled:bg-gray-100 disabled:cursor-not-allowed resize-none shadow-inner mb-4"
        />
        <button
          type="submit"
          disabled={isLoading || !details.trim()}
          className="w-full py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center font-medium shadow-sm"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin mr-2" />
              Analyzing Case...
            </>
          ) : (
            <>
              <Send className="w-5 h-5 mr-2" />
              Submit for Analysis
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default AnalysisForm;
