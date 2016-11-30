import Tkinter as tk, ttk, tkFont
#import tkinter.ttk as ttk
#import tkinter.font as tkFont
import os, sys
import collections
import webbrowser

from countdown import Solver


class App():
    def __init__(self):
        app_name = 'Countdown'

        self.solver = Solver()

        self.root = root = tk.Tk()
        root.title(app_name)
        root.geometry('345x315')
        root.minsize(345, 315)
        self._layout(root)
        root.iconbitmap(self._resource_path('icon.ico'))

        root.after_idle(self._load_words)

    @property
    def mainloop(self):
        return self.root.mainloop

    def _resource_path(self, relative):
        if getattr(sys, 'frozen', False):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)

        return os.path.join(basedir, relative)

    def _load_words(self):
        self.root.config(cursor='wait')
        self._set_all_states(tk.DISABLED)
        self.root.update()

        self.solver.load_words(self._resource_path('words.txt'))

        self.root.config(cursor='')
        self._set_all_states(tk.NORMAL)

    def _set_all_states(self, state, widget=None):
        if widget is None:
            widget = self.root

        if 'state' in widget.config():
            widget.configure(state=state)
            return

        for child in widget.winfo_children():
            self._set_all_states(state, child)

    def _layout(self, root):
        layoutFont = tkFont.Font(size=18, weight='bold')
        resultsFont = tkFont.Font(size=12)

        f = ttk.Frame(root)
        f.pack(side=tk.TOP, fill=tk.X)

        l = ttk.Label(f, text='Letters:', font=layoutFont)
        l.pack(side=tk.TOP, anchor=tk.W)

        sv = tk.StringVar()
        sv.trace('w', lambda name, index, mode, sv=sv: self._on_text_changed(sv))
        eLetters = tk.Entry(f, textvariable=sv, font=layoutFont, validate='key')
        vcmd = eLetters.register(self._validate_input)
        eLetters.config(validatecommand=(vcmd, '%d', '%S'))
        eLetters.pack(side=tk.TOP, fill=tk.X, expand=True)
        eLetters.bind('<Control-a>', self._select_all)
        eLetters.focus()

        bCalculate = tk.Button(f, text='Calculate', font=layoutFont)
        bCalculate.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=True)

        l = ttk.Label(f, text='Results:', font=layoutFont)
        l.pack(side=tk.TOP, anchor=tk.W)

        f = ttk.Frame(root)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(f, orient=tk.VERTICAL)
        lResults = tk.Listbox(f, selectmode=tk.EXTENDED, yscrollcommand=sb.set, font=resultsFont)
        sb.config(command=lResults.yview)
        lResults.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        lResults.bind('<Double-Button-1>', self._double_click)

        calc = lambda x=None: self._show_results(eLetters, lResults)
        bCalculate.configure(command=calc)
        eLetters.bind('<Return>', calc)

    def _on_text_changed(self, sv):
        sv.set(sv.get().upper())

    def _validate_input(self, action, key):
        return action != '1' or key.isalpha()

    def _select_all(self, event):
        event.widget.select_range(0, tk.END)
        return 'break'

    def _double_click(self, event):
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return

        value = widget.get(selection[0]).split(' ', 1)[1]

        webbrowser.open('https://www.google.com/search?q=define+' + value, 2)

    def _show_results(self, eLetters, lResults):
        self.root.config(cursor='wait')
        self._set_all_states(tk.DISABLED)
        self.root.update()

        lResults.config(state=tk.NORMAL)
        lResults.delete(0, 'end')

        for result in self.solver.get_matches(eLetters.get()):
            lResults.insert('end', '(%d) %s' % (len(result), result))

        self.root.config(cursor='')
        self._set_all_states(tk.NORMAL)


if __name__ == '__main__':
    app = App()
    app.mainloop()
