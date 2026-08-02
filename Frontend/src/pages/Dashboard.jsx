import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  //  Fetch dynamic aggregation dashboard metrics from backend
  useEffect(() => {
    fetch('/api/citizen/dashboard-metrics')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to pull system telemetry dashboard metrics.');
        return res.json();
      })
      .then((data) => {
        setMetrics(data); 
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-8 text-slate-500 animate-pulse">Loading dashboard telemetry...</div>;
  if (error) return <div className="p-8 text-red-500 font-medium">Error: {error}</div>;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Welcome Banner Section */}
      <div className="bg-slate-800 p-8 rounded-xl shadow-sm text-white">
        <h1 className="text-3xl font-bold tracking-tight">Citizen Dashboard</h1>
        <p className="text-slate-300 text-lg mt-2">Welcome back to your unified County Portal. Manage your services cleanly online.</p>
      </div>

      {/* Metrics Layout Configuration Grid */}
      <div>
        <h2 className="text-xl font-bold text-slate-900 mb-4">Application Statistics Summary</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card title="Submitted" value={metrics?.submitted ?? 0} type="info" />
          <Card title="Under Review" value={metrics?.pending ?? 0} type="warning" />
          <Card title="Approved" value={metrics?.approved ?? 0} type="success" />
          <Card title="Rejected" value={metrics?.rejected ?? 0} type="danger" />
        </div>
      </div>
    </div>
  );
}

//Reusable Visual Metric Dashboard Card 
function Card({ title, value, type }) {
  const typeStyles = {
    success: 'border-l-4 border-green-500',
    warning: 'border-l-4 border-amber-500',
    danger: 'border-l-4 border-red-500',
    info: 'border-l-4 border-blue-500',
  };

  return (
    <div className={`bg-white shadow-sm border border-slate-200/80 rounded-xl p-6 transition-all hover:shadow-md ${typeStyles[type] || ''}`}>
      <h3 className="text-sm font-semibold tracking-wide uppercase text-slate-500">{title}</h3>
      <p className="text-4xl font-extrabold text-slate-900 mt-2 tracking-tight">
        {value.toLocaleString()}
      </p>
    </div>
  );
}