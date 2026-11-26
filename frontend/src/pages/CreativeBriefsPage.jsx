import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function CreativeBriefsPage() {
  const [briefs, setBriefs] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [brands, setBrands] = useState([]);

  // Form state
  const [title, setTitle] = useState('Autonomous AI Fleet Global Launch');
  const [coreIdea, setCoreIdea] = useState('Sovereign enterprise autonomous AI systems delivering high assurance velocity without cloud leaks');
  const [selectedBrand, setSelectedBrand] = useState('');
  const [selectedCampaign, setSelectedCampaign] = useState('');
  const [aspectRatio, setAspectRatio] = useState('16:9');
  const [generating, setGenerating] = useState(false);
  const [createdResult, setCreatedResult] = useState(null);

  const fetchData = async () => {
    try {
      const [brRes, campRes, brandRes] = await Promise.all([
        axios.get('/api/v1/briefs'),
        axios.get('/api/v1/campaigns'),
        axios.get('/api/v1/brands'),
      ]);
      setBriefs(brRes.data);
      setCampaigns(campRes.data);
      setBrands(brandRes.data);
      if (brandRes.data.length > 0) setSelectedBrand(brandRes.data[0].id);
      if (campRes.data.length > 0) setSelectedCampaign(campRes.data[0].id);
    } catch (err) {
      console.error('Failed to fetch brief data:', err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateBrief = async (e) => {
    e.preventDefault();
    setGenerating(true);
    setCreatedResult(null);
    try {
      const res = await axios.post('/api/v1/briefs', {
        campaign_id: selectedCampaign,
        brand_id: selectedBrand,
        concept_title: title,
        core_idea: coreIdea,
        aspect_ratio: aspectRatio,
        target_channels: ['linkedin', 'x_twitter'],
      });
      setCreatedResult(res.data);
      fetchData();
    } catch (err) {
      alert('Brief generation rejected: ' + (err.response?.data?.detail || err.message));
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div style={{ padding: '0 24px 32px 24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#fff' }}>✨ AI Creative Brief Generator & ComfyUI Synthesizer</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8' }}>
          Real-time brand tone consistency reasoning, aspect ratio constraints, and negative prompt filtering
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Brief Creator Form */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            + Synthesize Creative Brief
          </h3>
          <form onSubmit={handleCreateBrief} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Brand Account</label>
                <select
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={selectedBrand}
                  onChange={(e) => setSelectedBrand(e.target.value)}
                >
                  {brands.map((b) => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Campaign</label>
                <select
                  className="glass-input"
                  style={{ width: '100%', fontSize: '12px' }}
                  value={selectedCampaign}
                  onChange={(e) => setSelectedCampaign(e.target.value)}
                >
                  {campaigns.map((c) => (
                    <option key={c.id} value={c.id}>{c.name} {c.is_paid_campaign ? '(Paid)' : '(Organic)'}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Concept Title</label>
              <input
                className="glass-input"
                style={{ width: '100%', fontSize: '12px' }}
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>

            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Core Creative Idea</label>
              <textarea
                className="glass-input"
                rows={3}
                style={{ width: '100%', fontSize: '12px', resize: 'vertical' }}
                value={coreIdea}
                onChange={(e) => setCoreIdea(e.target.value)}
                required
              />
            </div>

            <div>
              <label style={{ fontSize: '11px', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Aspect Ratio</label>
              <select
                className="glass-input"
                style={{ width: '100%', fontSize: '12px' }}
                value={aspectRatio}
                onChange={(e) => setAspectRatio(e.target.value)}
              >
                <option value="16:9">16:9 Landscape (YouTube / Desktop Ads)</option>
                <option value="1:1">1:1 Square (Instagram / LinkedIn Feed)</option>
                <option value="9:16">9:16 Vertical (Reels / TikTok / Shorts)</option>
              </select>
            </div>

            <button type="submit" className="btn-primary" disabled={generating} style={{ marginTop: '8px' }}>
              {generating ? 'Analyzing Brand Tone & Synthesizing...' : 'Generate Creative Brief'}
            </button>
          </form>

          {createdResult && (
            <div style={{
              marginTop: '16px',
              padding: '14px',
              borderRadius: '8px',
              background: 'rgba(168, 85, 247, 0.15)',
              border: '1px solid rgba(168, 85, 247, 0.4)'
            }}>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#c084fc', marginBottom: '4px' }}>
                ✅ Creative Brief Synthesized (Score: {createdResult.tone_result.brand_alignment_score}/100)
              </div>
              <div style={{ fontSize: '11px', color: '#cbd5e1' }}>
                Status: <strong>{createdResult.brief.status}</strong> {createdResult.requires_two_man_approval && '• Locked in Two-Man Creative Approval Queue'}
              </div>
              <div style={{
                marginTop: '8px',
                fontSize: '11px',
                fontFamily: 'monospace',
                background: 'rgba(0,0,0,0.4)',
                padding: '8px',
                borderRadius: '4px',
                color: '#38bdf8'
              }}>
                ComfyUI Prompt: {createdResult.visual_spec.positive_prompt.substring(0, 150)}...
              </div>
            </div>
          )}
        </div>

        {/* Existing Briefs List */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
            Creative Brief Pipeline ({briefs.length})
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '460px', overflowY: 'auto' }}>
            {briefs.map((b) => (
              <div key={b.id} className="glass-card" style={{ padding: '14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#fff' }}>{b.title}</h4>
                  <span className={`badge ${b.status === 'APPROVED' ? 'badge-airgap' : b.status === 'IN_REVIEW' ? 'badge' : 'badge'}`} style={{
                    background: b.status === 'APPROVED' ? 'rgba(16,185,129,0.2)' : 'rgba(245,158,11,0.2)',
                    color: b.status === 'APPROVED' ? '#34d399' : '#fbbf24'
                  }}>
                    {b.status}
                  </span>
                </div>
                <p style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>{b.core_message}</p>
                <div style={{ display: 'flex', gap: '12px', fontSize: '11px', color: '#64748b' }}>
                  <span>Ratio: <strong style={{ color: '#cbd5e1' }}>{b.aspect_ratio}</strong></span>
                  <span>Tone Score: <strong style={{ color: '#c084fc' }}>{b.brand_alignment_score}</strong></span>
                  <span>Channels: <strong style={{ color: '#38bdf8' }}>{b.target_channels?.join(', ')}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
