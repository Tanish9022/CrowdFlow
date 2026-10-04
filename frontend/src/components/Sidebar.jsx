// React library for building user interfaces
import React from 'react';
// NavLink is used for client-side routing between pages without reloading
import { NavLink } from 'react-router-dom';
// Lucide-react provides scalable SVG icons used throughout the UI design
import { LayoutDashboard, Video, Map, Route, PlayCircle, Sliders, AlertOctagon } from 'lucide-react';

// The Sidebar component constructs the primary navigation menu
export default function Sidebar() {
  // navItems array defines the menu structure and routing paths
  const navItems = [
    { to: '/', label: 'TOC Dashboard', icon: LayoutDashboard },
    { to: '/monitoring', label: 'Live CCTV Monitoring', icon: Video },
    { to: '/map', label: 'Live Pune Road Map', icon: Map },
    { to: '/routing', label: 'Route Optimizer', icon: Route },
    { to: '/simulator', label: 'What-If Simulator', icon: PlayCircle },
    { to: '/signals', label: 'Signal Advisory', icon: Sliders },
  ];

  // The return block renders the frontend JSX
  return (
    // <aside> acts as the semantic HTML container for the sidebar, styled by the "sidebar" CSS class
    <aside className="sidebar">
      {/* Header section of the sidebar containing the application logo */}
      <div style={{ padding: '32px 24px', borderBottom: '1px solid var(--border-subtle)' }}>
        {/* Flexbox is used to align the logo icon and text horizontally */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Logo container utilizing CSS variables (--accent-primary) to maintain consistent frontend design */}
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            background: 'var(--accent-primary)', // Connects to index.css minimalist theme
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 800,
            fontSize: '18px',
            color: 'var(--text-inverse)',
            boxShadow: '0 4px 12px var(--shadow-card)' // Applies the premium drop-shadow
          }}>
            CF
          </div>
          {/* App title text container */}
          <div>
            <h1 style={{ fontSize: '18px', fontWeight: 700, letterSpacing: '0.5px', color: 'var(--text-primary)', marginBottom: '2px' }}>
              CROWD FLOW
            </h1>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', fontWeight: 500 }}>
              AI Traffic & Jigsaw Route
            </p>
          </div>
        </div>
      </div>

      {/* Navigation menu wrapper pushing items into a flexible column layout */}
      <nav style={{ padding: '24px 12px', flex: 1, display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {/* Iterating over navItems to dynamically generate navigation links */}
        {navItems.map((item) => {
          // Destructuring the specific icon component to render it dynamically
          const Icon = item.icon;
          return (
            // NavLink connects to the React Router to change views instantly
            <NavLink
              key={item.to} // Unique key required by React for lists
              to={item.to} // The URL path to navigate to
              // Dynamically appends the 'active' CSS class when the route matches the current URL
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              {/* Renders the Lucide icon at 18px size */}
              <Icon size={18} />
              {/* Renders the text label for the navigation item */}
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Production-ready Footer Section */}
      <div style={{ padding: '24px', borderTop: '1px solid var(--border-subtle)', fontSize: '12px', color: 'var(--text-muted)' }}>
        {/* System version indicator */}
        <p style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>System v2.1.0 (Production)</p>
        <p style={{ marginTop: '4px' }}>All systems operational.</p>
      </div>
    </aside>
  );
}
