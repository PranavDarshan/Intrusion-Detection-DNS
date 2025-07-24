import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { IPData } from '../types';

interface IPStatsChartProps {
  ipStats: IPData[];
}

export const IPStatsChart: React.FC<IPStatsChartProps> = ({ ipStats }) => {
  // Take top 10 IPs by count
  const topIPs = ipStats
    .sort((a, b) => b.count - a.count)
    .slice(0, 10)
    .map(ip => ({
      ip: ip.SourceIP.length > 15 ? `${ip.SourceIP.substring(0, 12)}...` : ip.SourceIP,
      count: ip.count,
      fullIP: ip.SourceIP
    }));

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="px-6 py-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold">Top Source IPs</h2>
        <p className="text-sm text-gray-400 mt-1">Most active source addresses</p>
      </div>
      
      <div className="p-6">
        {topIPs.length === 0 ? (
          <div className="text-center text-gray-400 py-8">
            No IP statistics available yet
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topIPs} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="ip" 
                stroke="#9CA3AF"
                angle={-45}
                textAnchor="end"
                height={80}
                interval={0}
              />
              <YAxis stroke="#9CA3AF" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#F9FAFB'
                }}
                formatter={(value, name, props) => [
                  `${value} flows`,
                  `IP: ${props.payload?.fullIP}`
                ]}
              />
              <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};