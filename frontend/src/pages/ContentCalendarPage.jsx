import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function ContentCalendarPage() {
  const [calendar, setCalendar] = useState([]);
  const [briefs, setBriefs] = useState([]);
  const [selectedBrief, setSelectedBrief] = useState('');
  const [channel, setChannel] = useState('LINKEDIN');
  const [scheduledFor, setScheduledFor] = useState('2026-12-01T10:00:00Z');
  const [copyText, setCopyText] = useState('Autonomous enterprise AI that operates without data leaks.');

  const fetchData = async () => {
    try {
      const [calRes, brRes] = await Promise.all([
        axios.get('/api/v1/calendar'),
        axios.get('/api/v1/briefs'),
      ]);
      setCalendar(calRes.data);
      setBriefs(brRes.data);
      if (brRes.data.length > 0) setSelectedBrief(brRes.data[0].id);
    } catch (err) {
      console.error('Failed to fetch calendar:', err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSchedule = async (e) => {
    e.preventDefault();
    if (!selectedBrief) return;
    try {
      await axios.post('/api/v1/calendar', {
        brief_id: selectedBrief,
        brand_id: 'brand-shivam-itcs',
        channel,
        scheduled_for: scheduledFor,
        copy_text: copyText,
      });
      fetchData();
    } catch (err) {
      alert('Failed to schedule item: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div style={{ padding: '0 24px 32px 24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#fff' }}>📅 Multi-Channel Content Calendar</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8' }}>
          Schedule and synchronize brand-approved content across LinkedIn, X/Twitter, Instagram, and YouTube
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Schedule Form */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            + Schedule Publishing Event
          </h3>
          <form onSubmit={handleSchedule} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Approved Brief</label>
              <select
                className="glass-input"
                style={{ width: '100%', fontSize: '12px' }}
                value={selectedBrief}
                onChange={(e) => setSelectedBrief(e.target.value)}
              >
                {briefs.map((b) => (
                  <option key={b.id} value={b.id}>{b.title} ({b.status})</option>
                ))}
              </select>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Channel</label>
                <select
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={channel}
                  onChange={(e) => setChannel(e.target.value)}
                >
                  <option value="LINKEDIN">LinkedIn</option>
                  <option value="TWITTER">X / Twitter</option>
                  <option value="INSTAGRAM">Instagram</option>
                  <option value="YOUTUBE">YouTube Shorts</option>
                </select>
              </div>

              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Publish Timestamp</label>
                <input
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={scheduledFor}
                  onChange={(e) => setScheduledFor(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Post Copy</label>
              <textarea
                className="glass-input"
                rows={3}
                style={{ width: '100%', fontSize: '12px', resize: 'vertical' }}
                value={copyText}
                onChange={(e) => setCopyText(e.target.value)}
              />
            </div>

            <button type="submit" className="btn-primary" style={{ marginTop: '8px' }}>
              Schedule Publication
            </button>
          </form>
        </div>

        {/* Calendar Queue */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            Scheduled Events ({calendar.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '460px', overflowY: 'auto' }}>
            {calendar.map((item) => (
              <div key={item.id} className="glass-card" style={{ padding: '14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <span className="badge" style={{ background: 'rgba(59,130,246,0.2)', color: '#60a5fa' }}>
                    {item.channel}
                  </span>
                  <span className="badge badge-airgap">{item.status}</span>
                </div>
                <p style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '6px' }}>{item.copy_text}</p>
                <div style={{ fontSize: '10px', color: '#64748b', marginTop: '6px' }}>
                  Scheduled: {item.scheduled_for}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
