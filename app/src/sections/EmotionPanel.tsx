import { useEffect, useState } from 'react';
import { TrendingUp, TrendingDown, Minus, Brain } from 'lucide-react';

interface EmotionPanelProps {
  emotions: Record<string, number>;
  isOpen: boolean;
}

const EMOTION_CONFIG: Record<string, { color: string; icon: string; label: string }> = {
  joy: { color: 'bg-green-500', icon: '😊', label: 'Joy' },
  sadness: { color: 'bg-blue-500', icon: '😢', label: 'Sadness' },
  anger: { color: 'bg-red-500', icon: '😠', label: 'Anger' },
  fear: { color: 'bg-purple-500', icon: '😨', label: 'Fear' },
  surprise: { color: 'bg-yellow-500', icon: '😲', label: 'Surprise' },
  neutral: { color: 'bg-gray-500', icon: '😐', label: 'Neutral' }
};

export default function EmotionPanel({ emotions, isOpen }: EmotionPanelProps) {
  const [prevEmotions, setPrevEmotions] = useState(emotions);
  const [trends, setTrends] = useState<Record<string, 'up' | 'down' | 'stable'>>({});

  // Calculate trends
  useEffect(() => {
    const newTrends: Record<string, 'up' | 'down' | 'stable'> = {};
    
    Object.entries(emotions).forEach(([emotion, value]) => {
      const prevValue = prevEmotions[emotion] || 0;
      const diff = value - prevValue;
      
      if (diff > 0.05) {
        newTrends[emotion] = 'up';
      } else if (diff < -0.05) {
        newTrends[emotion] = 'down';
      } else {
        newTrends[emotion] = 'stable';
      }
    });
    
    setTrends(newTrends);
    setPrevEmotions(emotions);
  }, [emotions]);

  const getDominantEmotion = () => {
    return Object.entries(emotions)
      .sort(([,a], [,b]) => b - a)[0];
  };

  const [dominantEmotion, dominantScore] = getDominantEmotion();
  const config = EMOTION_CONFIG[dominantEmotion] || EMOTION_CONFIG.neutral;

  if (!isOpen) return null;

  return (
    <aside className="fixed right-0 top-16 bottom-0 w-72 bg-slate-900/90 backdrop-blur-md border-l border-white/10 flex flex-col z-40 overflow-hidden">
      <div className="p-4 border-b border-white/10">
        <div className="flex items-center gap-2 mb-4">
          <Brain className="w-5 h-5 text-purple-400" />
          <h2 className="text-lg font-semibold text-white">Emotion Analysis</h2>
        </div>

        {/* Dominant Emotion Card */}
        <div className="p-4 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30">
          <p className="text-sm text-white/50 mb-1">Current Mood</p>
          <div className="flex items-center gap-3">
            <span className="text-4xl">{config.icon}</span>
            <div>
              <p className="text-2xl font-bold text-white capitalize">{config.label}</p>
              <p className="text-sm text-white/50">{Math.round(dominantScore * 100)}% confidence</p>
            </div>
          </div>
        </div>
      </div>

      {/* Emotion Bars */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        <p className="text-sm text-white/50 mb-3">Emotion Breakdown</p>
        
        {Object.entries(emotions)
          .sort(([,a], [,b]) => b - a)
          .map(([emotion, score]) => {
            const emotionConfig = EMOTION_CONFIG[emotion] || EMOTION_CONFIG.neutral;
            const trend = trends[emotion];
            
            return (
              <div key={emotion} className="space-y-1">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{emotionConfig.icon}</span>
                    <span className="text-sm text-white/70 capitalize">{emotion}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-white/50">{Math.round(score * 100)}%</span>
                    {trend === 'up' && <TrendingUp className="w-3 h-3 text-green-400" />}
                    {trend === 'down' && <TrendingDown className="w-3 h-3 text-red-400" />}
                    {trend === 'stable' && <Minus className="w-3 h-3 text-gray-400" />}
                  </div>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${emotionConfig.color}`}
                    style={{ width: `${score * 100}%` }}
                  />
                </div>
              </div>
            );
          })}
      </div>

      {/* Sentiment Indicator */}
      <div className="p-4 border-t border-white/10">
        <div className="flex items-center justify-between">
          <span className="text-sm text-white/50">Overall Sentiment</span>
          <span className={`text-sm font-medium ${
            dominantScore > 0.5 && dominantEmotion === 'joy' ? 'text-green-400' :
            dominantEmotion === 'sadness' || dominantEmotion === 'fear' ? 'text-red-400' :
            'text-yellow-400'
          }`}>
            {dominantScore > 0.5 && dominantEmotion === 'joy' ? 'Positive' :
             dominantEmotion === 'sadness' || dominantEmotion === 'fear' ? 'Needs Support' :
             'Neutral'}
          </span>
        </div>
      </div>
    </aside>
  );
}
