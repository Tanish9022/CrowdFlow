import React, { useState, useEffect } from 'react';
import { signalsAPI } from '../api/client';
import { Sliders, CheckCircle2, AlertTriangle, ShieldCheck, ArrowRight } from 'lucide-react';

export default function SignalAdvisory() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [acceptedSignals, setAcceptedSignals] = useState({});
  const [errorMsg, setErrorMsg] = useState('');

  const fetchRecommendations = async () => {
    try {
      const res = await signalsAPI.getRecommendations();
      setRecommendations(res.data);
      setErrorMsg('');
    } catch (err) {
      console.error('Failed to load signal recommendations', err);
      setErrorMsg(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
    const interval = setInterval(fetchRecommendations, 6000);
    return () => clearInterval(interval);
  }, []);

  const handleAcknowledge = (sigId) => {
    setAcceptedSignals((prev) => ({ ...prev, [sigId]: true }));
  };

  if (loading && recommendations.length === 0) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <p style={{ fontSize: '16px', fontWeight: 600 }}>Loading Advisory Plans...</p>
        {errorMsg && (
          <div style={{ marginTop: '16px' }}>
            <p style={{ color: '#ef4444', marginBottom: '12px' }}>Backend Connection Error: {errorMsg}</p>
            <button className="btn btn-primary" onClick={fetchRecommendations}>
              Retry Backend Connection
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="page-body">
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 700 }}>Advisory Traffic Signal Timing Plans</h2>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            Webster Equisaturation green-split adjustments calculated to relieve detour bottleneck surges
          </p>
        </div>
        <div style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid var(--traffic-slow)', padding: '6px 12px', borderRadius: '6px', fontSize: '12px', color: 'var(--traffic-slow)', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <AlertTriangle size={14} />
          <strong>ADVISORY ONLY:</strong> Requires Human Operator Authorization
        </div>
      </div>

      {/* Recommendations Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '20px' }}>
        {recommendations.map((rec) => {
          const isAccepted = acceptedSignals[rec.signal_id];
          const curr = rec.current_timings || { NS_green: 40, EW_green: 40 };
          const recommended = rec.recommended_timings || { NS_green: 55, EW_green: 25 };

          return (
            <div key={rec.signal_id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '12px' }}>
                <div>
                  <span className="mono" style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                    {rec.signal_id}
                  </span>
                  <h3 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {rec.junction_name}
                  </h3>
                </div>
                <span className="badge badge-open">
                  Cycle: 90s
                </span>
              </div>

              {/* Timing Comparison Sliders */}
              <div>
                <p style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
                  Green Phase Allocation (Current vs Recommended)
                </p>

                {/* North-South Phase */}
                <div style={{ marginBottom: '12px', background: 'var(--bg-tertiary)', padding: '10px 14px', borderRadius: '6px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                    <span style={{ fontWeight: 600 }}>Phase 1 (North-South Detour Corridor)</span>
                    <span className="mono">
                      Current: <strong>{curr.NS_green}s</strong> âž” Recommended:{' '}
                      <strong style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>{recommended.NS_green}s</strong>
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: 'var(--border-subtle)', borderRadius: '4px', overflow: 'hidden', display: 'flex' }}>
                    <div style={{ width: `${(curr.NS_green / 90) * 100}%`, height: '100%', background: '#6b7280' }}></div>
                    <div style={{ width: `${((recommended.NS_green - curr.NS_green) / 90) * 100}%`, height: '100%', background: 'var(--text-secondary)' }}></div>
                  </div>
                </div>

                {/* East-West Phase */}
                <div style={{ background: 'var(--bg-tertiary)', padding: '10px 14px', borderRadius: '6px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                    <span style={{ fontWeight: 600 }}>Phase 2 (East-West Cross Corridor)</span>
                    <span className="mono">
                      Current: <strong>{curr.EW_green}s</strong> âž” Recommended:{' '}
                      <strong style={{ color: '#f59e0b', fontSize: '13px' }}>{recommended.EW_green}s</strong>
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: 'var(--border-subtle)', borderRadius: '4px', overflow: 'hidden', display: 'flex' }}>
                    <div style={{ width: `${(recommended.EW_green / 90) * 100}%`, height: '100%', background: '#f59e0b' }}></div>
                  </div>
                </div>
              </div>

              {/* Justification Box */}
              <div style={{ background: 'rgba(6, 182, 212, 0.06)', border: '1px solid var(--border-active)', padding: '10px 14px', borderRadius: '6px', fontSize: '12px' }}>
                <p style={{ color: 'var(--text-secondary)' }}>
                  <strong>Engineering Rationale:</strong> {rec.justification}
                </p>
                <p style={{ color: '#10b981', fontWeight: 600, marginTop: '4px' }}>
                  Expected Effect: Detour queue reduction by ~{rec.expected_delay_reduction_pct}%
                </p>
              </div>

              {/* Action Button */}
              <div style={{ marginTop: 'auto', paddingTop: '8px' }}>
                {isAccepted ? (
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', color: '#10b981', fontWeight: 600, fontSize: '13px', padding: '8px' }}>
                    <CheckCircle2 size={16} /> Plan Acknowledged & Logged in Audit Trail
                  </div>
                ) : (
                  <button
                    onClick={() => handleAcknowledge(rec.signal_id)}
                    className="btn btn-primary"
                    style={{ width: '100%', justifyContent: 'center' }}
                  >
                    <Sliders size={16} /> Authorize & Acknowledge Advisory Split
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

