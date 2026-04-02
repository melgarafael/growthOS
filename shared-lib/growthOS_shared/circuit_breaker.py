"""Circuit breaker with CLOSED/OPEN/HALF_OPEN state machine."""

import inspect
import time
from enum import Enum
from typing import Any, Callable


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    """Protects external service calls with automatic failure detection and recovery.

    State machine:
      CLOSED  -- failure_threshold consecutive failures --> OPEN
      OPEN    -- after recovery_timeout seconds         --> HALF_OPEN
      HALF_OPEN -- success                              --> CLOSED
      HALF_OPEN -- failure                              --> OPEN
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 60,
        half_open_max: int = 1,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max = half_open_max

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._half_open_calls = 0

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN and self._last_failure_time is not None:
            if time.monotonic() - self._last_failure_time >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
        return self._state

    async def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        current_state = self.state

        if current_state == CircuitState.OPEN:
            raise CircuitOpenError(
                f"Circuit is OPEN. Retry after {self.recovery_timeout}s."
            )

        if current_state == CircuitState.HALF_OPEN and self._half_open_calls >= self.half_open_max:
            raise CircuitOpenError(
                "Circuit is HALF_OPEN and max probe calls reached."
            )

        try:
            if current_state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1

            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            self._on_success()
            return result

        except CircuitOpenError:
            raise
        except Exception:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        self._failure_count = 0
        self._state = CircuitState.CLOSED
        self._half_open_calls = 0

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.monotonic()
        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
