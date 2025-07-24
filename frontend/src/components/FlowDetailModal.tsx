import React, { useState, useEffect } from 'react';
import { NetworkFlow, FlowDetail } from '../types';
import { X, Shield, AlertTriangle, Clock, Server, ExternalLink } from 'lucide-react';
import axios from 'axios';

interface FlowDetailModalProps {
  flow: NetworkFlow;
  onClose: () => void;
}

export const FlowDetailModal: React.FC<FlowDetailModalProps> = ({ flow, onClose }) => {
  const [flowDetail, setFlowDetail] = useState<FlowDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFlowDetail = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:5000/flow-detail?flow_id=${flow.FlowID}`);
        setFlowDetail(response.data);
      } catch (error) {
        console.error('Failed to fetch flow details:', error);
        // Use the basic flow data if API fails
        setFlowDetail(flow);
      } finally {
        setLoading(false);
      }
    };

    fetchFlowDetail();
  }, [flow]);

  const getRiskColor = (risk: string) => {
    if (typeof risk !== 'string') return 'text-gray-400';
    
    if (risk.includes('Very High')) return 'text-red-400';
    if (risk.includes('High')) return 'text-orange-400';
    if (risk.includes('Medium')) return 'text-yellow-400';
    if (risk.includes('Low')) return 'text-green-400';
    return 'text-blue-400';
  };

  const formatIP = (ip: string) => {
    return ip?.replace(/<[^>]*>/g, '') || 'Unknown';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-lg border border-gray-700 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700">
          <div className="flex items-center space-x-3">
            {flow.Classification === 'Benign' ? (
              <Shield className="h-6 w-6 text-green-400" />
            ) : (
              <AlertTriangle className="h-6 w-6 text-red-400" />
            )}
            <h2 className="text-xl font-semibold">Flow #{flow.FlowID} Details</h2>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => window.open(`http://localhost:5000/flow-detail?flow_id=${flow.FlowID}`, '_blank')}
              className="flex items-center space-x-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
              title="Open in new tab"
            >
              <ExternalLink className="h-4 w-4" />
              <span className="text-sm">Open URL</span>
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400 mx-auto"></div>
            <p className="text-gray-400 mt-2">Loading flow details...</p>
          </div>
        ) : (
          <div className="p-6 space-y-6">
            {/* Basic Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Server className="h-5 w-5 text-blue-400" />
                  <span className="text-sm font-medium">Source</span>
                </div>
                <p className="font-mono text-lg">{formatIP(flow.Src)}</p>
                <p className="text-sm text-gray-400">Port: {flow.SrcPort}</p>
              </div>

              <div className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Server className="h-5 w-5 text-green-400" />
                  <span className="text-sm font-medium">Destination</span>
                </div>
                <p className="font-mono text-lg">{formatIP(flow.Dest)}</p>
                <p className="text-sm text-gray-400">Port: {flow.DestPort}</p>
              </div>

              <div className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Clock className="h-5 w-5 text-yellow-400" />
                  <span className="text-sm font-medium">Duration</span>
                </div>
                <p className="text-lg">{flow.FlowDuration?.toFixed(2) || 'N/A'} ms</p>
                <p className="text-sm text-gray-400">Protocol: {flow.Protocol}</p>
              </div>
            </div>

            {/* Classification & Risk */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <h3 className="text-lg font-semibold mb-3">Classification</h3>
                <div className="flex items-center space-x-2 mb-2">
                  {flow.Classification === 'Benign' ? (
                    <Shield className="h-5 w-5 text-green-400" />
                  ) : (
                    <AlertTriangle className="h-5 w-5 text-red-400" />
                  )}
                  <span className={`text-lg font-medium ${
                    flow.Classification === 'Benign' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {flow.Classification}
                  </span>
                </div>
                <p className="text-sm text-gray-400">
                  Confidence: {((flow.Probability || 0) * 100).toFixed(1)}%
                </p>
              </div>

              <div className="bg-gray-700 rounded-lg p-4">
                <h3 className="text-lg font-semibold mb-3">Risk Level</h3>
                <p className={`text-lg font-medium ${getRiskColor(flow.Risk)}`}>
                  {typeof flow.Risk === 'string' ? flow.Risk.replace(/<[^>]*>/g, '') : 'Unknown'}
                </p>
              </div>
            </div>

            {/* Flow Features */}
            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="text-lg font-semibold mb-3">Flow Features</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-gray-400">Duration:</span>
                  <p className="font-mono">{flow.FlowDuration?.toFixed(2) || 'N/A'}</p>
                </div>
                <div>
                  <span className="text-gray-400">Start Time:</span>
                  <p className="font-mono text-xs">{flow.FlowStartTime || 'N/A'}</p>
                </div>
                <div>
                  <span className="text-gray-400">Last Seen:</span>
                  <p className="font-mono text-xs">{flow.FlowLastSeen || 'N/A'}</p>
                </div>
                <div>
                  <span className="text-gray-400">Process:</span>
                  <p className="font-mono">{flow.PName || 'N/A'} ({flow.PID || 'N/A'})</p>
                </div>
              </div>
            </div>

            {/* ML Explanation */}
            {flowDetail?.explanation && (
              <div className="bg-gray-700 rounded-lg p-4">
                <h3 className="text-lg font-semibold mb-3">ML Model Explanation</h3>
                <div dangerouslySetInnerHTML={{ __html: flowDetail.explanation }} />
              </div>
            )}

            {/* Autoencoder Plot */}
            {flowDetail?.ae_plot && (
              <div className="bg-gray-700 rounded-lg p-4">
                <h3 className="text-lg font-semibold mb-3">Anomaly Detection</h3>
                <div dangerouslySetInnerHTML={{ __html: flowDetail.ae_plot }} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};