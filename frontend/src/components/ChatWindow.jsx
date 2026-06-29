import React, { useState } from 'react';
import { Send, Bot, User } from 'lucide-react';
import EvidenceCard from './EvidenceCard';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "Hello. I am the Autopsy AI Investigator. How can I help you analyze your behavioral data today?", evidence: [] }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;
    
    // Optimistically add user message
    const newMessages = [...messages, { role: 'user', text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);
    
    // Mocking API call to FastAPI /ai/chat/message
    setTimeout(() => {
      setMessages([...newMessages, { 
        role: 'assistant', 
        text: "According to your behavioral snapshot, your context-switching increased by 40% over the last 3 days, primarily driven by late-night YouTube sessions, which is fracturing your deep work.",
        evidence: [
          { document_type: 'Habit', text: 'Your context-switching increased by 40% over the last 3 days due to late-night YouTube.' }
        ]
      }]);
      setLoading(false);
    }, 1200);
  };

  return (
    <div className="flex flex-col h-[600px] bg-gray-900 rounded-xl border border-gray-800 overflow-hidden text-white">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700 flex items-center gap-3">
        <div className="bg-blue-600 p-2 rounded-lg">
          <Bot size={20} className="text-white" />
        </div>
        <div>
          <h2 className="font-bold">AI Investigator</h2>
          <p className="text-xs text-gray-400">RAG-Powered Behavioral Analysis</p>
        </div>
      </div>
      
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] ${msg.role === 'user' ? 'bg-blue-600 rounded-l-xl rounded-tr-xl text-white p-3' : ''}`}>
              
              {msg.role === 'assistant' && (
                <div className="flex gap-3 mb-2">
                   <div className="h-8 w-8 bg-gray-800 rounded-full flex items-center justify-center shrink-0 border border-gray-700">
                     <Bot size={16} className="text-blue-400" />
                   </div>
                   <div className="pt-1 text-gray-200 leading-relaxed">
                     {msg.text}
                   </div>
                </div>
              )}

              {msg.role === 'user' && (
                <div className="leading-relaxed">
                  {msg.text}
                </div>
              )}
              
              {msg.evidence && msg.evidence.length > 0 && (
                <div className="ml-11">
                  <EvidenceCard evidence={msg.evidence} />
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
             <div className="h-8 w-8 bg-gray-800 rounded-full flex items-center justify-center shrink-0 border border-gray-700">
               <Bot size={16} className="text-gray-500" />
             </div>
             <div className="pt-2 text-gray-500 italic text-sm">Analyzing vectors...</div>
          </div>
        )}
      </div>
      
      {/* Input Area */}
      <div className="p-4 bg-gray-800 border-t border-gray-700">
        <div className="flex gap-2">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about your productivity or habits..." 
            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          />
          <button 
            onClick={handleSend}
            className="bg-blue-600 hover:bg-blue-500 text-white p-2 px-4 rounded-lg flex items-center justify-center transition-colors"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
