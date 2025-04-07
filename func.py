import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from tkinter import filedialog
from dotenv import load_dotenv

import os
import ast
import data
import random
import requests
import mathfunc
import string
import json
import csv
import sys
import re

load_dotenv()

# System configurations
system = os.name

# Note functions -----------------------------------------------------------
def new_file(notes_box, title_box, text, title): 

    notes_box.delete(1.0, tk.END)
    notes_box.insert(tk.END, text)

    title_box.delete(1.0, tk.END)
    title_box.insert(tk.END, title)

def open_file(notes_box, title_box):
    
    # Ask for a file
    file_types = [("Text Files", "*.txt")]
    file_path = filedialog.askopenfilename(title = "Open Text File", filetypes = file_types)

    if file_path == None:
        return
    else:
        file_path = file_path.replace("/", "\\")
        data.recently_edited = file_path

    # Depending on the system read the file a different way
    if system == "posix":
        
        with open(file_path, encoding = 'utf-8') as file:
            file = open(file_path, encoding = 'utf-8')
            text = file.read()
            
            # Open a new file with the text we read
            new_file(notes_box, title_box, text, "Untitled")
    else:

        with open(file_path, encoding = 'utf-8') as file:
            file = open(file_path, encoding = 'utf-8')
            text = file.read()
            
            # Open a new file with the text we read
            new_file(notes_box, title_box, text, "Untitled")

def save(notes_box, title_box):

    if data.recently_edited != None:
        with open(data.recently_edited, "w", encoding = 'utf-8') as f:
            f = open(data.recently_edited, "w", encoding = 'utf-8')
            f.write(f"{title_box.get(1.0, tk.END)}\n")
            f.write(notes_box.get(1.0, tk.END))

    else:
        save_as(notes_box, title_box)

def save_as(notes_box, title_box):

    # Dialog box and then write the notes in
    file_types = [("All Files", "*.*"), ("Text Files", "*.txt")]
    file_name = f"{title_box.get(1.0, tk.END).strip()}.txt"

    file = filedialog.asksaveasfile(initialfile = file_name, filetypes = file_types, defaultextension = ".txt")

    if file:

        # Save file path in recently edited to find when saving things
        file_path = file.name.replace("/", "\\")
        data.recently_edited = file_path

        with open(file_path, "w", encoding = 'utf-8') as f:
            f = open(file_path, "w", encoding = 'utf-8')
            f.write(f"{title_box.get(1.0, tk.END)}\n")
            f.write(notes_box.get(1.0, tk.END).strip())

def change_theme(root, selected):

    cancelled = messagebox.askyesno("CAUTION", "In changing your theme this app will be forced to shutdown to make all correct changes. Continue?")

    # If cancelled, go back to what it was
    if not cancelled:
        if selected.get() == "Dark":
            selected.set("Light")
        else:
            selected.set("Dark")
    # If it goes through, change the theme
    else:
       data.mode = selected.get()[0]

       # Save preferences
       save = {"theme": f"{data.mode}"}
       json_file = json.dumps(save)
       with open("Save Data/save_data.json", "w") as f:
           f.write(json_file)

       root.destroy()

def load_theme():

    if os.path.exists("Save Data/save_data.json"):
        with open("Save Data/save_data.json", "r") as f:
            text = f.read()
            mode = json.loads(text)
            data.mode = mode["theme"]

# --------------------------------------------------------------------------


def edit_text(edit, text_box, highlight_spec):

    # Gets the indices of the selected text
    tag_range = text_box.tag_ranges("sel")
    if tag_range:
        i1, i2 = tag_range
    else:
        return
    
    def text_formatting(tag):

        # Gets each interval of ranges
        ranges = list(text_box.tag_ranges(tag))
        it = iter(ranges)
        formatted_ranges = list(zip(it, it))
    
        # Checks if selected region already has a tag
        if (i1, i2) in formatted_ranges:
            text_box.tag_remove(tag, i1, i2)
        else:
            # Get rid of any tags in the way
            for type in ["tag_bold", "tag_underline", "tag_strikethrough", "tag_italicize"]:
                if type != tag:
                    text_box.tag_remove(type, i1, i2)
 
            text_box.tag_add(tag, i1, i2)

    # For each case of each type of text edit
    if edit == "b":
        text_formatting("tag_bold")

    # Special highlighting requires modification of text_formatting function
    elif edit == "h":

        if highlight_spec == 0:
            for i in range(8):
                text_box.tag_remove(f"tag_highlight{i + 1}", i1, i2)
        else:
            for i in range(8):
                text_box.tag_remove(f"tag_highlight{i + 1}", i1, i2)

            text_box.tag_add(f"tag_highlight{highlight_spec}", i1, i2)

    elif edit == "u":
        text_formatting("tag_underline")

    elif edit == "i":
        text_formatting("tag_italicize")

    elif edit == "s":
        text_formatting("tag_strikethrough")

