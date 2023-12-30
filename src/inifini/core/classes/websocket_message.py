# -*- coding=utf-8 -*-
r"""
WS-Message Format

0     1      2      3      4 5 6 7   8 	    9 A B C D E F
FIN   RSV1   RSV2   RSV3   Opcode    Mask   Payload length
Extended payload length (optional 2bytes or 8bytes)
Masking key (optional 4bytes)
Payload data
"""
import os
import typing as t
from functools import cached_property


_LONG = 2 ^ (8*8)
_INT = 2 ^ (8*4)
_SHORT = 2 ^ (8*2)


# todo: move somewhere
MAX_WS_MESSAGE_SIZE: t.Optional[int] = None


class WSOPCode:
    CONTINUE = 0x0
    TEXT = 0x1
    BINARY = 0x2
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xA


class WebsocketMessage:
    r"""
    wrapper for a websocket message

    barely implemented as it is currently unused
    """
    def __init__(
            self,
            body: t.Union[str, bytes],
            *, opcode: int = None,
    ):
        if opcode is None:
            opcode = WSOPCode.BINARY if isinstance(body, bytes) else WSOPCode.TEXT
        self._opcode = opcode
        self._body = body if isinstance(body, bytes) else body.decode()

    def __repr__(self):
        return (f"{bytes((self.opcode,)).hex()} - {self.length}\n"
                f"{self.body}")

    @property
    def opcode(self) -> int:
        return self._opcode

    @property
    def length(self):
        return len(self._body)

    @property
    def body(self) -> bytes:
        return self._body

    @cached_property
    def text(self) -> str:
        return self._body.decode()

    # ----------------------------------------------------------------------- #

    @property
    def is_continue(self) -> bool:
        return self.opcode == WSOPCode.CONTINUE

    @property
    def is_text(self) -> bool:
        return self.opcode == WSOPCode.TEXT

    @property
    def is_binary(self) -> bool:
        return self.opcode == WSOPCode.BINARY

    @property
    def is_close(self) -> bool:
        return self.opcode == WSOPCode.CLOSE

    @property
    def is_ping(self) -> bool:
        return self.opcode == WSOPCode.PING

    @property
    def is_pong(self) -> bool:
        return self.opcode == WSOPCode.PONG

    # ----------------------------------------------------------------------- #

    def write_stream(self, stream: t.BinaryIO, *, masked: bool = False):
        extended_payload: bytes = b''
        length: int = self.length
        if length <= 125:
            payload_length = length
        elif length <= _SHORT:
            payload_length = 125
            extended_payload = length.to_bytes(length=2, byteorder='big', signed=False)
        elif length <= _LONG:
            payload_length = 126
            extended_payload = length.to_bytes(length=8, byteorder='big', signed=False)
        else:
            raise RuntimeError(f"body too long (> {_LONG})")

        head: bytes = int.to_bytes(
            (self.opcode << 8) | (0b1000000 if masked else 0b00000000) | payload_length,
            length=2, byteorder='big', signed=False)
        stream.write(head + extended_payload)
        body: bytes = self.body
        if masked:
            masks = t.cast(t.Tuple[int, int, int, int], tuple(_ for _ in os.urandom(4)))
            stream.write(bytes(masks))
            body = bytes((byte ^ masks[i % 4]) for i, byte in enumerate(body))
        stream.write(body)

    @classmethod
    def from_stream(cls, stream: t.BinaryIO):
        h1 = int.from_bytes(stream.read(1), byteorder='big', signed=False)
        opcode = h1 & 0b00001111
        h2 = int.from_bytes(stream.read(1), byteorder='big', signed=False)
        masked = h2 & 0b10000000
        length = h2 & 0b01111111
        if length == 126:
            length = int.from_bytes(stream.read(2), byteorder='big', signed=False)
        elif length == 127:
            length = int.from_bytes(stream.read(8), byteorder='big', signed=False)
        if MAX_WS_MESSAGE_SIZE and length > MAX_WS_MESSAGE_SIZE:
            raise RuntimeError("Websocket message is over the limit")
        masks = list(stream.read(4)) if masked else None
        body = stream.read(length)
        if masks:  # unmask the message
            body = bytes((byte ^ masks[i % 4]) for i, byte in enumerate(body))
        if opcode == WSOPCode.TEXT:
            body = body.decode()
        return cls(
            opcode=opcode,
            body=body,
        )
