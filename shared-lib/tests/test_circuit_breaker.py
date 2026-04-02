"""Tests for CircuitBreaker — state machine and async call protection."""

import time
from unittest.mock import patch

import pytest

from growthOS_shared.circuit_breaker import (
    CircuitBreaker,
    CircuitOpenError,
    CircuitState,
)


@pytest.fixture
def breaker() -> CircuitBreaker:
    return CircuitBreaker(failure_threshold=3, recovery_timeout=2, half_open_max=1)


class TestInitialState:
    def test_starts_closed(self, breaker: CircuitBreaker) -> None:
        assert breaker.state == CircuitState.CLOSED

    def test_defaults(self) -> None:
        cb = CircuitBreaker()
        assert cb.failure_threshold == 3
        assert cb.recovery_timeout == 60
        assert cb.half_open_max == 1


class TestClosedToOpen:
    @pytest.mark.asyncio
    async def test_opens_after_threshold_failures(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        for _ in range(3):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        assert breaker.state == CircuitState.OPEN

    @pytest.mark.asyncio
    async def test_stays_closed_below_threshold(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        for _ in range(2):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        assert breaker.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_success_resets_failure_count(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        async def succeed():
            return "ok"

        # 2 failures, then success, then 2 more failures — should not open
        for _ in range(2):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)
        await breaker.call(succeed)
        for _ in range(2):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        assert breaker.state == CircuitState.CLOSED


class TestOpenState:
    @pytest.mark.asyncio
    async def test_open_rejects_calls(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        for _ in range(3):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        with pytest.raises(CircuitOpenError):
            await breaker.call(fail)


class TestHalfOpen:
    @pytest.mark.asyncio
    async def test_transitions_to_half_open_after_timeout(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        for _ in range(3):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        assert breaker.state == CircuitState.OPEN

        # Simulate time passing beyond recovery_timeout
        with patch("growthOS_shared.circuit_breaker.time") as mock_time:
            mock_time.monotonic.return_value = time.monotonic() + 3
            assert breaker.state == CircuitState.HALF_OPEN

    @pytest.mark.asyncio
    async def test_half_open_success_closes(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        async def succeed():
            return "ok"

        for _ in range(3):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        # Move to HALF_OPEN
        with patch("growthOS_shared.circuit_breaker.time") as mock_time:
            mock_time.monotonic.return_value = time.monotonic() + 3
            result = await breaker.call(succeed)

        assert result == "ok"
        assert breaker.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_half_open_failure_reopens(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        for _ in range(3):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        with patch("growthOS_shared.circuit_breaker.time") as mock_time:
            mock_time.monotonic.return_value = time.monotonic() + 3
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        assert breaker.state == CircuitState.OPEN

    @pytest.mark.asyncio
    async def test_half_open_max_calls(self, breaker: CircuitBreaker) -> None:
        async def fail():
            raise RuntimeError("boom")

        async def succeed():
            return "ok"

        for _ in range(3):
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        # Move to HALF_OPEN, consume the 1 allowed probe
        with patch("growthOS_shared.circuit_breaker.time") as mock_time:
            mock_time.monotonic.return_value = time.monotonic() + 3
            with pytest.raises(RuntimeError):
                await breaker.call(fail)

        # Now it should be OPEN again, not allowing more calls
        assert breaker.state == CircuitState.OPEN


class TestSyncFunction:
    @pytest.mark.asyncio
    async def test_sync_callable(self, breaker: CircuitBreaker) -> None:
        def sync_add(a: int, b: int) -> int:
            return a + b

        result = await breaker.call(sync_add, 2, 3)
        assert result == 5
