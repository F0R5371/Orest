import tkinter as tk
from tkinter import ttk

from tkinter import font
from dotenv import load_dotenv

import os
import data
import func

load_dotenv()

class Orest:

    def __init__(self):
        # To keep track of what section we are in
        self.sections = dict()

        # Create the menus and navbar
        self.setup()

    def setup(self):

        # Init
        root = tk.Tk()
        root.title("Orest - Eng/Zh Study Tool")
        root.attributes('-topmost', True)

        root.config(background = os.getenv(f"{data.mode}_BG1"))

        # App dimensions
        w = int(root.winfo_screenwidth() * float(os.getenv("APP_WIDTH")))
        h = int(root.winfo_screenheight() * float(os.getenv("APP_HEIGHT")))

        root.geometry(f"{w}x{h}")

        # --------------------------------------------------------------------------

        # Navigation bar (soon will not have text but images/icons for each button)
        navbar = tk.Frame(root, background = os.getenv(f"{data.mode}_BG1"))
        navbar.pack(pady = (10, 10), fill = 'x')
        navbar.grid_columnconfigure((0, 1, 2), weight = 1)

        # Notes, dictionary, and tools menus
        menu = tk.Menu(root, background = os.getenv(f"{data.mode}_BG1"))

        # Notes menu
        notes = tk.Menu(
            menu, tearoff = 0, 
            background = os.getenv(f"{data.mode}_BG1"), 
            foreground = os.getenv(f"{data.mode}_FONT")
        )
        menu.add_cascade(label = "File", menu = notes)

        notes_img = tk.Button(
            navbar, 
            text = "Notes", 
            command = lambda : self.open_section("Notes"), 
            background = os.getenv(f"{data.mode}_BG"), 
            foreground = os.getenv(f"{data.mode}_FONT"),
            borderwidth = 0,
        )
        notes_img.grid(row = 0, column = 0, padx=(10, 10))

        # Settings
        settings = tk.Menu(
            menu, 
            tearoff = 0, 
            background = os.getenv(f"{data.mode}_BG1"), 
            foreground = os.getenv(f"{data.mode}_FONT")
        )
        menu.add_cascade(label = "Edit", menu = settings)

        settings.add_command(label = "Preferences", command = lambda : self.open_section("Settings"))

        # Dictionary 
        dict_img = tk.Button(
            navbar, 
            text = "Dict", 
            command = lambda : self.open_section("Dictionary"), 
            background = os.getenv(f"{data.mode}_BG"),
            foreground = os.getenv(f"{data.mode}_FONT"),
            borderwidth = 0
        )
        dict_img.grid(row = 0, column = 1, padx=(10, 10))

        # Tools
        tools = tk.Menu(
            menu, 
            tearoff = 0, 
            background = os.getenv(f"{data.mode}_BG1"), 
            foreground = os.getenv(f"{data.mode}_FONT")
        )
        menu.add_cascade(label = "Tools", menu = tools)  

        opts_img = tk.Button(
            navbar, 
            text = "Options", 
            command = lambda : self.open_section("Settings"), 
            background = os.getenv(f"{data.mode}_BG"),
            foreground = os.getenv(f"{data.mode}_FONT"),
            borderwidth = 0
        )
        opts_img.grid(row = 0, column = 2, padx=(10, 10))

        root.config(menu = menu)

        # --------------------------------------------------------------------------
        
        screen = tk.Frame(root)
        screen.pack(expand = True, fill = 'both')
        screen.grid_rowconfigure(0, weight = 1)
        screen.grid_columnconfigure(0, weight = 1)

        # Loading instances of sections
        self.sections["Notes"] = Notes(root, screen, notes, tools)
        self.sections["Dictionary"] = Dictionary(root, screen, None, tools)
        self.sections["Settings"] = Settings(root, screen, settings, tools)

        # Where each frame will be contained in
        for frame in self.sections.values():
            frame.grid(row = 0, column = 0, sticky = tk.NSEW)

        # Start with notes open
        self.open_section("Notes")

        # --------------------------------------------------------------------------

        # Shortcut binding
        if os.name != "posix":
            root.bind(os.getenv("WIN_OPEN_NOTES_SHORT"), lambda f : self.open_section("Notes"))
            root.bind(os.getenv("WIN_OPEN_DICT_SHORT"), lambda f : self.open_section("Dictionary"))
            root.bind(os.getenv("WIN_OPEN_OPTIONS_SHORT"), lambda f : self.open_section("Settings"))

            root.bind(os.getenv("WIN_QUIT_SHORT"), lambda f : root.destroy())

        else:
            root.bind(os.getenv("OPEN_NOTES_SHORT"), lambda f : self.open_section("Notes"))
            root.bind(os.getenv("OPEN_DICT_SHORT"), lambda f : self.open_section("Dictionary"))
            root.bind(os.getenv("OPEN_OPTIONS_SHORT"), lambda f : self.open_section("Settings"))

            root.bind(os.getenv("MAC_QUIT_SHORT"), lambda f : root.destroy())

        root.mainloop()

    def open_section(self, section):
        selected = self.sections[section]
        selected.tkraise()


