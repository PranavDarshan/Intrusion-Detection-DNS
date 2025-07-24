import React from 'react';
import { Wifi, WifiOff } from 'lucide-react';

interface StatusIndicatorProps {
  isConnected: boolean;
  error?: string | null;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ isConnected, error }) => {
  return (
    <div className="flex items-center space-x-2">
      {error ? (
        <>
          <WifiOff className="h-5 w-5 text-red-400" />
          <span className="text-sm text-red-400">Connection Error</span>
        </>
      ) : isConnected ? (
        <>
          <Wifi className="h-5 w-5 text-green-400" />
          <span className="text-sm text-green-400">Connected</span>
        </>
      ) : (
        <>
          <WifiOff className="h-5 w-5 text-red-400" />
          <span className="text-sm text-red-400">Connecting...</span>
        </>
      )}
    </div>
  );
};