def style_window(root, notes_box):

    print("OFF LIMITS FOR NOW")
    return

    # Window initiation and config
    window = tk.Toplevel()

    w = int(root.winfo_screenwidth() * float(os.getenv("STYLE_WIDTH")))
    h = int(root.winfo_screenheight() * float(os.getenv("STYLE_HEIGHT")))

    window.geometry(f"{w}x{h}")
    window.title("Style Panel")
    window.attributes('-topmost', True)

    window.resizable(False, False)

    # --------------------------------------------------------------------------

    # Right frame with styling preview
    main1 = tk.Frame(window)
    main1.grid(padx = (10, 10), pady = (10, 10), sticky = "nsew", row = 0, column = 1)

    title1 = tk.Label(main1, text = "Text Preview", font = ('calibre', 24, 'bold'))
    title1.pack(anchor = "center", pady = (0, 10))

    window.grid_columnconfigure(1, weight = 1)
    window.grid_rowconfigure(0, weight = 1)

    preview = tk.Text(main1, font = ('calibre', 14, 'normal'), xscrollcommand = True, borderwidth = 7)
    preview.insert(1.0, os.getenv("FILLER_TEXT"))
    preview.config(state = "disabled")
    preview.pack(pady = (0, 10), anchor = "e", fill = 'both', expand = True)

    # Text color tags
    preview.tag_configure("tag_color1", foreground = data.colors["Red"])
    preview.tag_configure("tag_color2", foreground = data.colors["Orange"])
    preview.tag_configure("tag_color3", foreground = data.colors["Yellow"])
    preview.tag_configure("tag_color4", foreground = data.colors["Green"])
    preview.tag_configure("tag_color5", foreground = data.colors["Blue"])
    preview.tag_configure("tag_color6", foreground = data.colors["Purple"])
    preview.tag_configure("tag_color7", foreground = data.colors["Pink"])

    # --------------------------------------------------------------------------

    # Left frame with styling options
    main = tk.Frame(window)
    main.grid(padx = (10, 10), pady = (10, 10), sticky = "nsew", row = 0, column = 0)

    # Title
    title = tk.Label(main, text = "Styling", font = ('calibre', 24, 'bold'))
    title.pack(anchor = "nw", pady = (0, 10))

    # Dropdown menu for font sizes
    font_sizes = [
        "Title 1",
        "Title 2",
        "Title 3",
        "Text"
    ]

    box1 = tk.Frame(main)
    box1.pack(pady = (0, 10), anchor = "w")
    
    selected = tk.StringVar(box1)
    selected.set(font_sizes[-1])

    sizes_label = tk.Label(box1, text = "Font Size")
    sizes_label.pack(anchor = "w")

    sizes = tk.OptionMenu(box1, selected, *font_sizes, command = lambda f : edit_prev_text(preview, selected, "s"))
    sizes.pack()

    # Dropdown menu for font styles
    font_styles = [
        "Calibre",
        "Times New Roman"
    ]

    box2 = tk.Frame(main)
    box2.pack(pady = (0, 10), anchor = "w")

    selected1 = tk.StringVar(box2)
    selected1.set(font_styles[0])

    styles_label = tk.Label(box2, text = "Font Style")
    styles_label.pack(anchor = "w")

    styles = tk.OptionMenu(box2, selected1, *font_styles, command = lambda f : edit_prev_text(preview, selected1, "f"))
    styles.pack()

    # Dropdown menu for font colors
    colors = [
        "Red", 
        "Orange", 
        "Yellow", 
        "Green", 
        "Blue", 
        "Purple", 
        "Pink",
        "None"
    ]

    box3 = tk.Frame(main)
    box3.pack(pady = (0, 10), anchor = "w")

    selected2 = tk.StringVar(box3)
    selected2.set(colors[-1])

    colors_label = tk.Label(box3, text = "Font Colors")
    colors_label.pack(anchor = "w")

    colors = tk.OptionMenu(box3, selected2, *colors, command = lambda f : edit_prev_text(preview, selected2, "c"))
    colors.pack()

    change = tk.Button(box3, text = "Stylize", anchor = 'w', command = lambda : stylize_notes(notes_box))
    change.pack(anchor = "w", pady = (10, 10))

