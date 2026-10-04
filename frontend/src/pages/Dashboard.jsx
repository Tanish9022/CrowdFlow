// React hooks: useState manages local component state, useEffect runs side-effects (like API calls on load)
import React, { useState, useEffect } from 'react';
// Import the centralized Axios API clients that connect to our FastAPI backend endpoints
import { networkAPI, simulationAPI } from '../api/client';
// Import the custom SVG map component used to design the visual frontend representation of the graph
import RealMapCanvas from '../components/RealMapCanvas';
// Import frontend UI icons from the Lucide library for premium design aesthetics
import { AlertTriangle, ShieldAlert, Activity, ArrowRight, PlayCircle, Video, CheckCircle2 } from 'lucide-react';

// The main Dashboard component which acts as the TOC (Traffic Operations Center) root view
export default function Dashboard() {
  // State: 'network' stores the JSON graph data fetched from the backend API
  const [network, setNetwork] = useState(null);
  // State: 'selectedRoad' tracks which edge/road the user has clicked on the frontend map
  const [selectedRoad, setSelectedRoad] = useState(null);
  // State: 'loading' controls the loading UI screen while the initial backend request is running
  const [loading, setLoading] = useState(true);
  // State: 'actionLoading' disables UI buttons while a POST/PATCH request is sent to the backend
  const [actionLoading, setActionLoading] = useState(false);
  // State: 'errorMsg' stores any HTTP/Network errors caught during backend connection
  const [errorMsg, setErrorMsg] = useState('');

  // async function to fetch the latest traffic graph from the FastAPI backend
  const fetchGraph = async () => {
    try {
      // CONNECT TO BACKEND: Calls GET /api/v1/network/graph via the Axios client
      const res = await networkAPI.getGraph();
      // Update frontend state with the JSON payload returned by the backend
      setNetwork(res.data);
      // Auto-select the first available road if nothing is currently selected
      if (!selectedRoad && res.data?.edges?.length > 0) {
        setSelectedRoad(res.data.edges[2]); // Default to JM Road
      }
      setErrorMsg(''); // Clear any previous frontend error states
    } catch (err) {
      // Log backend connection failures to the browser console
      console.error('Failed to load network graph', err);
      setErrorMsg(err.message || String(err));
    } finally {
      // Remove the frontend loading spinner regardless of success or failure
      setLoading(false);
    }
  };

  // useEffect triggers the backend API call as soon as the Dashboard component mounts on the screen
  useEffect(() => {
    fetchGraph(); // Initial backend fetch
    // Setup a polling interval: Connects to the backend every 5 seconds to sync live traffic data
    const interval = setInterval(fetchGraph, 5000);
    // Cleanup function to stop polling when the user navigates away from the Dashboard
    return () => clearInterval(interval);
  }, []);

  // async function triggered by the frontend button to manually block/open a road
  const handleToggleBlock = async () => {
    if (!selectedRoad) return;
    setActionLoading(true); // Disable frontend UI button
    // Determine the new state based on current frontend data
    const newStatus = selectedRoad.current_status === 'BLOCKED' ? 'OPEN' : 'BLOCKED';
    try {
      // CONNECT TO BACKEND: Sends PATCH /api/v1/network/roads/{roadId}/status
      await networkAPI.updateRoadStatus(selectedRoad.road_id, newStatus, 'Operator manual toggle');
      // Re-sync with backend to get updated network capacities
      await fetchGraph();
      // Update local frontend state immediately for snappy UI feel
      setSelectedRoad((prev) => ({ ...prev, current_status: newStatus }));
    } catch (err) {
      alert('Failed to update road status via Backend API');
    } finally {
      setActionLoading(false); // Re-enable frontend UI button
    }
  };

  // Frontend UI Design: Render a fallback loading screen if backend data isn't ready
  if (loading && !network) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <p style={{ fontSize: '16px', fontWeight: 600 }}>Loading Pune Traffic Network...</p>
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

  if (!network) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <p style={{ color: 'orange', marginBottom: '12px' }}>Backend data not available.</p>
        <button className="btn btn-primary" onClick={fetchGraph}>
          Reload Traffic Network
        </button>
      </div>
    );
  }

  // Derive frontend metrics directly from the backend JSON payload
  const blockedCount = network.active_disruptions.length;
  const congestedCount = network.edges.filter((e) => e.current_status === 'CONGESTED').length;

  // The main return block renders the fully loaded Dashboard UI
  return (
    <div className="page-body">
      {/* Top Telemetry KPI Bar */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', marginBottom: '32px' }}>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '24px' }}>
          <div style={{ padding: '12px', borderRadius: '8px', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>
            <Activity size={24} />
          </div>
          <div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '4px' }}>
              Network Capacity
            </p>
            <h3 className="mono" style={{ fontSize: '24px', fontWeight: 700, color: 'var(--text-primary)' }}>
              {network.total_capacity_vph.toLocaleString()} <span style={{ fontSize: '14px', fontWeight: 400, color: 'var(--text-secondary)' }}>vph</span>
            </h3>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '24px' }}>
          <div style={{ padding: '12px', borderRadius: '8px', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981' }}>
            <Activity size={24} />
          </div>
          <div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '4px' }}>
              Average Saturation
            </p>
            <h3 className="mono" style={{ fontSize: '24px', fontWeight: 700, color: '#10b981' }}>
              {Math.round(network.average_network_occupancy * 100)}%
            </h3>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '24px' }}>
          <div style={{ padding: '12px', borderRadius: '8px', background: 'rgba(245, 158, 11, 0.1)', color: 'var(--traffic-slow)' }}>
            <AlertTriangle size={24} />
          </div>
          <div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '4px' }}>
              Bottleneck Corridors
            </p>
            <h3 className="mono" style={{ fontSize: '24px', fontWeight: 700, color: congestedCount > 0 ? 'var(--traffic-congested)' : 'var(--text-primary)' }}>
              {congestedCount}
            </h3>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '24px' }}>
          <div style={{ padding: '12px', borderRadius: '8px', background: 'rgba(220, 38, 38, 0.15)', color: 'var(--traffic-blocked)' }}>
            <ShieldAlert size={24} />
          </div>
          <div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500, marginBottom: '4px' }}>
              Blocked Roads
            </p>
            <h3 className="mono" style={{ fontSize: '24px', fontWeight: 700, color: blockedCount > 0 ? 'var(--traffic-blocked)' : '#10b981' }}>
              {blockedCount}
            </h3>
          </div>
        </div>
      </div>

      {/* Main Grid: Jigsaw Map (70%) + Road Detail Drawer (30%) */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '20px', marginBottom: '20px' }}>
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h2 style={{ fontSize: '16px', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
              Live Pune Road Network
              <span className="badge badge-open">Real-Time Traffic</span>
            </h2>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Click any road on the map to inspect or simulate disruption
            </p>
          </div>

          <RealMapCanvas
            nodes={network.nodes}
            edges={network.edges}
            selectedRoadId={selectedRoad?.road_id}
            onSelectRoad={(road) => setSelectedRoad(road)}
          />
        </div>

        {/* Selected Road HUD Drawer */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <span className="mono" style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                  {selectedRoad?.road_id}
                </span>
                <h3 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text-primary)', marginTop: '2px' }}>
                  {selectedRoad?.name}
                </h3>
              </div>
              <span className={`badge badge-${selectedRoad?.current_status.toLowerCase()}`}>
                {selectedRoad?.current_status}
              </span>
            </div>
          </div>

          {/* Mini CCTV Feed Snapshot */}
          <div style={{ width: '100%', height: '140px', background: '#000', borderRadius: '6px', overflow: 'hidden', position: 'relative' }}>
            <img
              src={`/api/v1/cameras/CAM_01/snapshot`}
              alt="CCTV"
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              onError={(e) => { e.target.style.display = 'none'; }}
            />
            <div style={{ position: 'absolute', top: '8px', left: '8px', background: 'rgba(0,0,0,0.7)', padding: '2px 6px', borderRadius: '3px', fontSize: '10px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Video size={10} /> LIVE CCTV FEED
            </div>
          </div>

          {/* Road Metrics Table */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '12px' }}>
            <div style={{ background: 'var(--bg-tertiary)', padding: '8px 10px', borderRadius: '4px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Vehicles:</span>
              <p className="mono" style={{ fontWeight: 700, fontSize: '14px' }}>
                {selectedRoad?.current_vehicle_count}
              </p>
            </div>
            <div style={{ background: 'var(--bg-tertiary)', padding: '8px 10px', borderRadius: '4px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Speed:</span>
              <p className="mono" style={{ fontWeight: 700, fontSize: '14px' }}>
                {selectedRoad?.current_average_speed} km/h
              </p>
            </div>
            <div style={{ background: 'var(--bg-tertiary)', padding: '8px 10px', borderRadius: '4px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Occupancy:</span>
              <p className="mono" style={{ fontWeight: 700, fontSize: '14px' }}>
                {Math.round((selectedRoad?.current_occupancy || 0.1) * 100)}%
              </p>
            </div>
            <div style={{ background: 'var(--bg-tertiary)', padding: '8px 10px', borderRadius: '4px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Capacity:</span>
              <p className="mono" style={{ fontWeight: 700, fontSize: '14px' }}>
                {selectedRoad?.capacity_vph} vph
              </p>
            </div>
          </div>

          {/* Action Button: Disruption Toggle */}
          <div style={{ marginTop: 'auto', paddingTop: '10px' }}>
            <button
              onClick={handleToggleBlock}
              disabled={actionLoading}
              className={`btn ${selectedRoad?.current_status === 'BLOCKED' ? 'btn-primary' : 'btn-danger'}`}
              style={{ width: '100%', justifyContent: 'center' }}
            >
              {selectedRoad?.current_status === 'BLOCKED' ? (
                <>
                  <CheckCircle2 size={16} /> Reopen Road
                </>
              ) : (
                <>
                  <ShieldAlert size={16} /> Mark as Blocked
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Bottom Alert Ticker & Advisory Alert */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="card">
          <h4 style={{ fontSize: '15px', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={16} color="var(--text-primary)" />
            Real-Time Disruption Log
          </h4>
          {blockedCount > 0 ? (
            <div style={{ background: 'rgba(220, 38, 38, 0.1)', border: '1px solid var(--traffic-blocked)', padding: '10px 12px', borderRadius: '6px', fontSize: '12px' }}>
              <strong style={{ color: 'var(--traffic-blocked)' }}>CRITICAL:</strong> Road segment <code>{network.active_disruptions.join(', ')}</code> is compromised. Dynamic rerouting and traffic redistribution active.
            </div>
          ) : (
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              No critical blockages detected. All network corridors are interlocking and operational.
            </p>
          )}
        </div>

        <div className="card">
          <h4 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <PlayCircle size={16} color="#10b981" />
            Advisory Signal Plan Status
          </h4>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
            Downstream signal timing plans at <strong>Deccan Gymkhana</strong> and <strong>Swargate Terminal</strong> are dynamically synchronized with observed detour volume.
          </p>
        </div>
      </div>
    </div>
  );
}


