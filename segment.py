from json import JSONEncoder
from dataclasses import dataclass

@dataclass
class Segment(JSONEncoder):
    def __init__(self, speaker, text, minuteStart, secondStart, minuteStop, secondStop):
        self.speaker = speaker
        self.text = text
        self.minuteStart = minuteStart
        self.secondStart = secondStart
        self.minuteStop = minuteStop
        self.secondStop = secondStop
     
    def __repr__(self):
        return f'Segment(\'{self.speaker}\', \'{self.text}\', {self.minuteStart}:{self.secondStart}-{self.minuteStop}:{self.secondStop})'
    """
    def default(self, obj):
        return obj.__dict__
    """