class Notes(tk.Frame):

    def __init__(self, root, parent, notes, tools):

        # Standard variables
        self.standard_font = font.Font(family = 'calibre', size = 14, weight = 'normal')

        # Actually initialize the frame
        tk.Frame.__init__(self, parent, background = os.getenv(f"{data.mode}_BG1"))

        # Notes GUI
        notes_title = tk.Text(
            self, 
            height = 1, 
            font = ('calibre', 24, 'bold'), 
            wrap = "word", 
            padx = 6,
            pady = 6,
            borderwidth = 0,
            foreground = os.getenv(f"{data.mode}_FONT"),
            background = os.getenv(f"{data.mode}_BG2")
        )
        notes_title.pack(side = 'top', fill = 'x', padx = (10, 10))

        notes_box = tk.Text(
            self, 
            font = self.standard_font, 
            borderwidth = 0, 
            xscrollcommand = True, 
            wrap = "word",
            padx = 6,
            pady = 6,
            foreground = os.getenv(f"{data.mode}_FONT"),
            background = os.getenv(f"{data.mode}_BG2")
        )
        notes_box.pack(expand = True, fill = 'both', padx = (10, 10), pady = (10, 10))

        func.new_file(notes_box, notes_title, "Notes here...", "Untitled")

        # General tags
        notes_box.tag_configure("tag_bold", font = font.Font(family = 'calibre', size = 14, weight = "bold"))
        notes_box.tag_configure("tag_underline", font = font.Font(family = 'calibre', size = 14, underline = True))
        notes_box.tag_configure("tag_italicize", font = font.Font(family = 'calibre', size = 14, slant = "italic"))
        notes_box.tag_configure("tag_strikethrough", font = font.Font(family = 'calibre', size = 14, overstrike = True))

        # Highlight tags
        notes_box.tag_configure("tag_highlight1", background = data.colors["Red"])
        notes_box.tag_configure("tag_highlight2", background = data.colors["Orange"])
        notes_box.tag_configure("tag_highlight3", background = data.colors["Yellow"])
        notes_box.tag_configure("tag_highlight4", background = data.colors["Green"])
        notes_box.tag_configure("tag_highlight5", background = data.colors["Blue"])
        notes_box.tag_configure("tag_highlight6", background = data.colors["Purple"])
        notes_box.tag_configure("tag_highlight7", background = data.colors["Pink"])

        # Notes menu commands
        notes.add_command(label = "New", command = lambda : func.new_file(notes_box, notes_title, "Notes here...", "Untitled"))
        notes.add_command(label = "Open", command = lambda : func.open_file(notes_box, notes_title))
        notes.add_command(label = "Save", command = lambda : func.save(notes_box, notes_title))
        notes.add_command(label = "Save As", command = lambda : func.save_as(notes_box, notes_title))

        notes.add_command(label = "Quit", command = lambda : root.destroy())

        # --------------------------------------------------------------------------

        # Keyboard short cuts for notes depending on system type
        if os.name != "posix":
            
            """
            root.bind("<Control-s>", lambda : func.save(notes_box, notes_title))
            root.bind("<Control-Shift-KeyPress-s>", lambda : func.save_as(notes_box, notes_title))
            root.bind("<Shift-n>", lambda : func.new_file(notes_box, notes_title, "Notes here...", "Untitled"))
            root.bind("<Shift-o>", lambda : func.open_file(notes_box, notes_title))
            """

            # Note tool keybinds
            root.bind(os.getenv("WIN_BOLD_SHORT"), lambda f : func.edit_text("b", notes_box, 0))
            root.bind(os.getenv("WIN_UNDER_SHORT"), lambda f : func.edit_text("u", notes_box, 0))
            root.bind(os.getenv("WIN_ITALI_SHORT"), lambda f : func.edit_text("i", notes_box, 0))
            root.bind(os.getenv("WIN_STRIKE_SHORT"), lambda f : func.edit_text("s", notes_box, 0))

            # Highlight keybinds
            """
            root.bind(f"<Control-1>", lambda f : func.edit_text("h", notes_box, 1))
            root.bind(f"<Control-2>", lambda f : func.edit_text("h", notes_box, 2))
            root.bind(f"<Control-3>", lambda f : func.edit_text("h", notes_box, 3))
            root.bind(f"<Control-4>", lambda f : func.edit_text("h", notes_box, 4))
            root.bind(f"<Control-5>", lambda f : func.edit_text("h", notes_box, 5))
            root.bind(f"<Control-6>", lambda f : func.edit_text("h", notes_box, 6))
            root.bind(f"<Control-7>", lambda f : func.edit_text("h", notes_box, 7))
            root.bind(f"<Control-~>", lambda f : func.edit_text("h", notes_box, 0))
            """
            
        else:

            """
            root.bind(os.getenv("SAVE_SHORT"), lambda f : func.save(notes_box, notes_title))
            root.bind(os.getenv("SAVE_AS_SHORT"), lambda f : func.save_as(notes_box, notes_title))
            root.bind(os.getenv("NEW_FILE_SHORT"), lambda f : func.new_file(notes_box, notes_title, "Notes here...", "Untitled"))
            root.bind(os.getenv("OPEN_FILE_SHORT"), lambda f : func.open_file(notes_box, notes_title))
            """

            # Note tool keybinds
            root.bind(os.getenv("MAC_BOLD_SHORT"), lambda f : func.edit_text("b", notes_box, 0))
            root.bind(os.getenv("MAC_UNDER_SHORT"), lambda f : func.edit_text("u", notes_box, 0))
            root.bind(os.getenv("MAC_ITALI_SHORT"), lambda f : func.edit_text("i", notes_box, 0))
            root.bind(os.getenv("MAC_STRIKE_SHORT"), lambda f : func.edit_text("s", notes_box, 0))

            # Highlight keybinds
            """
            root.bind(f"<Command-1>", lambda f : func.edit_text("h", notes_box, 1))
            root.bind(f"<Command-2>", lambda f : func.edit_text("h", notes_box, 2))
            root.bind(f"<Command-3>", lambda f : func.edit_text("h", notes_box, 3))
            root.bind(f"<Command-4>", lambda f : func.edit_text("h", notes_box, 4))
            root.bind(f"<Command-5>", lambda f : func.edit_text("h", notes_box, 5))
            root.bind(f"<Command-6>", lambda f : func.edit_text("h", notes_box, 6))
            root.bind(f"<Command-7>", lambda f : func.edit_text("h", notes_box, 7))
            root.bind(f"<Command-~>", lambda f : func.edit_text("h", notes_box, 0))
            """

        # --------------------------------------------------------------------------

        # Bolding, hightlighting tools etc.
        writing_tools = tk.Menu(tools, tearoff = 0)
        tools.add_cascade(label = "Writing", menu = writing_tools)

        writing_tools.add_command(label = "Bold", command = lambda : func.edit_text("b", notes_box, 0))
        writing_tools.add_command(label = "Underline", command = lambda : func.edit_text("u", notes_box, 0))
        writing_tools.add_command(label = "Italicize", command = lambda : func.edit_text("i", notes_box, 0))
        writing_tools.add_command(label = "Strikethrough", command = lambda : func.edit_text("s", notes_box, 0))

        highlights = tk.Menu(writing_tools, tearoff = 0)
        writing_tools.add_cascade(label = "Highlight", menu = highlights)
        
        highlights.add_command(label = "Red", command = lambda : func.edit_text("h", notes_box, 1))
        highlights.add_command(label = "Orange", command = lambda : func.edit_text("h", notes_box, 2))
        highlights.add_command(label = "Yellow", command = lambda : func.edit_text("h", notes_box, 3))
        highlights.add_command(label = "Green", command = lambda : func.edit_text("h", notes_box, 4))
        highlights.add_command(label = "Blue", command = lambda : func.edit_text("h", notes_box, 5))
        highlights.add_command(label = "Purple", command = lambda : func.edit_text("h", notes_box, 6))
        highlights.add_command(label = "Pink", command = lambda : func.edit_text("h", notes_box, 7))
        highlights.add_command(label = "Clear", command = lambda : func.edit_text("h", notes_box, 0))
    
        # Changing the appearance of the text, pops up a small window for this
        tools.add_command(label = "Style", command = lambda : func.style_window(root, notes_box))


