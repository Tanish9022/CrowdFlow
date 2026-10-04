import React, { useState, useEffect } from 'react';
import { networkAPI, simulationAPI } from '../api/client';
import { PlayCircle, AlertTriangle, ArrowRight, ShieldAlert, CheckCircle, BarChart3 } from 'lucide-react';

export default function Simulator() {
  const [roads, setRoads] = useState([]);
  const [selectedRoadId, setSelectedRoadId] = useState('R03_JM_DECCAN');
  const [disruptionType, setDisruptionType] = useState('PROTEST');
  const [divertedVolume, setDivertedVolume] = useState(1200);
  const [loading, setLoading] = useState(false);
  const [simulationResult, setSimulationResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const fetchRoads = async () => {
    try {
      const res = await networkAPI.getRoads();
      setRoads(res.data);
      if (res.data.length > 0) setSelectedRoadId(res.data[2]?.road_id || res.data[0].road_id);
      setErrorMsg('');
    } catch (err) {
      console.error('Failed to load roads for simulator', err);
      setErrorMsg(err.message || String(err));
    }
  };

  useEffect(() => {
    fetchRoads();
  }, []);

  const handleRunSimulation = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await simulationAPI.runSimulation(selectedRoadId, disruptionType, Number(divertedVolume));
      setSimulationResult(res.data);
    } catch (err) {
      alert('Simulation failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  if (roads.length === 0) {
    return (
      <div className="page-body">
        <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <p style={{ fontSize: '16px', fontWeight: 600 }}>Loading Road Network for Simulator...</p>
          {errorMsg && (
            <div style={{ marginTop: '16px' }}>
              <p style={{ color: '#ef4444', marginBottom: '12px' }}>Backend Connection Error: {errorMsg}</p>
              <button className="btn btn-primary" onClick={fetchRoads}>
                Retry Backend Connection
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="page-body">
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 700 }}>What-If Traffic Redistribution Simulator</h2>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Model the systemic ripple effects of road closures and evaluate downstream capacity strain
        </p>
      </div>

      {/* Disruption Setup Card */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <form onSubmit={handleRunSimulation} style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr) auto', gap: '16px', alignItems: 'flex-end' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Target Road Link
            </label>
            <select
              value={selectedRoadId}
              onChange={(e) => setSelectedRoadId(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 12px',
                background: 'var(--bg-tertiary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-active)',
                borderRadius: '6px',
                fontSize: '13px'
              }}
            >
              {roads.map((r) => (
                <option key={r.road_id} value={r.road_id}>
                  {r.name} ({r.road_id})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Disruption Event
            </label>
            <select
              value={disruptionType}
              onChange={(e) => setDisruptionType(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 12px',
                background: 'var(--bg-tertiary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-active)',
                borderRadius: '6px',
                fontSize: '13px'
              }}
            >
              <option value="PROTEST">Public Protest / Gathering</option>
              <option value="ACCIDENT">Multi-Vehicle Collision</option>
              <option value="ROAD_CLOSURE">VIP Movement / Rally</option>
              <option value="CONSTRUCTION">Emergency Waterlogging</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Displaced Volume (vph)
            </label>
            <input
              type="number"
              value={divertedVolume}
              onChange={(e) => setDivertedVolume(e.target.value)}
              min="100"
              max="5000"
              style={{
                width: '100%',
                padding: '8px 12px',
                background: 'var(--bg-tertiary)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-active)',
                borderRadius: '6px',
                fontSize: '13px'
              }}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', height: '38px', color: 'var(--text-muted)', fontSize: '12px' }}>
            Model: Logit Choice + BPR
          </div>

          <div>
            <button type="submit" disabled={loading} className="btn btn-primary" style={{ height: '38px' }}>
              <PlayCircle size={16} />
              {loading ? 'Simulating...' : 'Run What-If Simulation'}
            </button>
          </div>
        </form>
      </div>

      {/* Simulation Results View */}
      {simulationResult && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Summary KPIs */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
            <div className="card">
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Displaced Flow
              </span>
              <h3 className="mono" style={{ fontSize: '22px', fontWeight: 700, color: 'var(--text-secondary)' }}>
                {simulationResult.displaced_volume_vph} <span style={{ fontSize: '12px' }}>vph</span>
              </h3>
            </div>

            <div className="card">
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Affected Corridors
              </span>
              <h3 className="mono" style={{ fontSize: '22px', fontWeight: 700, color: 'var(--text-primary)' }}>
                {simulationResult.total_affected_roads}
              </h3>
            </div>

            <div className="card">
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Overloaded Saturated Corridors
              </span>
              <h3 className="mono" style={{ fontSize: '22px', fontWeight: 700, color: simulationResult.overloaded_roads_count > 0 ? 'var(--traffic-congested)' : '#10b981' }}>
                {simulationResult.overloaded_roads_count} Links
              </h3>
            </div>

            <div className="card">
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Est. Delay Increase
              </span>
              <h3 className="mono" style={{ fontSize: '22px', fontWeight: 700, color: 'var(--traffic-slow)' }}>
                +{simulationResult.network_average_delay_increase_pct}%
              </h3>
            </div>
          </div>

          {/* Recommended Detour Path Pill */}
          {simulationResult.recommended_detour_path.length > 0 && (
            <div className="card" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--text-secondary)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontWeight: 700, color: 'var(--text-secondary)', fontSize: '13px' }}>
                  OPTIMAL SYSTEM DETOUR:
                </span>
                <span className="mono" style={{ fontSize: '13px', color: 'var(--text-primary)' }}>
                  {simulationResult.recommended_detour_path.join('  âž”  ')}
                </span>
              </div>
            </div>
          )}

          {/* Before vs. After Comparative Table */}
          <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
            <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border-subtle)', background: 'var(--bg-secondary)' }}>
              <h3 style={{ fontSize: '14px', fontWeight: 700 }}>
                Network Impact Telemetry: Baseline vs. Simulated Redistribution
              </h3>
            </div>

            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
              <thead>
                <tr style={{ background: 'var(--bg-tertiary)', textAlign: 'left', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '10px 16px' }}>Road Corridor</th>
                  <th style={{ padding: '10px 16px' }}>Capacity</th>
                  <th style={{ padding: '10px 16px' }}>Baseline Vol</th>
                  <th style={{ padding: '10px 16px' }}>Simulated Vol</th>
                  <th style={{ padding: '10px 16px' }}>Flow Delta</th>
                  <th style={{ padding: '10px 16px' }}>Occupancy Delta</th>
                  <th style={{ padding: '10px 16px' }}>Status After</th>
                </tr>
              </thead>
              <tbody>
                {simulationResult.affected_edges.map((e) => (
                  <tr
                    key={e.road_id}
                    style={{
                      borderBottom: '1px solid var(--border-subtle)',
                      background: e.is_overloaded ? 'rgba(239, 68, 68, 0.08)' : 'transparent'
                    }}
                  >
                    <td style={{ padding: '10px 16px', fontWeight: 600 }}>{e.road_name}</td>
                    <td className="mono" style={{ padding: '10px 16px' }}>{e.capacity_vph} vph</td>
                    <td className="mono" style={{ padding: '10px 16px' }}>{e.baseline_volume_vph}</td>
                    <td className="mono" style={{ padding: '10px 16px', fontWeight: 700 }}>{e.simulated_volume_vph}</td>
                    <td className="mono" style={{ padding: '10px 16px', color: e.volume_delta_vph > 0 ? 'var(--text-secondary)' : 'inherit' }}>
                      {e.volume_delta_vph > 0 ? `+${e.volume_delta_vph}` : e.volume_delta_vph}
                    </td>
                    <td className="mono" style={{ padding: '10px 16px' }}>
                      {Math.round(e.baseline_occupancy * 100)}% âž”{' '}
                      <strong style={{ color: e.simulated_occupancy > 0.85 ? 'var(--traffic-congested)' : 'inherit' }}>
                        {Math.round(e.simulated_occupancy * 100)}%
                      </strong>
                    </td>
                    <td style={{ padding: '10px 16px' }}>
                      <span className={`badge badge-${e.status_after.toLowerCase()}`}>
                        {e.status_after}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

