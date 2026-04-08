import { useState, useEffect, useRef, useCallback } from "react";

export interface Citation {
  id: string;
  title: string;
  court: string;
  date_filed: string;
  snippet: string;
  url: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  status?: string;
}

const DEFAULT_WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

export const useChat = (url?: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let wsUrl = url || DEFAULT_WS_URL;

    // If we're in the browser and using the default localhost URL, 
    // try to be smarter by using the current hostname
    if (!url && typeof window !== "undefined" && wsUrl.includes("localhost")) {
      const hostname = window.location.hostname;
      if (hostname !== "localhost") {
        wsUrl = wsUrl.replace("localhost", hostname);
      }
    }

    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("WebSocket connected");
      setIsConnected(true);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "status") {
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { ...lastMsg, status: data.text },
            ];
          }
          return prev;
        });
      } else if (data.type === "content") {
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { ...lastMsg, content: lastMsg.content + data.text, status: undefined },
            ];
          }
          return prev;
        });
      } else if (data.type === "citations") {
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { ...lastMsg, citations: data.payload },
            ];
          }
          return prev;
        });
      } else if (data.type === "error") {
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { ...lastMsg, content: lastMsg.content + (lastMsg.content ? "\n\n" : "") + "**Error:** " + data.text, status: undefined },
            ];
          }
          return prev;
        });
      }
    };

    socket.onclose = () => {
      console.log("WebSocket disconnected");
      setIsConnected(false);
    };

    return () => {
      socket.close();
    };
  }, [url]);

  const sendMessage = useCallback((content: string | Record<string, any>) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      const isObject = typeof content === 'object' && content !== null;
      const displayContent = isObject ? "Case details submitted for analysis." : content;
      const payload = isObject ? content : { message: content };

      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: displayContent as string,
      };
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "",
      };
      setMessages((prev) => [...prev, userMessage, assistantMessage]);
      socketRef.current.send(JSON.stringify(payload));
    }
  }, []);

  return {
    messages,
    isConnected,
    sendMessage,
  };
};
