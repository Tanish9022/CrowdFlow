import React, { useState, useEffect } from 'react';
import { Camera, AlertTriangle, ShieldAlert, Activity, RefreshCw } from 'lucide-react';

export default function Navbar({ networkSummary, onRefresh }) {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const blockedCount = networkSummary?.active_disruptions?.length || 0;
  const avgLoad = networkSummary?.average_network_occupancy ? Math.round(networkSummary.average_network_occupancy * 100) : 28;

  return (
    <header className="topbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--traffic-open)', boxShadow: '0 0 8px var(--traffic-open)' }}></div>
          <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>
            Pune Central TOC • Live
          </span>
        </div>
        <span className="mono" style={{ fontSize: '14px', color: 'var(--text-primary)', background: 'var(--bg-tertiary)', padding: '4px 10px', borderRadius: '4px', fontWeight: 600 }}>
          {time}
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
        {/* KPI Pills */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: 'var(--text-muted)' }}>
          <Camera size={16} color="var(--text-secondary)" />
          <span>Feeds:</span>
          <strong className="mono" style={{ color: 'var(--text-primary)', fontSize: '14px' }}>6 Online</strong>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: 'var(--text-muted)' }}>
          <Activity size={16} color="var(--traffic-open)" />
          <span>Network Load:</span>
          <strong className="mono" style={{ color: avgLoad > 75 ? 'var(--traffic-congested)' : 'var(--text-primary)', fontSize: '14px' }}>{avgLoad}%</strong>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: 'var(--text-muted)' }}>
          <ShieldAlert size={16} color={blockedCount > 0 ? 'var(--traffic-blocked)' : 'var(--traffic-open)'} />
          <span>Blocked Pieces:</span>
          <strong className="mono" style={{ color: blockedCount > 0 ? 'var(--traffic-blocked)' : 'var(--traffic-open)', fontSize: '14px' }}>
            {blockedCount}
          </strong>
        </div>

        <button onClick={onRefresh} className="btn btn-outline" style={{ padding: '8px 16px', fontSize: '13px', marginLeft: '12px' }}>
          <RefreshCw size={14} />
          Sync Network
        </button>
      </div>
    </header>
  );
}