def edit_prev_text(text_box, style, op):

    # If modifying size of font
    if op == "s":
        # Create the new font and set current font equal to it
        new_size = data.sizes[style.get()]
        font = data.curr_font

        new_font = (font[0], new_size, font[2])
        
        data.curr_font = new_font

        # Replace and change text
        text_box.config(font = new_font)

        text_box.delete(1.0, tk.END)
        text_box.insert(1.0, os.getenv("FILLER_TEXT"))

        # Account for color
        text_box.tag_add(data.curr_color, 1.0, tk.END)

    elif op == "f":

        new_style = style.get().lower()
        font = data.curr_font

        new_font = (new_style, font[1], font[2])

        data.curr_font = new_font

        # Replace and change text
        text_box.config(font = new_font)

        text_box.delete(1.0, tk.END)
        text_box.insert(1.0, os.getenv("FILLER_TEXT"))

        # Account for color
        text_box.tag_add(data.curr_color, 1.0, tk.END)

    elif op == "c":

        if style.get() == data.curr_color:
            return

        if style.get() == "None":

            for i in range(8):
                text_box.tag_remove(f"tag_color{i + 1}", 1.0, tk.END)
            
            data.curr_color = "None"
            return
        
        new_color = list(data.colors.keys()).index(style.get()) + 1

        text_box.tag_remove(data.curr_color, 1.0, tk.END)

        # Store the color
        data.curr_color = style.get()

        # Change the color
        text_box.tag_add(f"tag_color{new_color}", 1.0, tk.END)

def stylize_notes(notes_box):
    
    # Gets the indices of the selected text
    tag_range = notes_box.tag_ranges("sel")
    if tag_range:
        i1, i2 = tag_range
    else:
        return
    
    # Pruning list for any unused fonts
    for i in range(len(data.generated_fonts)):

        font = data.generated_fonts[i]
        ranges = notes_box.tag_ranges(font)
        it = iter(ranges)
        formatted_ranges = list(zip(it, it))
        if len(formatted_ranges) == 0:
            data.generated_fonts.remove(font)
    
    # Generate a tag and add it to selected text
    tag = f"{data.curr_font}+{data.curr_color}"
    if data.curr_color == "None":
        notes_box.tag_configure(tag, font = data.curr_font, foreground = "White")
    else:
        notes_box.tag_configure(tag, font = data.curr_font, foreground = data.colors[data.curr_color])
    notes_box.tag_add(tag, i1, i2)

    if tag not in data.generated_fonts:
        data.generated_fonts.append(tag)


