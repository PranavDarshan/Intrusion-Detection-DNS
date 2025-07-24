import React from 'react';
import { NetworkFlow } from '../types';
import { Eye, Shield, AlertTriangle } from 'lucide-react';

interface FlowTableProps {
  flows: NetworkFlow[];
  onFlowSelect: (flow: NetworkFlow) => void;
}

export const FlowTable: React.FC<FlowTableProps> = ({ flows, onFlowSelect }) => {
  const getRiskColor = (risk: string) => {
    if (typeof risk !== 'string') return 'text-gray-400';
    
    if (risk.includes('Very High')) return 'text-red-400';
    if (risk.includes('High')) return 'text-orange-400';
    if (risk.includes('Medium')) return 'text-yellow-400';
    if (risk.includes('Low')) return 'text-green-400';
    return 'text-blue-400';
  };

  const getClassificationIcon = (classification: string) => {
    if (classification === 'Benign') {
      return <Shield className="h-4 w-4 text-green-400" />;
    }
    return <AlertTriangle className="h-4 w-4 text-red-400" />;
  };

  const formatIP = (ip: string) => {
    // Remove HTML tags for display (flags will be handled separately)
    return ip.replace(/<[^>]*>/g, '');
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="px-6 py-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold">Network Flows</h2>
        <p className="text-sm text-gray-400 mt-1">Real-time network traffic analysis</p>
      </div>
      
      <div className="overflow-x-auto">
        <div className="max-h-96 overflow-y-auto">
          <table className="w-full">
            <thead className="bg-gray-700 sticky top-0">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Flow ID
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Source
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Destination
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Protocol
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Classification
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Risk
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {flows.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-400">
                    No network flows detected yet. Waiting for traffic...
                  </td>
                </tr>
              ) : (
                flows.map((flow, index) => (
                  <tr key={`${flow.FlowID}-${index}`} className="hover:bg-gray-750 transition-colors">
                    <td className="px-4 py-3 text-sm font-mono">
                      #{flow.FlowID}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <div className="flex flex-col">
                        <span className="font-mono">{formatIP(flow.Src || 'Unknown')}</span>
                        <span className="text-xs text-gray-400">:{flow.SrcPort}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <div className="flex flex-col">
                        <span className="font-mono">{formatIP(flow.Dest || 'Unknown')}</span>
                        <span className="text-xs text-gray-400">:{flow.DestPort}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span className="px-2 py-1 bg-blue-600 rounded text-xs">
                        {flow.Protocol || 'Unknown'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <div className="flex items-center space-x-2">
                        {getClassificationIcon(flow.Classification)}
                        <span className={flow.Classification === 'Benign' ? 'text-green-400' : 'text-red-400'}>
                          {flow.Classification}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span className={getRiskColor(flow.Risk)}>
                        {typeof flow.Risk === 'string' ? flow.Risk.replace(/<[^>]*>/g, '') : 'Unknown'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <button
                        onClick={() => onFlowSelect(flow)}
                        className="flex items-center space-x-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded transition-colors"
                      >
                        <Eye className="h-4 w-4" />
                        <span>Details</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};