class Dictionary(tk.Frame):
    
    def __init__(self, root, parent, dictionary, tools):

        # Initialize the frame
        tk.Frame.__init__(self, parent, background = os.getenv(f"{data.mode}_BG1"))

        # Main container
        main_dict = tk.Frame(self, background = os.getenv(f"{data.mode}_BG1"))
        main_dict.pack(padx = (20, 20), pady = (10, 10))

        # Search bar
        search_bar = tk.Frame(main_dict, background = os.getenv(f"{data.mode}_BG1"))
        search_bar.pack(side = 'top', fill = 'x')

        search_bar.grid_columnconfigure(0, weight = 1)

        search_entry = tk.Text(
            search_bar, 
            height = 0.8, 
            font = ('calibre', 24, 'normal'), 
            background = os.getenv(f"{data.mode}_BG2"),
            borderwidth = 0,
            foreground = os.getenv(f"{data.mode}_FONT"),
            padx = 5,
            pady = 5
        )
        search_entry.grid(row = 0, sticky = "ew")

        search_button = tk.Button(
            search_bar, 
            text = "Search", 
            command = lambda : func.load_results(search_entry.get(1.0, tk.END), self), 
            anchor = "w", 
            background = os.getenv(f"{data.mode}_BG"),
            borderwidth = 0,
            foreground = os.getenv(f"{data.mode}_FONT")
        )
        search_button.grid(row = 1, sticky = "ew", pady = (10, 0))

        # Results
        results = tk.Frame(self, background = os.getenv(f"{data.mode}_BG1"))
        results.pack(expand = True, fill = 'both')

        # Results label
        results_label = tk.Label(
            results, 
            text = "⎯⎯⎯⎯⎯ Results ⎯⎯⎯⎯⎯", 
            font = ('calibre', 18, 'bold'), 
            background = os.getenv(f"{data.mode}_BG1"), 
            foreground = os.getenv(f"{data.mode}_FONT")
        )
        results_label.pack(padx = (20, 20), pady = (0, 10))

        func.load_results("", results) # Loads all of the results into the table for viewing``


