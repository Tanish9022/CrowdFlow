// React core and hooks
import React, { useEffect, useRef } from 'react';
// Leaflet core library for real-world map rendering (OpenStreetMap tiles)
import L from 'leaflet';
// Import Leaflet CSS for proper tile and control styling
import 'leaflet/dist/leaflet.css';

// Real GPS coordinates for Pune road network junctions
// These are used as a fallback when the backend doesn't provide lat/lng
const PUNE_COORDS = {
  J_SHIVAJINAGAR: [18.5308, 73.8475],
  J_JM_NORTH:     [18.5285, 73.8410],
  J_FC_NORTH:     [18.5275, 73.8380],
  J_KARVE_ROAD:   [18.5195, 73.8330],
  J_DECCAN:       [18.5165, 73.8405],
  J_SWARGATE:     [18.5018, 73.8630],
  J_SB_ROAD:      [18.5100, 73.8300],
};

// Map traffic status to line colors for real-world road overlays
const STATUS_COLORS = {
  OPEN: '#16a34a',       // Green - free flow
  SLOW: '#f59e0b',       // Amber - slow traffic
  CONGESTED: '#ef4444',  // Red - congested
  BLOCKED: '#991b1b',    // Dark Red - road closed
};

/**
 * RealMapCanvas - Production-grade OpenStreetMap component
 * Renders actual Pune road network with live traffic overlays
 * Props:
 *   nodes: Array of junction objects from backend API
 *   edges: Array of road segment objects from backend API
 *   selectedRoadId: Currently selected road ID
 *   onSelectRoad: Callback when a road polyline is clicked
 */
export default function RealMapCanvas({
  nodes = [],
  edges = [],
  activeDetourRoads = [],
  selectedRoadId = null,
  onSelectRoad = () => {},
  onSelectNode = () => {}
}) {
  // Ref to hold the Leaflet map instance
  const mapRef = useRef(null);
  // Ref to the DOM container div
  const containerRef = useRef(null);
  // Ref to store all drawn layers for cleanup on re-render
  const layersRef = useRef([]);

  // Initialize the Leaflet map once on component mount
  useEffect(() => {
    if (mapRef.current) return; // Don't re-init

    // Create the Leaflet map centered on Pune, India
    const map = L.map(containerRef.current, {
      center: [18.5204, 73.8567], // Pune city center
      zoom: 14,
      zoomControl: true,
      attributionControl: true,
    });

    // Add OpenStreetMap tile layer (free, no API key required)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
    }).addTo(map);

    mapRef.current = map;

    // Cleanup on unmount
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  // Re-draw overlays whenever data changes
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    // Clear previous layers
    layersRef.current.forEach(layer => map.removeLayer(layer));
    layersRef.current = [];

    // Build node coordinate lookup from backend data or fallback to hardcoded GPS
    const nodeCoords = {};
    nodes.forEach(n => {
      if (n.latitude && n.longitude) {
        nodeCoords[n.node_id] = [n.latitude, n.longitude];
      } else if (PUNE_COORDS[n.node_id]) {
        nodeCoords[n.node_id] = PUNE_COORDS[n.node_id];
      }
    });

    // Draw road edges as colored polylines on the real map
    edges.forEach(edge => {
      const from = nodeCoords[edge.source];
      const to = nodeCoords[edge.target];
      if (!from || !to) return;

      const isBlocked = edge.current_status === 'BLOCKED';
      const isSelected = selectedRoadId === edge.road_id;
      const isDetour = activeDetourRoads.includes(edge.road_id);
      const color = STATUS_COLORS[edge.current_status] || STATUS_COLORS.OPEN;
      const weight = isSelected ? 8 : (edge.lanes ? edge.lanes * 2 + 1 : 5);

      // Draw the road polyline
      const polyline = L.polyline([from, to], {
        color: isDetour ? '#0ea5e9' : color,
        weight: weight,
        opacity: isBlocked ? 0.6 : 0.85,
        dashArray: isBlocked ? '10, 8' : (isDetour ? '8, 6' : null),
        lineCap: 'round',
      }).addTo(map);

      // Add a click handler to select this road - connects frontend click to state
      polyline.on('click', () => onSelectRoad(edge));

      // Add a tooltip showing the road name and real-time metrics
      polyline.bindTooltip(
        '<strong>' + edge.name + '</strong><br/>' +
        'Status: <b style=\"color:' + color + '\">' + edge.current_status + '</b><br/>' +
        'Vehicles: ' + edge.current_vehicle_count + ' | Speed: ' + edge.current_average_speed + ' km/h<br/>' +
        'Capacity: ' + edge.capacity_vph + ' vph',
        { sticky: true, className: 'map-tooltip' }
      );

      // Highlight effect for selected road
      if (isSelected) {
        const glow = L.polyline([from, to], {
          color: color,
          weight: weight + 6,
          opacity: 0.25,
        }).addTo(map);
        layersRef.current.push(glow);
      }

      layersRef.current.push(polyline);
    });

    // Draw junction markers as circle markers on the real map
    nodes.forEach(node => {
      const coords = nodeCoords[node.node_id];
      if (!coords) return;

      const marker = L.circleMarker(coords, {
        radius: 8,
        fillColor: '#09090b',
        color: '#ffffff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.9,
      }).addTo(map);

      marker.bindTooltip(
        '<strong>' + node.name + '</strong><br/>Type: ' + node.node_type,
        { direction: 'top', offset: [0, -10] }
      );

      marker.on('click', () => onSelectNode(node));
      layersRef.current.push(marker);
    });

    // Auto-fit the map bounds to show all nodes
    const allCoords = Object.values(nodeCoords);
    if (allCoords.length > 1) {
      map.fitBounds(allCoords, { padding: [40, 40] });
    }

  }, [nodes, edges, selectedRoadId, activeDetourRoads]);

  return React.createElement('div', {
    ref: containerRef,
    style: {
      width: '100%',
      height: '540px',
      borderRadius: '12px',
      overflow: 'hidden',
      border: '1px solid var(--border-subtle)',
      boxShadow: 'var(--shadow-card)',
    }
  });
}
