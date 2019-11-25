from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
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

import sympy as sym
import time

from re import findall
# from kmp_sage import *

from tabulate import tabulate

def print_output(fsm, m, alphabet, eqs, g, mean):
    matrix = createTransitionsMatrix(fsm, m, alphabet)
    a = dict(parseInputAlphabet(alphabet)[0])
    f = open("./out/output.txt","a")
    string_out = ""
    string_out += "{"
    for i,lines in enumerate(matrix):
        string_out += str(i)+":"
        for letter in a:
            if letter in lines:
                string_out += str(lines.index(letter))+","
            else:
                string_out += str(0)+","
        string_out = string_out[0:-1]+'; '
    string_out = string_out[0:-2]+"}, "
    f.write(string_out)

    string_out = ""
    string_out += "{"
    for e in g:
        string_out += str(e)[2]+"="+str(g[e])+", "
    string_out = string_out[0:-2]+"}, "
    f.write(string_out)

    if mean < 1000000:
        f.write(str(float(mean)))
    else:
        f.write(str(mean))

    f.write("\n\n")

def createTransitionsMatrix(fsm, m, alphabet):
    matrix = [['-']*(m+1) for _ in range(m)]
    for c, t in fsm.items():
        for i, t_ in enumerate(t):
            matrix[i][t_] = c
    return matrix

def createStringMatrix(fsm, m, alphabet):
    matrix = createTransitionsMatrix(fsm, m, alphabet)
    s_matrix = ['         '.join(row) for row in matrix]
    labels = ['S_' + str(i) for i in range(m+1)]
    i = 0
    result = '      ' + '     '.join(labels) + '\n'
    for row in s_matrix:
        result += labels[i] + '   ' + row + '\n'
        i += 1
    return result[:-1]

def showPopup(title, message):
    pop = Popup(title = title, content = Label(text = message), size_hint = (None, None), size = (400, 200))
    pop.open()

def correctSyntax(in_alphabet, in_pattern):
    alphabet, message = parseInputAlphabet(in_alphabet)

    if alphabet != None:
        InputWindow.alphabet_str = ''.join(list(map(lambda k: k[0], alphabet)))
        InputWindow.alphabet_dict = dict(alphabet)
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
    alphabet_dict = ObjectProperty(None)

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
            begin = time.time()
            kmp_ = kmp.kmp(self.pattern_str, self.alphabet_str)
            eqs, v = kmp.equations_(kmp_, self.alphabet_dict)
            mean, g = kmp.mean_(eqs, v)
            end = time.time()
            print_output(kmp_[0], kmp_[1], self.alphabet.text, eqs, g, mean)            
            print('Elapsed time: {0:.2f} seconds'.format(end-begin))
            # Usando kmp_sage:
            # kmp_t = kmp(self.pattern_str, self.alphabet_str)
            # eqs, symbs, z = equations_sage(kmp_t)
            # mean = mean_sage(eqs, symbs, z, kmp_t.alph_size)

            ResultsWindow.alphabet = self.alphabet.text
            ResultsWindow.pattern = self.pattern.text
            ResultsWindow.mean = mean
            ResultsWindow.equations = eqs
            ResultsWindow.fsm = kmp_[0]
            ResultsWindow.g = g

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
    fsm = ObjectProperty(None)
    g = ObjectProperty(None)

    def showEquations(self):
        layout_popup = GridLayout(cols = 1, spacing=2, size_hint_y=None)
        layout_popup.bind(minimum_height=layout_popup.setter('height'))

        for eq in self.equations:
            lbl = Label(text = str(sym.pretty(eq)), size_hint_y = None, font_name="DejaVuSansMono.ttf")
            layout_popup.add_widget(lbl)

        sv = ScrollView(size_hint=(None, None), size=(675, 400))
        sv.add_widget(layout_popup)
        popup = Popup(title='Equations', content=sv, size_hint=(None, None), size = (700,500))
        popup.open()

    def showSolvedEquations(self):
        layout_popup = GridLayout(cols = 1, spacing=2, size_hint_y=None)
        layout_popup.bind(minimum_height=layout_popup.setter('height'))

        eqs = list(map(lambda x: sym.Eq(x[0],x[1]), self.g.items()))
        for eq in eqs:
            lbl = Label(text = str(sym.pretty(eq))+"\n\n\n", size_hint_y = None, font_name="DejaVuSansMono.ttf")
            layout_popup.add_widget(lbl)

        sv = ScrollView(size_hint=(None, None), size=(675, 400))
        sv.add_widget(layout_popup)
        popup = Popup(title='Solved Equations', content=sv, size_hint=(None, None), size = (700,500))
        popup.open()

    def showFSM(self):
        # message = createStringMatrix(self.fsm, len(self.pattern[1:-1]),self.alphabet)
        sz = len(self.pattern[1:-1])
        content = [["S_"+str(i)]+e for i, e in enumerate(createTransitionsMatrix(self.fsm, sz, self.alphabet))]
        table = tabulate(content, [""]+["S_"+str(i) for i in range(sz+1)], tablefmt = "fancy_grid")
        pop = Popup(title = "Finite State Machine", content = Label(text = table, font_name="DejaVuSansMono.ttf"), size_hint = (None, None), size = (700,500))
        pop.open()

    def returnToMenu(self):
        InputWindow.file_content = ["",""]
        sm.current = "input"

    def on_enter(self, *args):
        # self.alphabet_id.text = "Alphabet: " + self.alphabet
        self.pattern_id.text = "Pattern:  " + self.pattern
        if self.mean < 1000000:
            self.mean_id.text = "Mean:  " + str(float(self.mean))
        else:
            self.mean_id.text = "Mean:  " + str(self.mean)

class Tooltip(Label):
    pass

class MyButton(ActionButton, Widget):
    # tooltip = Tooltip(text = 'Hello world')

    # def __init__(self, **kwargs):
    #     Window.bind(mouse_pos=self.on_mouse_pos)
    #     super(ActionButton, self).__init__(**kwargs)

    # def on_mouse_pos(self, *args):
    #     if not self.get_sv_window():
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
    f = open("./out/output.txt","w")
    ADAMASTOR().run()
