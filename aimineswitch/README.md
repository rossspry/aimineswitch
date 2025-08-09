# AIMineSwitch (MVP)

**Windows + NVIDIA RTX + T-Rex + Ollama** orchestrator that auto-pauses mining when local AI is active, then resumes mining when idle.

## Features
- Watches GPU utilization & VRAM and detects AI processes (`ollama` by default).
- Pauses T-Rex miner during AI work; resumes afterward.
- Configurable thresholds (`config.yaml`).
- Lightweight Python service (runs in console or as a Windows Service).

## Requirements
- Windows 10/11, NVIDIA GPU + drivers
- Python 3.11 (64-bit)
- T-Rex miner with HTTP API enabled
- Ollama for Windows (or other AI runtimes you add)

## Quick start
1. Install Python 3.11 (add to PATH).
2. Install dependencies:
   ```powershell
   cd C:\aimineswitch
   python -m pip install -r requirements.txt
   ```
3. Start T-Rex with its HTTP API:
   ```bat
   trex.exe -a kaspa -o stratum+tcp://pool.example:port -u WALLET.WORKER ^
     --api-bind-http 127.0.0.1:4067 --api-read-only=false
   ```
4. Install Ollama and pull a model:
   ```powershell
   ollama run llama3.1:8b
   ```
5. Run AIMineSwitch:
   ```powershell
   .\scripts\run_dev.ps1
   ```

When you run a prompt in Ollama, the miner will pause. After activity subsides, the miner resumes.

## Windows Service (optional)
1. Install NSSM and set `$nssm` path in `scripts\install_service.ps1`.
2. Run:
   ```powershell
   .\scripts\install_service.ps1
   ```

## Configure
Edit `config.yaml`:
- `thresholds.enter_ai_gpu_util` — GPU util% that counts as AI activity.
- `thresholds.enter_ai_mem_free_gb` — treat low free VRAM as AI priority.
- `thresholds.exit_ai_gpu_util` — drop below this to leave AI mode.
- `thresholds.hysteresis_seconds` — avoid rapid flapping.
- `thermals.max_gpu_temp_c` — safety kill/miner pause for cooling.

## Notes
- This MVP includes a **T-Rex** miner adapter. Add more in `aimineswitch/miner_adapters`.
- AI detection is by process name; add more in `config.yaml` or extend `ai_adapters`.

## Roadmap
- Tray app & web UI
- Miner adapters: lolMiner, NBMiner
- Power limit/clock adjustments on mode switch
- Partial-throttle mode when VRAM headroom allows
- Linux support (systemd)

## License
MIT (for this MVP).


## lolMiner (optional)
To use lolMiner instead of T-Rex:
1. Start lolMiner with an API port enabled, for example:
   ```bat
   lolMiner.exe --algo KASPA --pool stratum+tcp://pool:port --user WALLET.WORKER ^
     --apiport 4444 --apiallow 127.0.0.1
   ```
2. Edit `config.yaml`:
   ```yaml
   miner:
     kind: lolminer
   miner_lolminer:
     host: "127.0.0.1"
     port: 4444
     process_names: ["lolMiner.exe","lolMiner"]
   ```
> Note: If the API is unavailable, the adapter will attempt to terminate the lolMiner process as a fallback. For best results, enable the API.
