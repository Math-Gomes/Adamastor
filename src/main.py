from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import kmp

def showPopup(title, message):
        pop = Popup(title = title, content = Label(text=message), size_hint = (None, None), size = (400, 400))
        pop.open()

def correctSyntax(alphabet, pattern):
    # TO DO:
    # Tratamento pra ver se o formato da entrada está correto.
    # showPopup("Error", "Incorrect syntax.\nSee example below:\nXXXXXXXXXX")

    # Tratamento pra ver se os caracteres do padrão fazem parte do alfabeto.
    for c in pattern:
        if not c in alphabet:
            showPopup("Error", "The pattern isn't at the alphabet.")
            return False
    return True

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
            kmp_ = kmp.kmp(self.pattern.text, self.alphabet.text)
            eqs, v = kmp.equations(kmp_)
            mean = kmp.mean(eqs, v, len(self.alphabet.text))

            ResultsWindow.alphabet = self.alphabet.text
            ResultsWindow.pattern = self.pattern.text
            ResultsWindow.mean = str(mean)
            ResultsWindow.equations = eqs

            sm.current = "results"
            # print(eq)
            # self.output.text = str(mean)
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
        self.alphabet_id.text = "Alphabet:  { " + ", ".join(self.alphabet) + " }"
        self.pattern_id.text = "Pattern:  " + self.pattern
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