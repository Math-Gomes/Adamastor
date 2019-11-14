from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config

Config.set('kivy','window_icon','img.png')

from inp import parseInputAlphabet, parseInputPattern

import kmp

def showPopup(title, message):
    pop = Popup(title = title, content = Label(text = message), size_hint = (None, None), size = (400, 400))
    pop.open()

def correctSyntax(in_alphabet, in_pattern):
    alphabet, message = parseInputAlphabet(in_alphabet)

    if alphabet != None:
        InputWindow.alphabet_str = ''.join(list(map(lambda k: k[0], alphabet)))
        pattern, message = parseInputPattern(in_pattern, InputWindow.alphabet_str)
        if pattern != None:
            InputWindow.pattern_str = pattern
            return True

    showPopup("Error", message)

    return False

class InputWindow(Screen):
    alphabet = ObjectProperty(None)
    pattern = ObjectProperty(None)
    current = ""

    def submitBtn(self):
        print("Alphabet:", self.alphabet.text, "Pattern:", self.pattern.text)

        if self.alphabet.text == '' or self.pattern.text == '':
            showPopup("Error", "Missing parameter(s).")
            return

        if correctSyntax(self.alphabet.text, self.pattern.text):
            kmp_ = kmp.kmp(self.pattern_str, self.alphabet_str)
            eqs, v = kmp.equations(kmp_)
            mean = kmp.mean(eqs, v, len(self.alphabet_str))

            ResultsWindow.alphabet = self.alphabet.text
            ResultsWindow.pattern = self.pattern.text
            ResultsWindow.mean = str(mean)
            ResultsWindow.equations = eqs

            sm.current = "results"
            self.reset()

    def reset(self):
        self.alphabet.text = ""
        self.pattern.text = ""

class ResultsWindow(Screen):
    alphabet = ObjectProperty(None)
    pattern = ObjectProperty(None)
    mean = ObjectProperty(None)
    equations = ObjectProperty(None)

    def returnToMenu(self):
        sm.current = "input"

    def on_enter(self, *args):
        self.alphabet_id.text = "Alphabet: " + self.alphabet.replace(" ", "")
        self.pattern_id.text = "Pattern:  " + self.pattern.replace(" ", "")
        self.mean_id.text = "Mean:  " + self.mean


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [InputWindow(name = "input"), ResultsWindow(name = "results")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "input"

class ADAMASTOR(App):
    def build(self):
        return sm

if __name__ == "__main__":
    ADAMASTOR().run()