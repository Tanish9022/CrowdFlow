import React, { useState, useEffect } from 'react';
import { networkAPI, routingAPI } from '../api/client';
import RealMapCanvas from '../components/RealMapCanvas';
import { Route, Navigation, Clock, ShieldCheck, AlertCircle } from 'lucide-react';

export default function RouteOptimizer() {
  const [network, setNetwork] = useState(null);
  const [sourceNode, setSourceNode] = useState('J_SHIVAJINAGAR');
  const [targetNode, setTargetNode] = useState('J_SWARGATE');
  const [avoidBlocked, setAvoidBlocked] = useState(true);
  const [routeResult, setRouteResult] = useState(null);
  const [activeDetourRoads, setActiveDetourRoads] = useState([]);
  const [loading, setLoading] = useState(false);

  const [errorMsg, setErrorMsg] = useState('');

  const fetchGraph = async () => {
    try {
      const res = await networkAPI.getGraph();
      setNetwork(res.data);
      setErrorMsg('');
    } catch (err) {
      console.error('Failed to load network graph', err);
      setErrorMsg(err.message || String(err));
    }
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  const handleCalculateRoute = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    try {
      const res = await routingAPI.calculateRoute(sourceNode, targetNode, avoidBlocked);
      setRouteResult(res.data);
      if (res.data.primary_route) {
        setActiveDetourRoads(res.data.primary_route.roads);
      }
    } catch (err) {
      alert('Routing query failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (network) {
      handleCalculateRoute();
    }
  }, [network, sourceNode, targetNode, avoidBlocked]);

  if (!network) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <p style={{ fontSize: '16px', fontWeight: 600 }}>Loading Pune Road Network...</p>
        {errorMsg && (
          <div style={{ marginTop: '16px' }}>
            <p style={{ color: '#ef4444', marginBottom: '12px' }}>Backend Connection Error: {errorMsg}</p>
            <button className="btn btn-primary" onClick={fetchGraph}>
              Retry Backend Connection
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="page-body">
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 700 }}>Real-World Dynamic Route & Detour Optimizer</h2>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Shortest path calculation with dynamic BPR impedance and automatic blocked road avoidance
        </p>
      </div>

      {/* Query Form */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr) auto', gap: '16px', alignItems: 'flex-end' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Origin Junction
            </label>
            <select
              value={sourceNode}
              onChange={(e) => setSourceNode(e.target.value)}
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
              {network.nodes.map((n) => (
                <option key={n.node_id} value={n.node_id}>{n.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Destination Junction
            </label>
            <select
              value={targetNode}
              onChange={(e) => setTargetNode(e.target.value)}
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
              {network.nodes.map((n) => (
                <option key={n.node_id} value={n.node_id}>{n.name}</option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', height: '38px', gap: '8px' }}>
            <input
              type="checkbox"
              id="avoidBlocked"
              checked={avoidBlocked}
              onChange={(e) => setAvoidBlocked(e.target.checked)}
              style={{ width: '16px', height: '16px', accentColor: 'var(--text-secondary)' }}
            />
            <label htmlFor="avoidBlocked" style={{ fontSize: '13px', color: 'var(--text-primary)', cursor: 'pointer' }}>
              Avoid Blocked Roads
            </label>
          </div>

          <div>
            <button onClick={handleCalculateRoute} disabled={loading} className="btn btn-primary" style={{ height: '38px' }}>
              <Navigation size={15} /> Recalculate
            </button>
          </div>
        </div>
      </div>

      {/* Grid: Map View (60%) + Route Options (40%) */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: '20px' }}>
        <div>
          <RealMapCanvas
            nodes={network.nodes}
            edges={network.edges}
            activeDetourRoads={activeDetourRoads}
          />
        </div>

        {/* Route Details Panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {routeResult && routeResult.found && routeResult.primary_route ? (
            <>
              {/* Primary Route Card */}
              <div className="card" style={{ borderLeft: '4px solid var(--text-secondary)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                  <h3 style={{ fontSize: '15px', fontWeight: 700, color: 'var(--text-secondary)' }}>
                    Primary Optimal Corridor
                  </h3>
                  <span className="badge badge-open">Recommended</span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '14px', fontSize: '12px' }}>
                  <div style={{ background: 'var(--bg-tertiary)', padding: '6px 10px', borderRadius: '4px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Distance:</span>
                    <p className="mono" style={{ fontWeight: 700 }}>
                      {(routeResult.primary_route.total_distance_meters / 1000).toFixed(2)} km
                    </p>
                  </div>
                  <div style={{ background: 'var(--bg-tertiary)', padding: '6px 10px', borderRadius: '4px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Est. Duration:</span>
                    <p className="mono" style={{ fontWeight: 700 }}>
                      {Math.round(routeResult.primary_route.total_time_seconds / 60)} mins
                    </p>
                  </div>
                </div>

                {/* Segments Timeline */}
                <h4 style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
                  Corridor Segments
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '12px' }}>
                  {routeResult.primary_route.segments.map((seg, idx) => (
                    <div
                      key={idx}
                      style={{
                        padding: '8px 10px',
                        background: 'var(--bg-secondary)',
                        borderRadius: '4px',
                        borderLeft: `2px solid ${seg.status === 'OPEN' ? '#10b981' : '#f59e0b'}`
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <strong style={{ color: 'var(--text-primary)' }}>{seg.road_name}</strong>
                        <span className="mono" style={{ color: 'var(--text-muted)', fontSize: '11px' }}>
                          {seg.distance_meters}m
                        </span>
                      </div>
                      <p style={{ color: 'var(--text-secondary)', fontSize: '11px' }}>
                        {seg.from_node} &rarr; {seg.to_node}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Alternative Detours List */}
              {routeResult.alternative_routes.length > 0 && (
                <div className="card">
                  <h4 style={{ fontSize: '13px', fontWeight: 700, marginBottom: '10px' }}>
                    Available Alternative Detours ({routeResult.alternative_routes.length})
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {routeResult.alternative_routes.map((alt, idx) => (
                      <div
                        key={idx}
                        onClick={() => setActiveDetourRoads(alt.roads)}
                        style={{
                          padding: '10px 12px',
                          background: 'var(--bg-tertiary)',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          border: '1px solid var(--border-subtle)',
                          transition: 'border-color 0.2s ease'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <span style={{ fontWeight: 600, fontSize: '12px' }}>{alt.route_name}</span>
                          <span className="mono" style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>
                            {(alt.total_distance_meters / 1000).toFixed(2)} km
                          </span>
                        </div>
                        <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                          Via: {alt.nodes.join(' \u2192 ')}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="card" style={{ textAlign: 'center', padding: '30px' }}>
              <AlertCircle size={32} color="var(--traffic-blocked)" style={{ margin: '0 auto 10px' }} />
              <h4 style={{ color: 'var(--traffic-blocked)' }}>No Feasible Detour Route</h4>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '6px' }}>
                All connecting road segments are severed or blocked. Manual traffic police intervention required.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

