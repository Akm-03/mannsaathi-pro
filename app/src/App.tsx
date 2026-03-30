import { useState, useEffect, useRef } from 'react';
import { Toaster, toast } from 'sonner';
import ChatInterface from './sections/ChatInterface';
import EmotionPanel from './sections/EmotionPanel';
import CrisisAlert from './sections/CrisisAlert';
import Sidebar from './sections/Sidebar';
import Header from './sections/Header';
import { v4 as uuidv4 } from 'uuid';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  emotions?: Record<string, number>;
  dominantEmotion?: string;
  inputMode?: 'text' | 'voice' | 'image';
}

export interface CrisisInfo {
  isCrisis: boolean;
  tier?: number;
  severity?: string;
  helplines?: Helpline[];
  message?: string;
}

export interface Helpline {
  name: string;
  number: string;
  hours: string;
  languages: string[];
}

function App() {
  const [sessionId] = useState(() => uuidv4());
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentEmotions, setCurrentEmotions] = useState<Record<string, number>>({
    sadness: 0,
    fear: 0,
    anger: 0,
    joy: 0,
    surprise: 0,
    neutral: 1
  });
  const [crisisInfo, setCrisisInfo] = useState<CrisisInfo>({ isCrisis: false });
  const [isTyping, setIsTyping] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [language, setLanguage] = useState<'hinglish' | 'hindi' | 'english'>('hinglish');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Welcome message
  useEffect(() => {
    const welcomeMessage: Message = {
      id: uuidv4(),
      role: 'assistant',
      content: 'Namaste! Main MannSaathi hoon, aapka mental health companion. Aap jo bhi feel kar rahe hain, mujhse share kar sakte hain. Main yahan sunne aur support karne ke liye hoon. 🙏',
      timestamp: new Date()
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleSendMessage = async (content: string, inputMode: 'text' | 'voice' = 'text') => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: new Date(),
      inputMode
    };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const response = await fetch(`${API_URL}/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Session-ID': sessionId
        },
        body: JSON.stringify({
          message: content,
          session_id: sessionId,
          input_mode: inputMode
        })
      });

      const data = await response.json();

      if (data.success) {
        // Add assistant message
        const assistantMessage: Message = {
          id: uuidv4(),
          role: 'assistant',
          content: data.response,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, assistantMessage]);

        // Update emotions
        if (data.emotion_analysis) {
          setCurrentEmotions(data.emotion_analysis.emotions);
        }

        // Handle crisis
        if (data.crisis?.is_crisis) {
          setCrisisInfo({
            isCrisis: true,
            tier: data.crisis.tier,
            severity: data.crisis.severity,
            helplines: data.crisis.intervention?.helplines,
            message: data.crisis.intervention?.message
          });
          toast.error('Crisis detected - Helpline information provided', {
            duration: 10000
          });
        } else {
          setCrisisInfo({ isCrisis: false });
        }
      } else {
        toast.error('Failed to get response. Please try again.');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Network error. Please check your connection.');
    } finally {
      setIsTyping(false);
    }
  };

  const handleImageAnalysis = async (imageData: string) => {
    try {
      const response = await fetch(`${API_URL}/multimodal/analyze-image`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Session-ID': sessionId
        },
        body: JSON.stringify({
          image: imageData,
          session_id: sessionId
        })
      });

      const data = await response.json();

      if (data.success && data.faces_detected > 0) {
        // Update emotions based on facial analysis
        const faceEmotions = data.faces[0]?.emotions || {};
        setCurrentEmotions(prev => ({
          ...prev,
          ...faceEmotions
        }));
        toast.success(`Detected emotion: ${data.dominant_emotion}`);
      }
    } catch (error) {
      console.error('Error analyzing image:', error);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setCurrentEmotions({
      sadness: 0,
      fear: 0,
      anger: 0,
      joy: 0,
      surprise: 0,
      neutral: 1
    });
    setCrisisInfo({ isCrisis: false });
    toast.success('Chat cleared');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">
      <Toaster position="top-right" richColors />
      
      <Header 
        sidebarOpen={sidebarOpen}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        language={language}
        onLanguageChange={setLanguage}
      />

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <Sidebar 
          isOpen={sidebarOpen}
          sessionId={sessionId}
          messageCount={messages.length}
          currentEmotions={currentEmotions}
          onClearChat={handleClearChat}
        />

        {/* Main Chat Area */}
        <main className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'ml-80' : 'ml-0'}`}>
          {/* Crisis Alert */}
          {crisisInfo.isCrisis && (
            <CrisisAlert 
              crisisInfo={crisisInfo}
              onClose={() => setCrisisInfo({ isCrisis: false })}
            />
          )}

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-5 py-3 ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                      : 'bg-white/10 backdrop-blur-sm text-white border border-white/20'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <span className="text-xs opacity-50 mt-1 block">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white/10 backdrop-blur-sm rounded-2xl px-5 py-3 border border-white/20">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-white/50 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-white/50 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-white/50 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <ChatInterface 
            onSendMessage={handleSendMessage}
            onImageUpload={handleImageAnalysis}
            isTyping={isTyping}
          />
        </main>

        {/* Emotion Panel */}
        <EmotionPanel 
          emotions={currentEmotions}
          isOpen={sidebarOpen}
        />
      </div>
    </div>
  );
}

export default App;
