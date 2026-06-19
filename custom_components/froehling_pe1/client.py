from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import aiohttp

from .const import SUPPORTED_DOMAINS

_LOGGER = logging.getLogger(__name__)

StateCallback = Callable[[dict[str, Any]], None]


@dataclass(slots=True)
class FroehlingDeviceInfo:
    name: str
    title: str | None = None
    uptime: int | None = None


class FroehlingPe1WebClient:
    """Small client for the ESPHome web_server Server-Sent Events endpoint.

    This is intentionally read-only. It consumes the same `/events` stream that the
    ESPHome web UI uses and mirrors state events into Home Assistant entities.
    """

    def __init__(self, session: aiohttp.ClientSession, host: str, port: int, name: str) -> None:
        self.session = session
        self.host = host
        self.port = port
        self.device = FroehlingDeviceInfo(name=name)
        self.states: dict[str, dict[str, Any]] = {}
        self._callbacks: list[StateCallback] = []
        self._task: asyncio.Task[None] | None = None
        self._stopped = asyncio.Event()

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/events"

    @property
    def device_identifiers(self) -> set[tuple[str, str]]:
        return {("froehling_pe1", f"{self.host}:{self.port}")}

    async def async_validate(self) -> None:
        """Validate that the ESPHome web_server event stream is reachable."""
        timeout = aiohttp.ClientTimeout(total=10)
        async with self.session.get(self.url, timeout=timeout) as response:
            response.raise_for_status()
            deadline = asyncio.get_running_loop().time() + 8
            while asyncio.get_running_loop().time() < deadline:
                line = await response.content.readline()
                if not line:
                    break
                text = line.decode(errors="ignore").strip()
                if text.startswith("event:") or text.startswith("data:"):
                    return
        raise TimeoutError("No ESPHome event data received")

    def start(self) -> None:
        if self._task is None or self._task.done():
            self._stopped.clear()
            self._task = asyncio.create_task(self._run(), name="froehling_pe1_web_events")

    async def async_stop(self) -> None:
        self._stopped.set()
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def subscribe(self, callback: StateCallback) -> Callable[[], None]:
        self._callbacks.append(callback)
        for state in self.states.values():
            callback(state)

        def _unsubscribe() -> None:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

        return _unsubscribe

    async def _run(self) -> None:
        backoff = 2
        while not self._stopped.is_set():
            try:
                await self._stream_once()
                backoff = 2
            except asyncio.CancelledError:
                raise
            except Exception as err:  # noqa: BLE001 - keep background listener alive
                _LOGGER.warning("Fröling PE1 event stream failed: %s", err)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)

    async def _stream_once(self) -> None:
        event_name: str | None = None
        data_lines: list[str] = []
        timeout = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=None)
        async with self.session.get(self.url, timeout=timeout) as response:
            response.raise_for_status()
            async for raw_line in response.content:
                if self._stopped.is_set():
                    return
                line = raw_line.decode(errors="ignore").rstrip("\r\n")
                if not line:
                    self._handle_event(event_name, "\n".join(data_lines))
                    event_name = None
                    data_lines = []
                    continue
                if line.startswith("event:"):
                    event_name = line.removeprefix("event:").strip()
                elif line.startswith("data:"):
                    data_lines.append(line.removeprefix("data:").strip())

    def _handle_event(self, event_name: str | None, data: str) -> None:
        if not event_name or not data:
            return
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            return

        if event_name == "ping":
            if title := payload.get("title"):
                self.device.title = str(title)
            if uptime := payload.get("uptime"):
                self.device.uptime = int(uptime)
            return

        if event_name != "state" or payload.get("domain") not in SUPPORTED_DOMAINS:
            return

        key = str(payload.get("id") or payload.get("name_id") or payload.get("name"))
        self.states[key] = payload
        for callback in list(self._callbacks):
            callback(payload)
