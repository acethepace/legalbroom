"use client";

import React, { useState, useEffect } from "react";
import Chat from "@/components/Chat";
import SourcesPanel from "@/components/SourcesPanel";
import { useChat, Citation } from "@/hooks/useChat";
import { Search, Settings, Info, History } from "lucide-react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const { messages, isConnected, sendMessage } = useChat();
  const [activeCitation, setActiveCitation] = useState<Citation | undefined>();
  const [currentCitations, setCurrentCitations] = useState<Citation[]>([]);

  // Update current citations when messages change
  useEffect(() => {
    const lastAssistantMessage = [...messages]
      .reverse()
      .find((m) => m.role === "assistant" && m.citations && m.citations.length > 0);
    
    if (lastAssistantMessage && lastAssistantMessage.citations) {
      setCurrentCitations(lastAssistantMessage.citations);
    }
  }, [messages]);

  const handleCitationClick = (citation: Citation) => {
    setActiveCitation(citation);
    // Open the URL in a new tab when a citation is clicked
    if (citation.url) {
      window.open(citation.url, "_blank", "noopener,noreferrer");
    }
  };

  return (
    <main className="flex h-screen bg-gray-100 overflow-hidden text-gray-900 font-sans">
      {/* Sidebar - Navigation */}
      <div className="w-16 bg-gray-900 flex flex-col items-center py-6 space-y-8 text-gray-400">
        <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white font-bold text-xl mb-4">
          LB
        </div>
        <button 
          onClick={() => router.push('/analysis')}
          className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-white"
        >
          <Search className="w-6 h-6" />
        </button>
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
        {/* Left Section: Chat (Main Driver) */}
        <div className="flex-1 border-r border-gray-200 shadow-xl z-10">
          <Chat
            messages={messages}
            isConnected={isConnected}
            onSendMessage={sendMessage}
            onCitationClick={handleCitationClick}
          />
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
