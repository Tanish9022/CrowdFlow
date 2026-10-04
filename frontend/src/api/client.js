import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const networkAPI = {
  getGraph: () => api.get('/network/graph'),
  getRoads: () => api.get('/network/roads'),
  updateRoadStatus: (roadId, status, reason = '') =>
    api.patch(`/network/roads/${roadId}/status`, { status, reason })
};

export const routingAPI = {
  calculateRoute: (source, target, avoidBlocked = true) =>
    api.post('/routing/calculate', {
      source_node_id: source,
      target_node_id: target,
      avoid_blocked: avoidBlocked,
      calculate_alternatives: true
    })
};

export const simulationAPI = {
  runSimulation: (blockedRoadId, disruptionType = 'PROTEST', volume = null) =>
    api.post('/simulation/run', {
      blocked_road_id: blockedRoadId,
      disruption_type: disruptionType,
      diverted_volume_vph: volume
    })
};

export const signalsAPI = {
  getRecommendations: () => api.get('/signals/recommendations')
};

export const camerasAPI = {
  getCameras: () => api.get('/cameras'),
  getTelemetry: (cameraId) => api.get(`/cameras/${cameraId}/telemetry`),
  getFeedUrl: (cameraId) => `/api/v1/cameras/${cameraId}/feed`
};

export default api;
