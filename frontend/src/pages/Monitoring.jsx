import React, { useState, useEffect } from 'react';
import { camerasAPI } from '../api/client';
import { Video, Activity, Users, Car, AlertOctagon } from 'lucide-react';

export default function Monitoring() {
  const [cameras, setCameras] = useState([]);
  const [telemetry, setTelemetry] = useState({});
  const [loading, setLoading] = useState(true);
  const [frameTick, setFrameTick] = useState(0);

  const fetchCameras = async () => {
    try {
      const res = await camerasAPI.getCameras();
      setCameras(res.data);
      
      // Fetch telemetry for all cameras
      const telMap = {};
      await Promise.all(
        res.data.map(async (cam) => {
          try {
            const tRes = await camerasAPI.getTelemetry(cam.camera_id);
            telMap[cam.camera_id] = tRes.data;
          } catch (e) {
            console.error(e);
          }
        })
      );
      setTelemetry(telMap);
    } catch (err) {
      console.error('Failed to load cameras', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCameras();
    const timer = setInterval(fetchCameras, 4000);
    const frameTimer = setInterval(() => {
      setFrameTick((prev) => (prev + 1) % 1000);
    }, 250); // ~4 FPS smooth animated camera grid

    return () => {
      clearInterval(timer);
      clearInterval(frameTimer);
    };
  }, []);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>Connecting to CCTV Feeds...</div>;
  }

  return (
    <div className="page-body">
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 700 }}>Live CCTV Surveillance Grid</h2>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            Real-time multi-stream vehicle detection, tracking, and traffic state intelligence
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <span className="badge badge-open">6 Streams Active</span>
          <span className="badge badge-congested">YOLOv8 + ByteTrack HUD</span>
        </div>
      </div>

      {/* 2x3 or 3x2 Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
        {cameras.map((cam) => {
          const t = telemetry[cam.camera_id] || {
            fps: 25.0,
            vehicle_count: 14,
            pedestrian_count: 2,
            average_speed_kmh: 38.0,
            traffic_state: 'NORMAL',
            road_status: 'OPEN'
          };

          const isBlocked = t.road_status === 'BLOCKED';

          return (
            <div key={cam.camera_id} className="card" style={{ padding: '0', overflow: 'hidden', border: isBlocked ? '1px solid var(--traffic-blocked)' : '1px solid var(--border-subtle)' }}>
              {/* Camera Header Bar */}
              <div style={{ padding: '10px 14px', background: 'var(--bg-secondary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-subtle)' }}>
                <div>
                  <span className="mono" style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: 600 }}>
                    {cam.camera_id}
                  </span>
                  <h4 style={{ fontSize: '13px', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {cam.name}
                  </h4>
                </div>
                <span className={`badge badge-${t.road_status.toLowerCase()}`}>
                  {t.traffic_state}
                </span>
              </div>

              {/* Video Player Canvas */}
              <div style={{ position: 'relative', width: '100%', height: '220px', background: '#000' }}>
                <img
                  src={`/api/v1/cameras/${cam.camera_id}/snapshot?t=${frameTick}`}
                  alt={cam.name}
                  style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
                />
                
                {/* HUD Overlay inside video */}
                <div style={{
                  position: 'absolute',
                  top: '10px',
                  left: '10px',
                  background: 'var(--bg-card)',
                  backdropFilter: 'blur(4px)',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '11px',
                  fontFamily: 'var(--font-mono)',
                  display: 'flex',
                  gap: '10px'
                }}>
                  <span style={{ color: 'var(--text-secondary)' }}>FPS: {t.fps}</span>
                  <span style={{ color: '#10b981' }}>Veh: {t.vehicle_count}</span>
                  <span style={{ color: '#c084fc' }}>Ped: {t.pedestrian_count}</span>
                  <span style={{ color: '#f59e0b' }}>{t.average_speed_kmh} km/h</span>
                </div>
              </div>

              {/* Telemetry Breakdown Footer */}
              <div style={{ padding: '12px 14px', background: 'var(--bg-card)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px' }}>
                <div style={{ display: 'flex', gap: '14px' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>
                    Road: <strong style={{ color: 'var(--text-primary)' }}>{cam.monitored_road_name}</strong>
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Occupancy:</span>
                  <strong className="mono" style={{ color: t.occupancy_ratio > 0.75 ? 'var(--traffic-congested)' : 'var(--text-primary)' }}>
                    {Math.round((t.occupancy_ratio || 0.2) * 100)}%
                  </strong>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

