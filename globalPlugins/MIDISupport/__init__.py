from globalPluginHandler import GlobalPlugin as GP
from . import midi
from .midi import frequency_to_midi
import tones
import wx

class GlobalPlugin (GP):
    def __init__ (self):
        GP.__init__(self)
        midi.init()
        self.output = o = midi.Output(midi.get_default_output_id())
        self.player = midi.Player(o)
        tones.decide_beep.register(self.intone)

    def terminate (self):
        tones.decide_beep.unregister(self.intone)
        self.player.quit()
        midi.quit()

    def intone (self, hz, length, left, right, isSpeechBeepCommand):
        self.player.pan(left, right)
        self.player.play(frequency_to_midi(hz), length)
        wx.CallLater(length, self.player.tick)
        return False
