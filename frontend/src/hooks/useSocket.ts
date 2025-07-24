import { useEffect, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { NetworkFlow, IPData, SocketResponse } from '../types';

export const useSocket = (serverUrl: string) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [flows, setFlows] = useState<NetworkFlow[]>([]);
  const [ipStats, setIpStats] = useState<IPData[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);

  useEffect(() => {
    // Connect to Flask-SocketIO backend
    const newSocket = io(serverUrl, {
      transports: ['polling', 'websocket'],
      timeout: 20000,
      forceNew: true,
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    
    });

    // Connect to the /test namespace after initial connection
    const testSocket = io(`${serverUrl}/test`, {
      transports: ['polling', 'websocket'],
      timeout: 20000,
      forceNew: true,
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    });

    testSocket.on('connect', () => {
      console.log('Connected to server');
      setIsConnected(true);
      setConnectionError(null);
    });

    testSocket.on('disconnect', () => {
      console.log('Disconnected from server');
      setIsConnected(false);
    });

    testSocket.on('connect_error', (error) => {
      console.error('Connection error:', error);
      setConnectionError(`Failed to connect to server: ${error.message}`);
      setIsConnected(false);
    });

    testSocket.on('reconnect_error', (error) => {
      console.error('Reconnection error:', error);
      setConnectionError(`Reconnection failed: ${error.message}`);
    });

    testSocket.on('newresult', (data: SocketResponse) => {
      console.log('New flow data:', data);
      
      try {
        // Parse the result array from Flask backend based on console output
        const result = data.result;
        
        // Map data according to the actual structure from console
        const newFlow: NetworkFlow = {
          FlowID: result[0] || 0,
          FlowDuration: 0, // Not directly available in the result array
          Src: (result[1] || '').replace(/<[^>]*>/g, ''), // Remove HTML tags
          SrcPort: result[2] || 0,
          Dest: (result[3] || '').replace(/<[^>]*>/g, ''), // Remove HTML tags
          DestPort: result[4] || 0,
          Protocol: result[5] || '',
          FlowStartTime: result[6] || new Date().toISOString(),
          FlowLastSeen: result[7] || new Date().toISOString(),
          PName: result[8] || '',
          PID: result[9] || '',
          Classification: result[10] || 'Unknown',
          Probability: result[11] || 0,
          Risk: result[12] || 'Unknown',
        };

        setFlows(prev => [newFlow, ...prev.slice(0, 99)]); // Keep last 100 flows
        setIpStats(data.ips || []);
      } catch (error) {
        console.error('Error parsing flow data:', error);
      }
    });

    setSocket(testSocket);

    return () => {
      testSocket.close();
      newSocket.close();
    };
  }, [serverUrl]);

  const clearFlows = useCallback(() => {
    setFlows([]);
  }, []);

  return {
    socket,
    flows,
    ipStats,
    isConnected,
    clearFlows,
    connectionError
  };
};