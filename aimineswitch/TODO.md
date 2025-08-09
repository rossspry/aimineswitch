# TODO: Tray App & Web UI

## Tray App (Windows)
- Framework: Tauri or Electron (Tauri preferred: smaller footprint).
- Features:
  - Show current state (MINING / AI / COOLING)
  - Toggle: Force AI / Force Mining / Auto
  - Temps, GPU util, VRAM free, miner status
  - Start/stop service (interface with Windows Service)

### Backend control API
- Expose a small HTTP server in Python (FastAPI) with endpoints:
  - `GET /status` -> state, temps, gpu util, mem, miner alive
  - `POST /mode` -> {"mode": "auto" | "ai" | "mining"}
  - `POST /restart` -> restart arbiter/service

## Web UI (local)
- Minimal FastAPI + Jinja2 or static HTML+JS hitting /status
- Future: auth token for remote access

## Power/Clocks (optional)
- Integrate NVML power limit & fan control on mode switch
- Add config flags to enable/disable

## Miner Adapters
- Add lolMiner, NBMiner
- Abstract pause/resume/throttle interface
