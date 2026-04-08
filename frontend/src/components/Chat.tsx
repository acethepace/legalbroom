"use client";

import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Message, Citation } from "../hooks/useChat";
import { Send, Loader2, Link2 } from "lucide-react";

interface ChatProps {
  messages: Message[];
  onSendMessage: (content: string) => void;
  isConnected: boolean;
  onCitationClick?: (citation: Citation) => void;
}

const Chat: React.FC<ChatProps> = ({
  messages,
  onSendMessage,
  isConnected,
  onCitationClick,
}) => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && isConnected) {
      onSendMessage(input);
      setInput("");
    }
  };

  // Custom renderer for markdown links to handle citations like [1]
  const components = {
    a: ({ node, ...props }: any) => {
      const content = props.children?.[0];
      if (typeof content === "string" && content.match(/^\[\d+\]$/)) {
        const index = parseInt(content.slice(1, -1)) - 1;
        return (
          <button
            onClick={() => {
              // We need to find the citation in the context of the message
              // This is a bit tricky since we don't have the message here
              // So we'll let the parent handle the click if possible
              // For now, just render it as a blue link
            }}
            className="text-blue-600 font-bold hover:underline"
          >
            {content}
          </button>
        );
      }
      return <a {...props} className="text-blue-500 hover:underline" />;
    },
  };

  return (
    <div className="flex flex-col h-full bg-white border-r border-gray-200">
      <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Legal Assistant</h2>
          <p className="text-xs text-gray-500">MVP Prototype v1.0</p>
        </div>
        <div className="flex items-center bg-white px-2 py-1 rounded-full border border-gray-200">
          <div
            className={`w-2 h-2 rounded-full mr-2 ${
              isConnected ? "bg-green-500" : "bg-red-500 animate-pulse"
            }`}
          />
          <span className="text-[10px] font-bold uppercase tracking-wider text-gray-600">
            {isConnected ? "Live" : "Connecting"}
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-gray-400 space-y-4">
            <div className="bg-gray-100 p-4 rounded-full">
              <Link2 className="w-8 h-8 opacity-50" />
            </div>
            <p className="text-sm font-medium">Ask a question about your documents</p>
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[85%] rounded-2xl p-4 shadow-sm ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-tr-none"
                  : "bg-gray-100 text-gray-800 rounded-tl-none border border-gray-200"
              }`}
            >
              <div className="text-[10px] font-bold uppercase tracking-widest mb-1 opacity-70">
                {msg.role === "user" ? "Client" : "Counsel"}
              </div>
              <div className="markdown-content text-sm leading-relaxed prose prose-sm max-w-none">
                {msg.status && (
                  <div className="flex items-center space-x-2 text-blue-600 font-medium mb-2 animate-pulse">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>{msg.status}</span>
                  </div>
                )}
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                    a: ({ node, children, ...props }: any) => {
                      const text = children?.[0];
                      if (typeof text === "string" && text.match(/^\[\d+\]$/)) {
                        const index = parseInt(text.slice(1, -1)) - 1;
                        return (
                          <button
                            onClick={() => {
                              if (msg.citations && msg.citations[index] && onCitationClick) {
                                onCitationClick(msg.citations[index]);
                              }
                            }}
                            className={`inline-flex items-center justify-center w-5 h-5 text-[10px] font-bold rounded-full ml-1 transition ${
                              msg.role === "user" 
                                ? "bg-white/20 text-white hover:bg-white/40" 
                                : "bg-blue-100 text-blue-700 hover:bg-blue-200"
                            }`}
                          >
                            {index + 1}
                          </button>
                        );
                      }
                      return <a {...props} className="underline">{children}</a>;
                    }
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={!isConnected}
            placeholder={
              isConnected ? "Inquire about legal precedents..." : "Awaiting connection..."
            }
            className="w-full bg-white border border-gray-300 rounded-xl px-4 py-3 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition disabled:bg-gray-100 disabled:cursor-not-allowed shadow-inner"
          />
          <button
            type="submit"
            disabled={!isConnected || !input.trim()}
            className="absolute right-2 p-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isConnected ? (
              <Send className="w-4 h-4" />
            ) : (
              <Loader2 className="w-4 h-4 animate-spin" />
            )}
          </button>
        </div>
        <p className="text-[10px] text-gray-400 mt-2 text-center">
          Powered by LegalBroom AI • Standard Legal Disclaimer Applies
        </p>
      </form>
    </div>
  );
};

export default Chat;
