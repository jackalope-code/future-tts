from json import JSONEncoder
from dataclasses import dataclass

@dataclass
class Segment(JSONEncoder):
    """
    Represents a transcript segment for TTS data preparation.
    Attributes:
        speaker (str): The speaker label for the segment.
        text (str): The transcript text for the segment.
        minuteStart (int): Start minute of the segment in the audio.
        secondStart (int): Start second of the segment in the audio.
        minuteStop (int): End minute of the segment in the audio.
        secondStop (int): End second of the segment in the audio.
    """
    def __init__(self, speaker: str, text: str, minuteStart: int, secondStart: int, minuteStop: int, secondStop: int):
        """
        Initialize a Segment instance.
        Args:
            speaker (str): Speaker label.
            text (str): Transcript text.
            minuteStart (int): Start minute.
            secondStart (int): Start second.
            minuteStop (int): End minute.
            secondStop (int): End second.
        """
        self.speaker = speaker
        self.text = text
        self.minuteStart = minuteStart
        self.secondStart = secondStart
        self.minuteStop = minuteStop
        self.secondStop = secondStop
    
    def __repr__(self) -> str:
        return f'Segment(\'{self.speaker}\', \'{self.text}\', {self.minuteStart}:{self.secondStart}-{self.minuteStop}:{self.secondStop})'
    # Optionally, override default for JSON serialization
    # def default(self, obj):
    #     return obj.__dict__