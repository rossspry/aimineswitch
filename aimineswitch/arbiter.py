import time
from .telemetry import nvml
from .ai_adapters import ollama

STATE_MINING = "MINING"
STATE_AI = "AI"
STATE_COOLING = "COOLING"

class Arbiter:
    def __init__(self, cfg, miner):
        self.cfg = cfg
        self.miner = miner
        self.state = STATE_MINING
        self.last_switch = 0.0

    def _set_state(self, s):
        self.state = s
        self.last_switch = time.time()

    def _hysteresis_done(self) -> bool:
        return time.time() - self.last_switch >= self.cfg.hysteresis_seconds

    def step(self):
        stats = nvml.query(self.cfg.gpu_index)
        ai_active = ollama.ai_running(self.cfg.ai_process_names) and stats.util >= self.cfg.enter_ai_gpu_util
        hot = stats.temp_c >= self.cfg.max_gpu_temp_c
        mem_tight = stats.mem_free_gb < self.cfg.enter_ai_mem_free_gb

        if hot:
            if self.state != STATE_COOLING:
                self.miner.pause()
                self._set_state(STATE_COOLING)
            time.sleep(self.cfg.cooloff_seconds)
            return

        if self.state == STATE_MINING:
            if ai_active or mem_tight:
                self.miner.pause()
                self._set_state(STATE_AI)
        elif self.state == STATE_AI:
            can_exit = (not ai_active) and (stats.util <= self.cfg.exit_ai_gpu_util)
            if can_exit and self._hysteresis_done():
                self.miner.resume()
                self._set_state(STATE_MINING)
        elif self.state == STATE_COOLING:
            if not ai_active and self._hysteresis_done():
                self.miner.resume()
                self._set_state(STATE_MINING)