# Dictionary functions -----------------------------------------------------------
def load_hanzi():

    # A dictionary for every known frequency of every character 
    freqs = dict()
    avg_freq = 0 # If a hanzi does not have a frequency, take the average of all of the frequencies as its frequency

    with open('Chinese Data/hsk_words.csv', 'r', encoding = 'utf-8') as hsk:

        reader = csv.DictReader(hsk)
        
        for row in reader:
            if row["Freq"] != '—' and row["Freq"] != '':
                freqs[row["Word"]] = row["Freq"]

                avg_freq += int(row["Freq"])

    avg_freq /= len(freqs.keys())

    # Loading all of the characters, their corresponding pinyin and English meaning into data.hanzi
    with open('Chinese Data/freq_chars.csv', 'r', encoding = 'utf-8') as freq_chars:

        reader = csv.DictReader(freq_chars)
        
        for row in reader:

            # word = (pinyin, english, freq)
            data.hanzi[row["Word"]] = (row["Pinyin"], row["Meaning"], row["Freq"])

            freqs[row["Word"]] = row["Freq"]
            
    with open('Chinese Data/cedict.txt', 'r', encoding = 'utf-8') as cedict:

        lines = cedict.readlines()
        for line in lines:
            
            # Seperate each part of the word
            line = line[0:len(line) - 2]

            ci = line[0:line.index(' ')]
            fayin = line[line.index('[') + 1:line.index(']')]
            yisi = line[line.index('/') + 1:len(line)]

            # Remove spaces from pinyin
            pinyin_no_space = ""
            for c in fayin:
                if c != " ":
                    pinyin_no_space += c

            freq = freqs[ci] if ci in freqs.keys() else avg_freq

            # If the word is already somewhere
            if ci in data.hanzi.keys():
                
                new_pinyin = data.hanzi[ci][0].lower()
                if pinyin_no_space != data.hanzi[ci][0]:
                    new_pinyin = f"{data.hanzi[ci][0]}, {pinyin_no_space}"

                new_meaning = data.hanzi[ci][1]
                if yisi != data.hanzi[ci][1]:
                    new_meaning = f'{data.hanzi[ci][1]}; {yisi}'

                data.hanzi[ci] = (new_pinyin, new_meaning, data.hanzi[ci][2])
            else:
                data.hanzi[ci] = (pinyin_no_space, yisi, freq)

