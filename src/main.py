from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config

Config.set('graphics','resizable', 0)
Config.set('kivy','window_icon','img.png')

from kivy.core.window import Window
from kivy.uix.actionbar import ActionButton
from kivy.clock import Clock
from kivy.uix.widget import Widget

from inp import parseInputAlphabet, parseInputPattern
import os
import kmp

from re import findall
# from kmp_sage import *

def showPopup(title, message):
    pop = Popup(title = title, content = Label(text = message), size_hint = (None, None), size = (400, 200))
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

class FileWindow(Screen):
    def getPath(self):
        return os.path.realpath(__file__)

    def open(self, path, filename):
        if(filename == []):
            showPopup("Error","No file selected")
            return
        try:
            with open(os.path.join(path, filename[0])) as f:
                splitInput = findall('\{.*?\}', f.read())
                if(len(splitInput) != 2):
                    showPopup("Error","Incorrect input syntax")
                    return
                InputWindow.file_content = splitInput
        except:
            showPopup("Error","There was an error reading the file")
            return
        sm.current = "input"

    def select(self, *args): 
        try: self.label.text = args[1][0] 
        except: pass

    def back(self):
        InputWindow.file_content = ["",""]
        sm.current = "input"

class InputWindow(Screen):
    alphabet = ObjectProperty(None)
    pattern = ObjectProperty(None)

    file_content = ["",""]

    def on_enter(self, *args):
        self.alphabet.text = self.file_content[0]
        self.pattern.text = self.file_content[1]

    def submitBtn(self):
        print("Alphabet:", self.alphabet.text, "Pattern:", self.pattern.text)

        if self.alphabet.text == '' or self.pattern.text == '':
            showPopup("Error", "Missing parameter(s).")
            return

        if correctSyntax(self.alphabet.text, self.pattern.text):
            # Usando kmp:
            kmp_ = kmp.kmp(self.pattern_str, self.alphabet_str)
            eqs, v = kmp.equations(kmp_)
            mean = kmp.mean(eqs, v, len(self.alphabet_str))

            # Usando kmp_sage:
            # kmp_t = kmp(self.pattern_str, self.alphabet_str)
            # eqs, symbs, z = equations_sage(kmp_t)
            # mean = mean_sage(eqs, symbs, z, kmp_t.alph_size)

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
        InputWindow.file_content = ["",""]
        sm.current = "input"

    def on_enter(self, *args):
        self.alphabet_id.text = "Alphabet: " + self.alphabet.replace(" ", "")
        self.pattern_id.text = "Pattern:  " + self.pattern.replace(" ", "")
        self.mean_id.text = "Mean:  " + self.mean

class Tooltip(Label):
    pass

class MyButton(ActionButton, Widget):
    # tooltip = Tooltip(text = 'Hello world')

    # def __init__(self, **kwargs):
    #     Window.bind(mouse_pos=self.on_mouse_pos)
    #     super(ActionButton, self).__init__(**kwargs)

    # def on_mouse_pos(self, *args):
    #     if not self.get_root_window():
    #         return
    #     pos = args[1]
    #     self.tooltip.pos = pos
    #     Clock.unschedule(self.display_tooltip) # cancel scheduled event since I moved the cursor
    #     self.close_tooltip() # close if it's opened
    #     if self.collide_point(*self.to_widget(*pos)):
    #         Clock.schedule_once(self.display_tooltip, 1)

    # def close_tooltip(self, *args):
    #     Window.remove_widget(self.tooltip)

    # def display_tooltip(self, *args):
    #     Window.add_widget(self.tooltip)
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [InputWindow(name = "input"), ResultsWindow(name = "results"), FileWindow(name = "fileWindow")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "input"

class ADAMASTOR(App):
    def build(self):
        return sm

if __name__ == "__main__":
    ADAMASTOR().run()