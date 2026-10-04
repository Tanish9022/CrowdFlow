import React from 'react';
import RealMapCanvas from './RealMapCanvas';

// Forwarding wrapper so any legacy import automatically uses RealMapCanvas (OpenStreetMap)
export default function JigsawMapCanvas(props) {
  return <RealMapCanvas {...props} />;
}
