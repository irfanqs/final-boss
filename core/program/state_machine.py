from enum import Enum, auto
import time

class State(Enum):
    IDLE = auto();         DETECTING = auto()
    VERIFY_POLLEN = auto(); SPRAYING  = auto()
    COOLDOWN = auto();     INSUFFICIENT = auto()
    ERROR = auto()

class PollinationStateMachine:
    def __init__(self, cfg):
        self.cfg         = cfg
        self.state       = State.IDLE
        self.last_t      = time.time()
        self.consecutive = 0
        self.spray_count = 0

    def _transit(self, new: State):
        self.state  = new
        self.last_t = time.time()

    def elapsed(self): return time.time() - self.last_t

    def update(self, *, detected, confidence=0.0, volume_ml=0.0):
        self.consecutive = self.consecutive + 1 if detected else 0
        action = {"spray": False, "open_valve": False, "blower_duty": 0.0}

        if self.state == State.IDLE:
            if (self.consecutive >= self.cfg.MIN_DETECTION_FRAMES
                    and confidence >= self.cfg.CONF_THRESHOLD):
                self._transit(State.DETECTING)

        elif self.state == State.DETECTING:
            self._transit(State.VERIFY_POLLEN)

        elif self.state == State.VERIFY_POLLEN:
            if volume_ml * 1000 >= self.cfg.VOLUME_MIN_THRESHOLD_MM3:
                self._transit(State.SPRAYING)
            else:
                self._transit(State.INSUFFICIENT)

        elif self.state == State.SPRAYING:
            if self.elapsed() < self.cfg.SPRAY_DURATION_SEC:
                action.update({"spray": True, "open_valve": True,
                               "blower_duty": self.cfg.BLOWER_DUTY_DEFAULT})
            else:
                self.spray_count += 1
                self._transit(State.COOLDOWN)

        elif self.state == State.COOLDOWN:
            if self.elapsed() >= self.cfg.COOLDOWN_AFTER_SPRAY_SEC:
                self._transit(State.IDLE)

        elif self.state in (State.INSUFFICIENT, State.ERROR):
            if self.elapsed() > 5.0:
                self._transit(State.IDLE)

        return action
