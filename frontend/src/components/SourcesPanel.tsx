"use client";

import React from "react";
import { FileText, Gavel, Calendar, ExternalLink } from "lucide-react";
import { Citation } from "../hooks/useChat";

interface SourcesPanelProps {
  citations: Citation[];
  onCitationClick: (citation: Citation) => void;
  activeCitationId?: string;
}

const SourcesPanel: React.FC<SourcesPanelProps> = ({
  citations,
  onCitationClick,
  activeCitationId,
}) => {
  if (citations.length === 0) {
    return (
      <div className="h-full flex items-center justify-center p-8 text-gray-400 bg-gray-50 border-l border-gray-200">
        <div className="text-center">
          <FileText className="w-12 h-12 mx-auto mb-2 opacity-20" />
          <p className="text-sm">No citations for this message</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-gray-50 border-l border-gray-200 w-full overflow-y-auto">
      <div className="p-4 border-b border-gray-200 bg-white sticky top-0 z-10">
        <h3 className="font-semibold text-gray-700 flex items-center">
          <FileText className="w-4 h-4 mr-2" />
          Sources
        </h3>
      </div>
      <div className="p-4 space-y-3">
        {citations.map((cite) => (
          <div
            key={cite.id}
            onClick={() => onCitationClick(cite)}
            className={`p-3 rounded-lg border transition cursor-pointer hover:shadow-sm ${
              activeCitationId === cite.id
                ? "bg-blue-50 border-blue-200 ring-1 ring-blue-100"
                : "bg-white border-gray-200 hover:border-blue-200"
            }`}
          >
            <div className="flex flex-col mb-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-100 px-1.5 py-0.5 rounded self-start mb-1">
                Source {cite.id}
              </span>
              <h4 className="text-xs font-bold text-gray-800 line-clamp-2">{cite.title}</h4>
            </div>
            <div className="space-y-1 mb-2">
              <div className="flex items-center text-[10px] text-gray-500 font-medium">
                <Gavel className="w-3 h-3 mr-1" />
                {cite.court}
              </div>
              <div className="flex items-center text-[10px] text-gray-500 font-medium">
                <Calendar className="w-3 h-3 mr-1" />
                {cite.date_filed}
              </div>
            </div>
            <p className="text-xs text-gray-600 line-clamp-4 leading-relaxed italic">
              "{cite.snippet}"
            </p>
            <a 
              href={cite.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="mt-2 flex items-center text-[10px] text-blue-500 hover:underline"
              onClick={(e) => e.stopPropagation()}
            >
              <ExternalLink className="w-3 h-3 mr-1" />
              View on CourtListener
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SourcesPanel;
