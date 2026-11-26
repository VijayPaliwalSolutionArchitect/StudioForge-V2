import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchApprovals = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/v1/approvals/pending');
      setApprovals(res.data);
    } catch (err) {
      console.error('Failed to fetch approvals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApprovals();
  }, []);

  const handleResolve = async (approvalId, decision) => {
    try {
      await axios.post(`/api/v1/approvals/${approvalId}/resolve`, {
        decision,
        approver: 'creative-director@shivamitcs.com',
        approver_role: 'CREATIVE_DIRECTOR',
        review_notes: decision === 'APPROVED' ? 'Brand alignment and visual aesthetics verified' : 'Off-brand copy',
      });
      fetchApprovals();
    } catch (err) {
      alert('Approval resolution failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div style={{ padding: '0 24px 32px 24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 700, color: '#fff' }}>🔒 Two-Man Creative Rule Approval Queue</h2>
        <p style={{ fontSize: '13px', color: '#94a3b8' }}>
          Mandatory independent clearance by a Creative Director before any paid media or high-budget campaign goes live
        </p>
      </div>

      {approvals.length === 0 ? (
        <div className="glass-panel" style={{ padding: '48px', textAlign: 'center' }}>
          <div style={{ fontSize: '32px', marginBottom: '8px' }}>🟢</div>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff' }}>No Pending Approvals</h3>
          <p style={{ fontSize: '12px', color: '#64748b' }}>All creative briefs and campaigns have been reviewed or are organic.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {approvals.map((app) => (
            <div key={app.id} className="glass-card" style={{ padding: '18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                  <span className="badge badge-topsecret">PAID MEDIA REVIEW</span>
                  <span style={{ fontSize: '12px', fontFamily: 'monospace', color: '#64748b' }}>{app.id}</span>
                </div>
                <h4 style={{ fontSize: '15px', fontWeight: 700, color: '#fff' }}>Brief ID: {app.brief_id}</h4>
                <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '4px' }}>
                  Requested by: <strong>{app.requested_by}</strong> ({app.requester_role}) • Campaign: {app.campaign_id}
                </div>
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  className="btn-primary"
                  style={{ background: '#10b981', fontSize: '12px', padding: '6px 14px' }}
                  onClick={() => handleResolve(app.id, 'APPROVED')}
                >
                  Approve Publication
                </button>
                <button
                  className="btn-secondary"
                  style={{ background: 'rgba(244,63,94,0.15)', color: '#fb7185', border: '1px solid rgba(244,63,94,0.4)', fontSize: '12px', padding: '6px 14px' }}
                  onClick={() => handleResolve(app.id, 'REJECTED')}
                >
                  Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
