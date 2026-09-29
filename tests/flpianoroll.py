"""Minimal mock of the FL Studio flpianoroll module - for tests outside FL."""


class Note:
    def __init__(self):
        self.number = 60
        self.time = 0
        self.length = 96
        self.velocity = 0.8
        self.pan = 0.5
        self.release = 0.5
        self.color = 0
        self.fcut = 0.5
        self.fres = 0.5
        self.pitchofs = 0
        self.slide = False
        self.porta = False
        self.muted = False
        self.group = 0
        self.selected = False


class Score:
    PPQ = 96

    def __init__(self):
        self.notes = []

    @property
    def noteCount(self):
        return len(self.notes)

    def getNote(self, i):
        return self.notes[i]

    def addNote(self, n):
        self.notes.append(n)

    def deleteNote(self, i):
        del self.notes[i]

    def clear(self):
        self.notes = []


class ScriptDialog:
    def __init__(self, title, desc):
        self.values = {}

    def AddInputKnob(self, name, value, lo, hi):
        self.values[name] = value

    def AddInputKnobInt(self, name, value, lo, hi):
        self.values[name] = value

    def AddInputCombo(self, name, options, value):
        self.values[name] = value

    def AddInputCheckbox(self, name, value):
        self.values[name] = value

    def GetInputValue(self, name):
        return self.values[name]


score = Score()
