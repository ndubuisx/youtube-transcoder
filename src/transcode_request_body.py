from typing import List

class Input:
    source: str

    def __init__(self, source: str) -> None:
        self.source = source

class Audio:
    codec: str
    bitrate_kb: int
    channels: int

    def __init__(self, codec: str, bitrate_kb: int, channels: int) -> None:
        self.codec = codec
        self.bitrate_kb = bitrate_kb
        self.channels = channels

class Video:
    codec: str
    width: int
    height: int
    frame_rate: int
    bitrate_mode: str
    bitrate_kb: int

    def __init__(self, codec: str, width: int, height: int, frame_rate: int, bitrate_mode: str, bitrate_kb: int) -> None:
        self.codec = codec
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.bitrate_mode = bitrate_mode
        self.bitrate_kb = bitrate_kb

class Output:
    destination: str
    kind: str
    audio: Audio
    video: Video

    def __init__(self, destination: str, kind: str, audio: Audio, video: Video) -> None:
        self.destination = destination
        self.kind = kind
        self.audio = audio
        self.video = video

class TranscodeRequestBody:
    inputs: List[Input]
    outputs: List[Output]

    def __init__(self, inputs: List[Input], outputs: List[Output]) -> None:
        self.inputs = inputs
        self.outputs = outputs
