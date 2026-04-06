import { useState, useRef, useEffect } from 'react'
import './App.css'
import "tailwindcss"

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  condition?: string;
  confidence?: number;
}

const API_URL = 'http://localhost:8000';

async function sendMessage(message: string): Promise<{ response: string; detected_condition: string; confidence: number }> {
  const res = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  
  if (!res.ok) {
    throw new Error('Failed to get response from server');
  }
  
  return res.json();
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      text: input,
      sender: 'user',
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendMessage(input);
      
      const botMessage: Message = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        condition: data.detected_condition,
        confidence: data.confidence,
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Sorry, I could not process your message. Please ensure the server is running.',
        sender: 'bot',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      <header className="font-sans shadow-xl font-bold font-sm bg-black w-screen h-[8vh] m-auto py-8 px-10 fixed top-0 left-0">
        Mental health detection model
      </header>
      
      <img src='/ai2.png' className='w-[7vw] justify-self-center relative bottom-5'></img>
      
      <div 
        ref={chatContainerRef}
        className='font-sans shadow-xl bg-black w-[80vw] h-[60vh] overflow-auto rounded-2xl p-4 flex flex-col gap-3'
      >
        {messages.length === 0 && (
          <p className="text-gray-500 text-center mt-8">
            Share how you're feeling and I'll try to help...
          </p>
        )}
        
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`max-w-[70%] p-3 rounded-2xl ${
              msg.sender === 'user'
                ? 'bg-blue-600 self-end rounded-br-sm'
                : 'bg-gray-700 self-start rounded-bl-sm'
            }`}
          >
            <p className="text-white">{msg.text}</p>
            {msg.condition && (
              <p className="text-xs text-gray-300 mt-2">
                Detected: {msg.condition} ({(msg.confidence! * 100).toFixed(1)}% confidence)
              </p>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="bg-gray-700 self-start p-3 rounded-2xl rounded-bl-sm">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
            </div>
          </div>
        )}
      </div>
      
      <textarea 
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        className='font-sans resize-none [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none] bg-black min-w-[75vw] h-[5vh] m-1 py-3 px-7 rounded-full fixed bottom-6 left-[10vw]' 
        placeholder='Enter the text'
        disabled={isLoading}
      />
      
      <button 
        onClick={handleSend}
        disabled={isLoading || !input.trim()}
        className='font-sans bg-black w-[4vw] h-[5vh] py-3 px-4 rounded-full fixed bottom-7 right-[10vw] transition ease-in-out hover:scale-105 hover:bg-blue-900 disabled:opacity-50 disabled:hover:scale-100 disabled:hover:bg-black'
      >
        Send
      </button>
    </>
  )
};

export default App
