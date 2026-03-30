import { AlertTriangle, Phone, X, Heart, ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import type { CrisisInfo } from '../App';

interface CrisisAlertProps {
  crisisInfo: CrisisInfo;
  onClose: () => void;
}

export default function CrisisAlert({ crisisInfo, onClose }: CrisisAlertProps) {
  if (!crisisInfo.isCrisis) return null;

  const severityColor = crisisInfo.severity === 'critical' ? 'red' : 
                        crisisInfo.severity === 'high' ? 'orange' : 'yellow';

  return (
    <div className="p-4 animate-in slide-in-from-top">
      <Alert className={`border-${severityColor}-500 bg-${severityColor}-500/10`}>
        <AlertTriangle className={`h-5 w-5 text-${severityColor}-400`} />
        <div className="flex-1">
          <AlertTitle className={`text-${severityColor}-400 font-semibold flex items-center gap-2`}>
            Crisis Support Available
            <span className={`px-2 py-0.5 text-xs rounded-full bg-${severityColor}-500/20 text-${severityColor}-400 uppercase`}>
              {crisisInfo.severity}
            </span>
          </AlertTitle>
          <AlertDescription className="mt-2 text-white/70">
            {crisisInfo.message}
          </AlertDescription>
          
          {/* Helplines */}
          {crisisInfo.helplines && crisisInfo.helplines.length > 0 && (
            <div className="mt-4 grid gap-2">
              <p className="text-sm text-white/50 font-medium">Available Helplines:</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {crisisInfo.helplines.slice(0, 4).map((helpline, index) => (
                  <a
                    key={index}
                    href={`tel:${helpline.number.replace(/[^\d]/g, '')}`}
                    className="flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors group"
                  >
                    <div className={`w-10 h-10 rounded-full bg-${severityColor}-500/20 flex items-center justify-center`}>
                      <Phone className={`w-5 h-5 text-${severityColor}-400`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white truncate">{helpline.name}</p>
                      <p className={`text-lg font-bold text-${severityColor}-400`}>{helpline.number}</p>
                      <p className="text-xs text-white/50">{helpline.hours}</p>
                    </div>
                    <ExternalLink className="w-4 h-4 text-white/30 group-hover:text-white/50" />
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Immediate Actions */}
          <div className="mt-4 p-3 rounded-lg bg-white/5">
            <p className="text-sm text-white/50 font-medium mb-2">Immediate Actions:</p>
            <ul className="space-y-1 text-sm text-white/70">
              <li className="flex items-start gap-2">
                <Heart className="w-4 h-4 text-pink-400 mt-0.5 shrink-0" />
                <span>Call a trusted friend or family member</span>
              </li>
              <li className="flex items-start gap-2">
                <Heart className="w-4 h-4 text-pink-400 mt-0.5 shrink-0" />
                <span>Go to a safe place (hospital, police station)</span>
              </li>
              <li className="flex items-start gap-2">
                <Heart className="w-4 h-4 text-pink-400 mt-0.5 shrink-0" />
                <span>Remove any means of self-harm from your vicinity</span>
              </li>
            </ul>
          </div>

          {/* Emergency Services */}
          <div className="mt-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <a 
                href="tel:112" 
                className="flex items-center gap-2 text-red-400 hover:text-red-300"
              >
                <Phone className="w-4 h-4" />
                <span className="font-bold">Emergency: 112</span>
              </a>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="text-white/50 hover:text-white hover:bg-white/10"
            >
              <X className="w-4 h-4 mr-1" />
              Dismiss
            </Button>
          </div>
        </div>
      </Alert>
    </div>
  );
}
