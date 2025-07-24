import React, { useState } from 'react';
import { useSocket } from '../hooks/useSocket';
import { NetworkFlow } from '../types';
import { FlowTable } from './FlowTable';
import { IPStatsChart } from './IPStatsChart';
import { FlowDetailModal } from './FlowDetailModal';
import { StatusIndicator } from './StatusIndicator';
import { Activity, Shield, AlertTriangle, Server } from 'lucide-react';

const BACKEND_URL = 'http://localhost:5000'; // Adjust to your Flask server

export const Dashboard: React.FC = () => {
  const { flows, ipStats, isConnected, clearFlows, connectionError } = useSocket(BACKEND_URL);
  const [selectedFlow, setSelectedFlow] = useState<NetworkFlow | null>(null);

  const threatCount = flows.filter(flow => 
    flow.Classification !== 'Benign' && flow.Classification !== 'Unknown'
  ).length;

  const riskStats = flows.reduce((acc, flow) => {
    if (typeof flow.Risk === 'string') {
      if (flow.Risk.includes('Very High')) acc.veryHigh++;
      else if (flow.Risk.includes('High')) acc.high++;
      else if (flow.Risk.includes('Medium')) acc.medium++;
      else if (flow.Risk.includes('Low')) acc.low++;
      else acc.minimal++;
    }
    return acc;
  }, { veryHigh: 0, high: 0, medium: 0, low: 0, minimal: 0 });

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Shield className="h-8 w-8 text-blue-400" />
            <h1 className="text-2xl font-bold">Network Flow Monitor</h1>
          </div>
          <div className="flex items-center space-x-4">
            <StatusIndicator isConnected={isConnected} error={connectionError} />
            <button
              onClick={clearFlows}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
            >
              Clear Flows
            </button>
          </div>
        </div>
      </header>

      {/* Connection Error Banner */}
      {connectionError && (
        <div className="bg-red-900 border-l-4 border-red-500 text-red-100 p-4 mx-6 mt-4 rounded">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-5 w-5 text-red-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm">
                <strong>Connection Error:</strong> {connectionError}
              </p>
              <p className="text-xs mt-1 text-red-200">
                Make sure your Flask server is running on {BACKEND_URL} with CORS enabled.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 p-6">
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="flex items-center">
            <Activity className="h-8 w-8 text-blue-400 mr-3" />
            <div>
              <p className="text-sm text-gray-400">Total Flows</p>
              <p className="text-2xl font-bold">{flows.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-red-400 mr-3" />
            <div>
              <p className="text-sm text-gray-400">Threats Detected</p>
              <p className="text-2xl font-bold text-red-400">{threatCount}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="flex items-center">
            <Server className="h-8 w-8 text-green-400 mr-3" />
            <div>
              <p className="text-sm text-gray-400">Unique IPs</p>
              <p className="text-2xl font-bold">{ipStats.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div>
            <p className="text-sm text-gray-400 mb-2">Risk Distribution</p>
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-red-400">Very High: {riskStats.veryHigh}</span>
                <span className="text-orange-400">High: {riskStats.high}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-yellow-400">Medium: {riskStats.medium}</span>
                <span className="text-green-400">Low: {riskStats.low}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 px-6 pb-6">
        {/* Flow Table */}
        <div className="lg:col-span-2">
          <FlowTable 
            flows={flows} 
            onFlowSelect={setSelectedFlow}
          />
        </div>

        {/* IP Statistics */}
        <div className="lg:col-span-1">
          <IPStatsChart ipStats={ipStats} />
        </div>
      </div>

      {/* Flow Detail Modal */}
      {selectedFlow && (
        <FlowDetailModal
          flow={selectedFlow}
          onClose={() => setSelectedFlow(null)}
        />
      )}
    </div>
  );
};