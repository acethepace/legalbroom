"use client";

import React, { useState, useEffect } from "react";
import AnalysisForm from "@/components/AnalysisForm";
import Chat from "@/components/Chat";
import SourcesPanel from "@/components/SourcesPanel";
import { useChat, Citation } from "@/hooks/useChat";
import { Search, Settings, Info, History } from "lucide-react";
import Link from "next/link";

export default function AnalysisPage() {
  const { messages, isConnected, sendMessage } = useChat();
  const [activeCitation, setActiveCitation] = useState<Citation | undefined>();
  const [currentCitations, setCurrentCitations] = useState<Citation[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    const lastAssistantMessage = [...messages]
      .reverse()
      .find((m) => m.role === "assistant" && m.citations && m.citations.length > 0);
    
    if (lastAssistantMessage && lastAssistantMessage.citations) {
      setCurrentCitations(lastAssistantMessage.citations);
    }

    // Check if assistant is done (no status and has content)
    const lastMsg = messages[messages.length - 1];
    if (lastMsg && lastMsg.role === "assistant" && !lastMsg.status && lastMsg.content) {
      setIsAnalyzing(false);
    }
  }, [messages]);

  const handleCitationClick = (citation: Citation) => {
    setActiveCitation(citation);
    if (citation.url) {
      window.open(citation.url, "_blank", "noopener,noreferrer");
    }
  };

  const handleAnalyze = (caseDetails: string) => {
    setIsAnalyzing(true);
    sendMessage({ case_details: caseDetails });
  };

  const hasMessages = messages.length > 0;

  return (
    <main className="flex h-screen bg-gray-100 overflow-hidden text-gray-900 font-sans">
      {/* Sidebar - Navigation */}
      <div className="w-16 bg-gray-900 flex flex-col items-center py-6 space-y-8 text-gray-400">
        <Link href="/" className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white font-bold text-xl mb-4 hover:bg-blue-700 transition-colors">
          LB
        </Link>
        <Link href="/analysis" className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-white">
          <Search className="w-6 h-6" />
        </Link>
        <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
          <History className="w-6 h-6" />
        </button>
        <div className="flex-1" />
        <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
          <Info className="w-6 h-6" />
        </button>
        <button className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
          <Settings className="w-6 h-6" />
        </button>
      </div>

      {/* Main Layout: Split Screen */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Section: Form or Chat */}
        <div className="flex-1 border-r border-gray-200 shadow-xl z-10 flex flex-col">
          {!hasMessages ? (
            <AnalysisForm onSubmit={handleAnalyze} isLoading={!isConnected || isAnalyzing} />
          ) : (
            <Chat
              messages={messages}
              isConnected={isConnected}
              onSendMessage={sendMessage}
              onCitationClick={handleCitationClick}
            />
          )}
        </div>

        {/* Right Section: Sources Panel */}
        <div className="w-96 shadow-2xl z-10">
          <SourcesPanel
            citations={currentCitations}
            activeCitationId={activeCitation?.id}
            onCitationClick={handleCitationClick}
          />
        </div>
      </div>
    </main>
  );
}
