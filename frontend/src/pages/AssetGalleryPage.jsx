import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function AssetGalleryPage() {
  const [assets, setAssets] = useState([]);
  const [briefs, setBriefs] = useState([]);
  const [selectedBrief, setSelectedBrief] = useState('');
  const [generating, setGenerating] = useState(false);

  const fetchData = async () => {
    try {
      const [assRes, brRes] = await Promise.all([
        axios.get('/api/v1/assets'),
        axios.get('/api/v1/briefs'),
      ]);
      setAssets(assRes.data);
      setBriefs(brRes.data);
      if (brRes.data.length > 0) setSelectedBrief(brRes.data[0].id);
    } catch (err) {
      console.error('Failed to fetch assets:', err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleGenerate = async () => {
    if (!selectedBrief || generating) return;
    setGenerating(true);
    try {
      await axios.post('/api/v1/assets/generate', {
        brief_id: selectedBrief,
        asset_type: 'IMAGE',
        model: 'flux-1-schnell',
      });
      fetchData();
    } catch (err) {
      alert('Asset generation failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div style={{ padding: '0 24px 32px 24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#fff' }}>🖼️ ComfyUI Generated Media Asset Gallery</h2>
          <p style={{ fontSize: '13px', color: '#94a3b8' }}>
            Diffusion assets rendered with headless ComfyUI, seed reproducibility, and brand color grading
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <select
            className="glass-input"
            value={selectedBrief}
            onChange={(e) => setSelectedBrief(e.target.value)}
            style={{ fontSize: '12px' }}
          >
            {briefs.map((b) => (
              <option key={b.id} value={b.id}>{b.title} ({b.aspect_ratio})</option>
            ))}
          </select>
          <button className="btn-primary" onClick={handleGenerate} disabled={generating}>
            {generating ? 'Rendering via ComfyUI...' : '+ Render Asset'}
          </button>
        </div>
      </div>

      {/* Asset Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
        {assets.map((a) => (
          <div key={a.id} className="glass-card" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{
              height: '160px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, rgba(168,85,247,0.2), rgba(6,182,212,0.2))',
              border: '1px solid rgba(255,255,255,0.06)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px'
            }}>
              🎨
            </div>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="badge badge-airgap">FLUX SCHNELL</span>
                <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#38bdf8' }}>{a.resolution}</span>
              </div>
              <div style={{ fontSize: '11px', fontFamily: 'monospace', color: '#94a3b8', marginTop: '6px' }}>
                ComfyUI ID: {a.comfyui_prompt_id}
              </div>
              <div style={{ fontSize: '11px', color: '#64748b' }}>
                Seed: {a.comfyui_seed || 'Deterministic'}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
