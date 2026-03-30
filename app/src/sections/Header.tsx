import { Menu, Brain, Heart, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface HeaderProps {
  sidebarOpen: boolean;
  onToggleSidebar: () => void;
  language: 'hinglish' | 'hindi' | 'english';
  onLanguageChange: (lang: 'hinglish' | 'hindi' | 'english') => void;
}

export default function Header({ 
  onToggleSidebar,
  language,
  onLanguageChange 
}: HeaderProps) {
  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur-md border-b border-white/10 flex items-center justify-between px-4 z-50">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleSidebar}
          className="text-white hover:bg-white/10"
        >
          <Menu className="w-5 h-5" />
        </Button>
        
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">MannSaathi Pro</h1>
            <p className="text-xs text-white/50 flex items-center gap-1">
              <Heart className="w-3 h-3 text-pink-400" />
              Your Mental Health Companion
            </p>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Language Selector */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="text-white hover:bg-white/10 gap-2">
              <Globe className="w-4 h-4" />
              <span className="capitalize">{language}</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="bg-slate-800 border-white/10">
            <DropdownMenuItem 
              onClick={() => onLanguageChange('hinglish')}
              className="text-white hover:bg-white/10 cursor-pointer"
            >
              Hinglish (Roman)
            </DropdownMenuItem>
            <DropdownMenuItem 
              onClick={() => onLanguageChange('hindi')}
              className="text-white hover:bg-white/10 cursor-pointer"
            >
              Hindi (Devanagari)
            </DropdownMenuItem>
            <DropdownMenuItem 
              onClick={() => onLanguageChange('english')}
              className="text-white hover:bg-white/10 cursor-pointer"
            >
              English
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* Status Indicator */}
        <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/20 border border-green-500/30">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="text-xs text-green-400 font-medium">Online</span>
        </div>
      </div>
    </header>
  );
}
