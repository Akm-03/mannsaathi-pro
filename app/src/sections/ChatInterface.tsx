import { useState, useRef, useCallback } from 'react';
import { Send, Mic, MicOff, Image as ImageIcon, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';

interface ChatInterfaceProps {
  onSendMessage: (message: string, inputMode: 'text' | 'voice') => void;
  onImageUpload: (imageData: string) => void;
  isTyping: boolean;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AnyType = any;

export default function ChatInterface({ 
  onSendMessage, 
  onImageUpload,
  isTyping 
}: ChatInterfaceProps) {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [transcript, setTranscript] = useState('');
  
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<AnyType>(null);

  // Auto-resize textarea
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 150)}px`;
  };

  // Handle send
  const handleSend = () => {
    if (message.trim() && !isTyping) {
      onSendMessage(message.trim(), 'text');
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  // Handle key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Voice recording
  const toggleRecording = useCallback(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition = (window as AnyType).SpeechRecognition || (window as AnyType).webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      toast.error('Speech recognition is not supported in your browser');
      return;
    }

    if (isRecording) {
      recognitionRef.current?.stop();
      setIsRecording(false);
      
      // Send transcribed message
      if (transcript.trim()) {
        onSendMessage(transcript.trim(), 'voice');
        setTranscript('');
      }
    } else {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'hi-IN';

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      recognitionRef.current.onresult = (event: AnyType) => {
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i];
          if (result.isFinal) {
            finalTranscript += result[0].transcript;
          }
        }

        if (finalTranscript) {
          setTranscript(prev => prev + finalTranscript);
        }
      };

      recognitionRef.current.onerror = () => {
        toast.error('Speech recognition error. Please try again.');
        setIsRecording(false);
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current.start();
      setIsRecording(true);
      setTranscript('');
      toast.info('Listening... Speak now');
    }
  }, [isRecording, transcript, onSendMessage]);

  // Image upload
  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast.error('Please select an image file');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const imageData = event.target?.result as string;
      setSelectedImage(imageData);
      onImageUpload(imageData);
      toast.success('Image uploaded for emotion analysis');
    };
    reader.readAsDataURL(file);
  };

  const clearImage = () => {
    setSelectedImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="border-t border-white/10 bg-slate-900/80 backdrop-blur-md p-4">
      {/* Image Preview */}
      {selectedImage && (
        <div className="mb-3 flex items-center gap-2">
          <div className="relative">
            <img 
              src={selectedImage} 
              alt="Selected" 
              className="h-16 w-16 object-cover rounded-lg border border-white/20"
            />
            <button
              onClick={clearImage}
              className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-white text-xs"
            >
              <X className="w-3 h-3" />
            </button>
          </div>
          <span className="text-sm text-white/50">Image selected for analysis</span>
        </div>
      )}

      {/* Voice Transcript */}
      {isRecording && transcript && (
        <div className="mb-3 p-3 rounded-lg bg-white/5 border border-white/10">
          <p className="text-sm text-white/70">{transcript}</p>
        </div>
      )}

      {/* Input Area */}
      <div className="flex items-end gap-2">
        {/* Image Upload Button */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleImageSelect}
          accept="image/*"
          className="hidden"
        />
        <Button
          variant="ghost"
          size="icon"
          onClick={() => fileInputRef.current?.click()}
          className="text-white/50 hover:text-white hover:bg-white/10 shrink-0"
          disabled={isTyping}
        >
          <ImageIcon className="w-5 h-5" />
        </Button>

        {/* Voice Button */}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleRecording}
          className={`shrink-0 ${
            isRecording 
              ? 'text-red-400 bg-red-400/20 animate-pulse' 
              : 'text-white/50 hover:text-white hover:bg-white/10'
          }`}
          disabled={isTyping}
        >
          {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
        </Button>

        {/* Text Input */}
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={handleInput}
            onKeyDown={handleKeyPress}
            placeholder={isRecording ? 'Listening...' : 'Type your message in Hinglish, Hindi, or English...'}
            className="min-h-[44px] max-h-[150px] bg-white/5 border-white/10 text-white placeholder:text-white/30 resize-none pr-12"
            disabled={isTyping || isRecording}
            rows={1}
          />
        </div>

        {/* Send Button */}
        <Button
          onClick={handleSend}
          disabled={!message.trim() || isTyping || isRecording}
          className="shrink-0 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
        >
          <Send className="w-5 h-5" />
        </Button>
      </div>

      {/* Quick Suggestions */}
      {!message && !isRecording && (
        <div className="mt-3 flex flex-wrap gap-2">
          {['mujhe tension ho rahi hai', 'main bahot udaas hoon', 'ghar mein problems hain'].map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => setMessage(suggestion)}
              className="px-3 py-1 text-xs rounded-full bg-white/5 text-white/50 hover:bg-white/10 hover:text-white/70 transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
