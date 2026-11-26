# 🎨 StudioForge V2 — Autonomous AI Brand & Media Factory

[![CI](https://github.com/VijayPaliwalSolutionArchitect/StudioForge-V2/actions/workflows/ci.yml/badge.svg)](https://github.com/VijayPaliwalSolutionArchitect/StudioForge-V2/actions/workflows/ci.yml)
[![Tests: 41 Passed](https://img.shields.io/badge/tests-41%20passed-brightgreen.svg)](#)
[![Evals: 4/4 Passed](https://img.shields.io/badge/evals-4%2F4%20passed-brightgreen.svg)](#)
[![ComfyUI Ready](https://img.shields.io/badge/ComfyUI-Flux%2FSDXL%20Synthesizer-purple.svg)](#)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](#)
[![React 18](https://img.shields.io/badge/react-18.3-61dafb.svg)](#)

> **Enterprise AI Brand & Media Factory:** Full creative operations platform managing brand guidelines, forbidden word scanners, ComfyUI latent diffusion prompt synthesis (16:9, 1:1, 9:16), Two-Man Rule Creative Director approvals on paid ads, and multi-channel social publishing.

---

## 🚀 Quick Start

### 1. Backend Service (Port :8097)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8097 --reload
```

### 2. Frontend Workstation (Port :5179)
```bash
cd frontend
npm install
npm run dev
```

### 3. Run Automated 41-Test Suite & Hard Evals Gate
```bash
cd backend
python -m pytest tests/ -v
python ../evals/run_evals.py
```
