# -*- coding=utf-8 -*-
r"""
def endpoint(websocket: WebsocketHandler):
    @websocket.on_text()
    def on_text(text: str):
        logging.info(f"Received: {text!r}")

    websocket.loop()

def endpoint(websocket: WebsocketHandler):
    while not websocket.closed:
        msg = websocket.receive_json()
        logging.info(f"Received Event: {msg['event']!r}")
        response = EVENT_HANDLER[msg['event']](msg)
        websocket.send_json(response)
"""
import typing as t
from ..._libs import json
from ...status import WSStatus
from .websocket_message import WebsocketMessage, WSOPCode


_CB_TEXT = t.Callable[[str], None]  # (text) -> None
_CB_BINARY = t.Callable[[bytes], None]  # (binary) -> None
_CB_MESSAGE = t.Callable[[t.AnyStr], None]  # (message) -> None
_CB_CLOSE = t.Callable[[str], None]  # (reason) -> None
_CB_CONTINUE = t.Callable[[], None]  # () -> None


class WebsocketHandler:
    def __init__(self, *, rfile: t.BinaryIO, wfile: t.BinaryIO):
        self._rfile = rfile
        self._wfile = wfile
        self._closed: bool = False
        self._on_text: t.List[_CB_TEXT] = []
        self._on_binary: t.List[_CB_BINARY] = []
        self._on_message: t.List[_CB_MESSAGE] = []
        self._on_close: t.List[_CB_CLOSE] = []
        self._on_continue: t.List[_CB_CONTINUE] = []

    @property
    def closed(self):
        return self._closed

    def send(self, data: t.AnyStr, *, opcode: WSOPCode = None) -> None:
        if self._closed:
            raise RuntimeError("Connection was already closed")
        message = WebsocketMessage(body=data, opcode=opcode)
        self._wfile.write(message.to_bytes())  # performance-reason with flushing
        # message.write_stream(stream=self._wfile)  # bit slower as it writes parts at a time

    def send_json(self, obj: t.Any) -> None:
        dumped = json.dumps(obj)
        self.send(dumped)

    def receive(self) -> WebsocketMessage:
        if self._closed:
            raise RuntimeError("Connection was already closed")
        return WebsocketMessage.from_stream(stream=self._rfile)

    def receive_json(self) -> t.Any:
        message = self.receive()
        if not message.is_text or message.is_binary:
            raise RuntimeError("Can't load received message to json")
        # todo: this function is to be used by the user and should be able to respond to close or ping
        # todo: JsonDecodeError raises custom error class which sends WSStatus.CLOSE_PROTOCOL_ERROR or so
        return json.loads(message.body)

    def close(self, reason: t.Union[str, int, WSStatus] = WSStatus.CLOSE_NORMAL, *, call_self: bool = False):
        if self._closed:
            return
            # raise RuntimeError("Connection was already closed")
        reason = reason if isinstance(reason, str) else WSStatus(reason).phrase
        self._wfile.write(WebsocketMessage(reason, opcode=WSOPCode.CLOSE).to_bytes())
        self._closed = True
        if call_self:
            for cb in self._on_close:
                cb(reason)

    def close_fatally(self):
        self._wfile.write(WebsocketMessage(WSStatus.SERVER_ERROR.phrase, opcode=WSOPCode.CLOSE).to_bytes())
        self._closed = True

    def _send_pong(self) -> None:
        if self._closed:
            raise RuntimeError("Connection was already closed")
        message = WebsocketMessage(b'', opcode=WSOPCode.PONG)
        self._wfile.write(message.to_bytes())  # todo: cache these bytes!?

    def loop(self, *, close_on_exception: bool = True):
        try:
            while not self._closed:
                message = self.receive()
                if message.is_text:
                    for cb in self._on_text:
                        cb(message.text)
                    for cb in self._on_message:
                        cb(message.text)
                elif message.is_binary:
                    for cb in self._on_binary:
                        cb(message.body)
                    for cb in self._on_message:
                        cb(message.body)
                elif message.is_close:
                    self._closed = True
                    for cb in self._on_close:
                        cb(message.text)
                elif message.is_continue:
                    for cb in self._on_continue:
                        cb()
                elif message.is_ping:
                    self._send_pong()
        except Exception:
            if close_on_exception:
                self.close_fatally()
            raise

    @t.overload
    def on_text(self) -> t.Callable[[_CB_TEXT], _CB_TEXT]: ...
    @t.overload
    def on_text(self, fn: _CB_TEXT) -> _CB_TEXT: ...

    def on_text(self, _fn=None):
        def decorator(fn):
            self._on_text.append(fn)
            return fn
        return decorator(_fn) if _fn is not None else decorator

    @t.overload
    def on_binary(self) -> t.Callable[[_CB_BINARY], _CB_BINARY]: ...
    @t.overload
    def on_binary(self, fn: _CB_BINARY) -> _CB_BINARY: ...

    def on_binary(self, _fn=None):
        def decorator(fn):
            self._on_binary.append(fn)
            return fn
        return decorator(_fn) if _fn is not None else decorator

    @t.overload
    def on_message(self) -> t.Callable[[_CB_MESSAGE], _CB_MESSAGE]: ...
    @t.overload
    def on_message(self, fn: _CB_MESSAGE) -> _CB_MESSAGE: ...

    def on_message(self, _fn=None):
        def decorator(fn):
            self._on_message.append(fn)
            return fn
        return decorator(_fn) if _fn is not None else decorator

    @t.overload
    def on_close(self) -> t.Callable[[_CB_CLOSE], _CB_CLOSE]: ...
    @t.overload
    def on_close(self, fn: _CB_CLOSE) -> _CB_CLOSE: ...

    def on_close(self, _fn=None):
        def decorator(fn):
            self._on_close.append(fn)
            return fn
        return decorator(_fn) if _fn is not None else decorator

    @t.overload
    def on_continue(self) -> t.Callable[[_CB_CONTINUE], _CB_CONTINUE]: ...
    @t.overload
    def on_continue(self, fn: _CB_CONTINUE) -> _CB_CONTINUE: ...

    def on_continue(self, _fn=None):
        def decorator(fn):
            self._on_continue.append(fn)
            return fn
        return decorator(_fn) if _fn is not None else decorator