def add_word_entry(table, char, count):

    # Container for word entry
    word_entry = tk.Text(
        table, 
        font = ('calibre', 16, 'normal'), 
        wrap = "word",
        padx = 10,
        pady = 10,
        borderwidth = 0,
        background = os.getenv(f"{data.mode}_BG2"),
        foreground = os.getenv(f"{data.mode}_FONT")
    )
    word_entry.grid(row = count, column = 0, pady = (0, 10), sticky = "ew")

    word = char
    pinyin = data.hanzi[char][0]
    meaning = data.hanzi[char][1]

    text = f"{word}\n{pinyin}\n{meaning}"
    word_entry.insert(1.0, text)

    word_entry.config(state = "disabled")

    word_entry.update()
    w = word_entry.winfo_width()
    line_len = round(w / 22)

    height = 0
    for ele in [word, pinyin, meaning]:
        if ele != " ":
            height += (len(ele) // line_len) + 1

    word_entry.config(height = round(height) + 1)

    return word_entry.winfo_reqheight()

def load_results(word, parent):

    # Format search a little
    search = word.strip()
    search = search.lower()
    
    # If there is already a table holding results, get rid of its children
    if data.results_table:
        for child in data.results_table.winfo_children():
            child.destroy()

        data.results_canvas.config(scrollregion = data.results_canvas.bbox('all'))
    else:

        # Parent widget grid configuration ensures widget that expand stay within the window

        # Make a container for each character
        results = tk.Frame(parent, background = os.getenv(f"{data.mode}_BG1"))
        results.pack(padx = (20, 20), pady = (0, 20), fill = 'both', expand = True, anchor = "center")

        parent.grid_columnconfigure(0, weight = 1)
        parent.grid_rowconfigure(0, weight = 1)

        # Scrollbar with color
        style = ttk.Style()
        style.theme_use('classic')
        style.configure('Vertical.TScrollbar', background = os.getenv(f"{data.mode}_BG2"), troughcolor = os.getenv(f"{data.mode}_BG"))

        v_scroll = ttk.Scrollbar(results, orient = 'vertical',)
        v_scroll.pack(side = 'right', fill = 'y')

        # Canvas to allow for scrolling through of different results
        can = tk.Canvas(results, highlightthickness = 0, background = os.getenv(f"{data.mode}_BG1"))
        can.pack(fill = 'both', expand = True, side = 'left')

        results.grid_columnconfigure(0, weight = 1)

        # Binding scroll command to canvas
        can.bind('<MouseWheel>', lambda f : can.yview_scroll(f.delta / 100, "units"))

        v_scroll.config(command = can.yview)

        can.config(yscrollcommand = v_scroll.set)

        # Container for everything in canvas
        table = tk.Frame(can, background = os.getenv(f"{data.mode}_BG1"))

        table.grid_columnconfigure(0, weight = 1)

        # Add frame to window in canvas for viewing
        can.create_window((0, 0), window = table, tags = "frame", anchor = "nw")

        can.bind('<Configure>', lambda e : can.itemconfig('frame', width = can.winfo_width()))

        data.results_table = table
        data.results_canvas = can

    # If search bar is empty, return random characters
    if search == "":

        canvas_h = 0 # To get the total height needed for the canvas
        limit = int(os.getenv("RESULT_LIMIT"))

        max_freq = lambda item : int(item[1][2])
        items = data.hanzi.items()
        items = sorted(items, key = max_freq)

        # Create each text box for a word
        for i, char in enumerate(items[0:limit]):

            # Adds a composite widget with Chinese, pinyin, and English meaning
            canvas_h += add_word_entry(data.results_table, char[0], i)

        data.results_canvas.config(scrollregion = (0, 0, 0, canvas_h + (10 * limit)))
        
    else:

        indices = list()

        # Determine if it has Chinese characters in it
        contains_chin = False
        alphabet = list(string.ascii_lowercase)
        for c in search:
            if c not in alphabet and not c.isdigit():
                contains_chin = True

        # If it does, just search for one character
        if contains_chin:

            # If the Chinese character is in words, return all words with that character
            for char in data.hanzi.keys():
                if char.strip() == search or search in char:
                    indices.append(char)

            if search in indices:
                indices.remove(search)
                indices.insert(0, search)

        else:

            def remove_digits(s):
                s1 = ""
                for c in s:
                    if not c.isdigit() and c != " ":
                        s1 += c

                return s1
            
            search1 = remove_digits(search)

            # If the pinyin with numbers in pinyin, return the indices of those
            for item in data.hanzi.items():
                if item[1][0] == search or re.search(fr'\b{search}\b', item[1][0]):
                    indices.append((item[0], mathfunc.cosine_sim(search, item[1][0])))
                elif remove_digits(item[1][0]) == search1 or re.search(fr'\b{search}\b', remove_digits(item[1][0])):
                    indices.append((item[0], mathfunc.cosine_sim(search1, remove_digits(item[1][0]))))

            # Sorted by cosine similarity and frequency
            # Multiplies 1 - cosine sim by frequency to get a rating of relevancy
            max_sim = lambda item : (1 - item[2]) * float(item[1][2])
            items = [(indices[i][0], data.hanzi[indices[i][0]], indices[i][1]) for i in range(len(indices))]
            items = sorted(items, key = max_sim)

            indices = [item[0] for item in items]

            # Get a english dictionary to tell you synonyms of words so that lookup is easier
            if len(indices) == 0:

                # API used to find synonyms of the word
                api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(search)
                query = requests.get(api_url, headers={'X-Api-Key': 'taCjXEVJV/knI6sskfNpCQ==QsXBRkMKo0FMgl4a'})

                if query.status_code == requests.codes.ok:
                    response = ast.literal_eval(query.text)
                    synonyms = set(response["synonyms"])
                else:
                    print(f"Error {query.status_code}")

                synonyms = list(synonyms)
                if len(synonyms) >= int(os.getenv("SEARCH_LIMIT")):
                    synonyms = synonyms[0:int(os.getenv("SEARCH_LIMIT"))]
                
                for item in list(data.hanzi.items()):
                    for word in synonyms:
                        if re.search(fr'\b{word}\b', item[1][1]):
                            indices.append((item[0], 0.5))

                    if re.search(fr'\b{search}\b', item[1][1]):
                        indices.insert(0, (item[0], mathfunc.cosine_sim(search, item[1][1])))

                # Sorted by cosine similarity
                max_sim = lambda item : 1 - item[2]
                items = [(indices[i][0], data.hanzi[indices[i][0]], indices[i][1]) for i in range(len(indices))]
                items = sorted(items, key = max_sim)

                indices = [item[0] for item in items]
                
        canvas_h = 0

        limit = int(os.getenv("RESULT_LIMIT"))

        i_length = len(indices)
        if i_length != 0:
            if i_length >= limit:
                for i in range(limit):
                    canvas_h += add_word_entry(data.results_table, indices[i], i)

                data.results_canvas.config(scrollregion = (0, 0, 0, canvas_h + 300))
            else:
                for i in range(i_length):
                    canvas_h += add_word_entry(data.results_table, indices[i], i)

                data.results_canvas.config(scrollregion = (0, 0, 0, canvas_h + (10 * i_length)))