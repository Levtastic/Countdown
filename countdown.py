import Tkinter as tk, ttk, tkFont
#import tkinter.ttk as ttk
#import tkinter.font as tkFont
import os, sys
import collections
import webbrowser

class Countdown():
    def __init__(self):
        with open(self._resource_path('words.txt')) as f:
            words = [word.strip().lower() for word in f.readlines()]
        
        self.words = dict(zip(words, [collections.Counter(word) for word in words]))
        
        app_name = 'Countdown Tool'
        
        self.root = root = tk.Tk()
        root.title(app_name)
        root.geometry('345x315')
        root.minsize(345, 315)
        self._layout(root)
        root.iconbitmap(self._resource_path('icon.ico'))
        
        root.mainloop()
    
    def _layout(self, root):
        layoutFont = tkFont.Font(size = 18, weight = 'bold')
        resultsFont = tkFont.Font(size = 12)
        
        f = ttk.Frame(root)
        f.pack(side = tk.TOP, fill = tk.X)
        
        l = ttk.Label(f, text = 'Letters:', font = layoutFont)
        l.pack(side = tk.TOP, anchor = tk.W)
        
        eLetters = tk.Entry(f, font = layoutFont)
        eLetters.pack(side = tk.TOP, fill = tk.X, expand = True)
        eLetters.bind('<Key>', self._validate_input)
        eLetters.bind('<Control-a>', self._select_all)
        eLetters.focus()
        
        bCalculate = tk.Button(f, text = 'Calculate', font = layoutFont)
        bCalculate.pack(side = tk.TOP, anchor = tk.W, fill = tk.X, expand = True)
        
        l = ttk.Label(f, text = 'Results:', font = layoutFont)
        l.pack(side = tk.TOP, anchor = tk.W)
        
        f = ttk.Frame(root)
        f.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        sb = ttk.Scrollbar(f, orient = tk.VERTICAL)
        lResults = tk.Listbox(f, selectmode = tk.EXTENDED, yscrollcommand = sb.set, font = resultsFont)
        sb.config(command = lResults.yview)
        lResults.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        sb.pack(side = tk.RIGHT, fill = tk.Y)
        
        lResults.bind('<Double-Button-1>', self._double_click)
        
        calc = lambda x=None: self._show_results(eLetters, lResults)
        bCalculate.configure(command = calc)
        eLetters.bind('<Return>', calc)
    
    def _validate_input(self, event):
        if event.char and event.char not in 'abcdefghijklmnopqrstuvqxyz':
            return 'break'
        
        return None
    
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
        self.root.config(cursor = 'wait')
        self.root.update()
        
        lResults.delete(0, 'end')
        
        for result in self._calculate(eLetters.get().strip()):
            lResults.insert('end', '(%d) %s' % (len(result), result))
        
        self.root.config(cursor = '')
    
    def _calculate(self, letters):
        if not letters:
            return []
        
        results = []
        letters = collections.Counter(letters.lower())
        
        for word, word_letters in self.words.items():
            difference = collections.Counter(letters)
            difference.subtract(word_letters)
            if not any(val < 0 for val in difference.values()):
                results.append(word)
        
        return sorted(results, key = len, reverse = True)
    
    def _resource_path(self, relative):
        if getattr(sys, 'frozen', False):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)

        return os.path.join(basedir, relative)

if __name__ == '__main__':
    Countdown()
