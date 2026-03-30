import { Trash2, Phone, Info, BarChart3 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

interface SidebarProps {
  isOpen: boolean;
  sessionId: string;
  messageCount: number;
  currentEmotions: Record<string, number>;
  onClearChat: () => void;
}

const HELPLINES = [
  { name: 'Vandrevala Foundation', number: '1860-2662-345', available: '24/7' },
  { name: 'AASRA', number: '91-22-27546669', available: '24/7' },
  { name: 'iCall', number: '022-25521111', available: 'Mon-Sat 10am-8pm' },
  { name: 'Kiran Helpline', number: '1800-599-0019', available: '24/7' },
];

export default function Sidebar({ 
  isOpen, 
  sessionId, 
  messageCount, 
  currentEmotions,
  onClearChat 
}: SidebarProps) {
  if (!isOpen) return null;

  const getDominantEmotion = () => {
    return Object.entries(currentEmotions)
      .sort(([,a], [,b]) => b - a)[0]?.[0] || 'neutral';
  };

  return (
    <aside className="fixed left-0 top-16 bottom-0 w-80 bg-slate-900/90 backdrop-blur-md border-r border-white/10 flex flex-col z-40">
      <ScrollArea className="flex-1 p-4">
        {/* Session Info */}
        <div className="mb-6 p-4 rounded-xl bg-white/5 border border-white/10">
          <h3 className="text-sm font-medium text-white/70 mb-2">Session Info</h3>
          <div className="space-y-1 text-xs">
            <p className="text-white/50">
              ID: <span className="text-white/70 font-mono">{sessionId.slice(0, 8)}...</span>
            </p>
            <p className="text-white/50">
              Messages: <span className="text-white/70">{messageCount}</span>
            </p>
            <p className="text-white/50 flex items-center gap-2">
              Current Mood: 
              <span className={`capitalize font-medium ${
                getDominantEmotion() === 'joy' ? 'text-green-400' :
                getDominantEmotion() === 'sadness' ? 'text-blue-400' :
                getDominantEmotion() === 'anger' ? 'text-red-400' :
                getDominantEmotion() === 'fear' ? 'text-purple-400' :
                'text-white/70'
              }`}>
                {getDominantEmotion()}
              </span>
            </p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-white/70 mb-3">Quick Actions</h3>
          <div className="space-y-2">
            <Button 
              variant="ghost" 
              className="w-full justify-start text-white/70 hover:text-white hover:bg-white/10"
              onClick={onClearChat}
            >
              <Trash2 className="w-4 h-4 mr-2" />
              Clear Chat
            </Button>
            
            <Dialog>
              <DialogTrigger asChild>
                <Button 
                  variant="ghost" 
                  className="w-full justify-start text-white/70 hover:text-white hover:bg-white/10"
                >
                  <BarChart3 className="w-4 h-4 mr-2" />
                  View Analytics
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-slate-800 border-white/10 text-white max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Session Analytics</DialogTitle>
                  <DialogDescription className="text-white/50">
                    Overview of your conversation patterns
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 rounded-lg bg-white/5">
                      <p className="text-sm text-white/50">Total Messages</p>
                      <p className="text-2xl font-bold text-white">{messageCount}</p>
                    </div>
                    <div className="p-4 rounded-lg bg-white/5">
                      <p className="text-sm text-white/50">Dominant Emotion</p>
                      <p className="text-2xl font-bold capitalize text-purple-400">
                        {getDominantEmotion()}
                      </p>
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-lg bg-white/5">
                    <p className="text-sm text-white/50 mb-3">Emotion Distribution</p>
                    <div className="space-y-2">
                      {Object.entries(currentEmotions)
                        .sort(([,a], [,b]) => b - a)
                        .map(([emotion, score]) => (
                          <div key={emotion} className="flex items-center gap-2">
                            <span className="text-xs text-white/70 w-20 capitalize">{emotion}</span>
                            <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                              <div 
                                className={`h-full rounded-full ${
                                  emotion === 'joy' ? 'bg-green-500' :
                                  emotion === 'sadness' ? 'bg-blue-500' :
                                  emotion === 'anger' ? 'bg-red-500' :
                                  emotion === 'fear' ? 'bg-purple-500' :
                                  emotion === 'surprise' ? 'bg-yellow-500' :
                                  'bg-gray-500'
                                }`}
                                style={{ width: `${score * 100}%` }}
                              />
                            </div>
                            <span className="text-xs text-white/50 w-12 text-right">
                              {Math.round(score * 100)}%
                            </span>
                          </div>
                        ))}
                    </div>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        {/* Helplines */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-white/70 mb-3 flex items-center gap-2">
            <Phone className="w-4 h-4 text-pink-400" />
            Emergency Helplines
          </h3>
          <div className="space-y-2">
            {HELPLINES.map((helpline) => (
              <div 
                key={helpline.number}
                className="p-3 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-colors"
              >
                <p className="text-sm font-medium text-white">{helpline.name}</p>
                <p className="text-lg font-bold text-pink-400">{helpline.number}</p>
                <p className="text-xs text-white/50">{helpline.available}</p>
              </div>
            ))}
          </div>
        </div>

        {/* About */}
        <div>
          <Dialog>
            <DialogTrigger asChild>
              <Button 
                variant="ghost" 
                className="w-full justify-start text-white/70 hover:text-white hover:bg-white/10"
              >
                <Info className="w-4 h-4 mr-2" />
                About MannSaathi
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-slate-800 border-white/10 text-white max-w-lg">
              <DialogHeader>
                <DialogTitle>About MannSaathi Pro</DialogTitle>
                <DialogDescription className="text-white/50">
                  Your AI-powered mental health companion
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 text-sm text-white/70">
                <p>
                  MannSaathi Pro is an advanced mental health support system designed specifically 
                  for Indian users. It understands code-mixed Hinglish, analyzes emotions from 
                  multiple modalities, and provides culturally appropriate responses.
                </p>
                <div className="space-y-2">
                  <p className="font-medium text-white">Key Features:</p>
                  <ul className="list-disc list-inside space-y-1 text-white/60">
                    <li>Multilingual support (8 Indian languages)</li>
                    <li>Text, voice, and image emotion analysis</li>
                    <li>Crisis detection with helpline integration</li>
                    <li>Culturally adaptive responses</li>
                    <li>Privacy-focused design</li>
                  </ul>
                </div>
                <p className="text-xs text-white/40">
                  Disclaimer: MannSaathi is a supportive tool and not a replacement for 
                  professional mental health care.
                </p>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </ScrollArea>
    </aside>
  );
}