class Settings(tk.Frame):

    def __init__(self, root, parent, settings, tools):

        tk.Frame.__init__(self, parent, background = os.getenv(f"{data.mode}_BG1"))

        main_settings = tk.Frame(self, background = os.getenv(f"{data.mode}_BG1"))
        main_settings.pack(padx = (10, 10), pady = (10, 10), expand = True, fill = 'both')

        themes = tk.Frame(main_settings, background = os.getenv(f"{data.mode}_BG1"))
        themes.grid(row = 0, sticky = "w")

        themes_label = tk.Label(
            themes,
            text = "Theme",
            font = ('calibre', 24, 'bold'), 
            foreground = os.getenv(f"{data.mode}_FONT"),
            background = os.getenv(f"{data.mode}_BG1")
        )

        themes_label.pack(pady = (0, 10), anchor = "w")

        AVAILABLE_THEMES = ["Dark", "Light"]

        if data.mode == "D":
            default = "Dark"
        else:
            default = "Light"

        selected = tk.StringVar()

        style = ttk.Style()
        style.theme_use('classic')
        style.configure(
            'TMenubutton', 
            background = os.getenv(f"{data.mode}_BG"), 
            foreground = os.getenv(f"{data.mode}_FONT"), 
            highlightthickness = 0, 
            borderwidth = 0,
            activebackground = os.getenv(f"{data.mode}_BG2"),
            activeforeground = os.getenv(f"{data.mode}_BG2")
        )

        options = ttk.OptionMenu(themes, selected, default, *AVAILABLE_THEMES, command = lambda f : func.change_theme(root, selected))
        options["menu"].config(
            background = os.getenv(f"{data.mode}_BG"), 
            foreground = os.getenv(f"{data.mode}_FONT"),
            activebackground = os.getenv(f"{data.mode}_BG2")
        )

        options.pack(anchor = "w", padx = (10, 0))
        

def main():

    func.load_theme()
    func.load_hanzi()

    orest = Orest()

if __name__ == "__main__":
    main()
    