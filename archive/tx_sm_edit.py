from tkinter import *
from tkinter import scrolledtext
from tkinter.colorchooser import askcolor
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
import sys
import glob
import mido
import ctypes

print("Please comment the errors")

pygame.mixer.init()

def create_key(frame, note, row, col):
    btn = ttk.Button(clavier_virtuel, text=note, width=5)
    btn.grid(row=row, column=col)
    return btn

titre_projet = "Selectionnez un fichier ou créez en un"

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Partition file", "*.part")])
    if file_path:
        # Le fichier a été sélectionné, vous pouvez effectuer les opérations nécessaires ici
        print("Fichier sélectionné :", file_path)
        titre_projet = os.path.basename(file_path)
        app.title(titre_projet + "   -   TEXTA SM edit")
        app.deiconify()  # Afficher la fenêtre principale

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".part", filetypes=[("Partition file", "*.part"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write("Votre texte ici")

def exit_app():
    app.quit()
    
def open_doc():
    # fonction pour ouvrir le fichier doc_tx_sm_edit.pdf
    pass

def aff_historique(tasks):
    hystorique_window = Toplevel(app)
    hystorique_window.title("Historique")
    hystorique_window.geometry("100x100")

    list_command = Listbox(hystorique_window)
    list_command.pack(fill=BOTH, expand=True)

def new_partition():
    pass

def draw_note(event):
    # Obtenez les coordonnées du curseur de la souris
    x = event.x
    y = event.y
    
    # Dessinez une note à la position du curseur
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#212121")

def delete_note(event):
    # Obtenez les coordonnées du curseur de la souris
    x = event.x
    y = event.y
    
    # Recherchez les éléments présents à la position du curseur
    elements = canvas.find_overlapping(x, y, x, y)
    
    # Supprimez tous les éléments trouvés à la position du curseur
    for element in elements:
        canvas.delete(element)

def draw_grid(canvas, x, y, width, height, spacing):
    # Dessiner les lignes horizontales
    for i in range(y, height + y, spacing):
        canvas.create_line(x, i, x + width, i, fill="gray")

    # Dessiner les lignes verticales
    for i in range(x, width + x, spacing):
        canvas.create_line(i, y, i, y + height, fill="gray")

def new_mesure():
    draw_staff(canvas, 50, 50, 4)

    draw_staff(draw_part, 50, 50, 4)

def select_or_create_file():
    dialog_window = Tk()
    dialog_window.title("Bienvenue")
    dialog_window.geometry("250x250")
    dialog_window.resizable(False, False)

    listbox_frame = ttk.Frame(dialog_window, width=50)
    listbox_frame.pack(side=LEFT, fill=Y)

    # Ajouter une Listbox
    listbox = Listbox(listbox_frame)
    listbox.pack(fill=BOTH, expand=True)

    def create_new_file():
        filename = filedialog.asksaveasfilename(filetypes=[("Partition file", "*.part")])
        if filename:
            with open(filename, 'w') as f:
                f.write("Contenu de votre fichier ici.")
            titre_projet = os.path.basename(filename)
            app.title(titre_projet + "   -   TEXTA SM edit")
            dialog_window.destroy()
            app.deiconify()

    def open_file0():
        file_path = filedialog.askopenfilename(filetypes=[("Partition file", "*.part")])
        if file_path:
            # Le fichier a été sélectionné, vous pouvez effectuer les opérations nécessaires ici
            # print("Fichier sélectionné :", file_path)
            titre_projet = os.path.basename(file_path)
            app.title(titre_projet + "   -   TEXTA SM edit")
            dialog_window.destroy()
            app.deiconify()

    def fill_listbox():
        listbox.delete(0, END)  # Effacer le contenu actuel de la liste box
        for filepath in glob.glob('*.part'):
            print("Fichier trouvé :", filepath)  # Vérifier si les fichiers sont détectés correctement
            listbox.insert(END, filepath)

    open_selection = ttk.Button(dialog_window, text="Ouvrir la selection")
    open_selection.pack(padx=10, pady=10)

    open_Button = ttk.Button(dialog_window, text="Ouvrir", command=open_file0)
    open_Button.pack(padx=10, pady=10)

    new_Button = ttk.Button(dialog_window, text="Nouveau", command=create_new_file)
    new_Button.pack(padx=10, pady=10)

def new_project():
    filename = filedialog.asksaveasfilename(filetypes=[("Partition file", "*.part")])
    if filename:
         with open(filename, 'w') as f:
            f.write("Contenu de votre fichier ici.")
    titre_projet = os.path.basename(filename)
    app.title(titre_projet + "   -   TEXTA SM edit")

def save_at():
    pass

def print():
    pass

def score_online():
    pass

def score_movie():
    pass

def import_audio():
    pass

def import_MIDI():
    pass

def import_xml():
    pass

def export_audio():
    pass

def export_picture():
    pass

def export_pdf():
    pass

def export_midi():
    pass

def export_xml():
    pass

def close_project():
    pass

def new_version_project():
    pass

def annule():
    pass

def retablir():
    pass

def cut():
    pass

def copy():
    pass

def coly():
    pass

def select():
    pass

def all_select():
    pass

def shearch():
    pass

def reorganize():
    pass

def mesure_auto():
    pass

def annotation_perfomant():
    pass

def open_midi_edit():
    pass

def open_rythme_edit():
    pass

def open_midi_edit_on_score():
    pass

def open_control_edit():
    pass

def saved_midi():
    pass

def transpose():
    pass

def setting_midi():
    setting_midi_window = Toplevel(app)
    setting_midi_window.title("paramèrte MIDI")
    setting_midi_window.resizable(False, False)

    # interface des parametres midi

def duplic_part():
    pass

def new_version_score():
    pass

def delete_score():
    pass

def delete_vierge_scores():
    pass

def bibilotheque():
    bibliotheque_window = Toplevel(app)
    bibliotheque_window.title("Bibliothèque")
    bibliotheque_window.resizable(False, False)
    bibliotheque_window.configure(bg="#212121")

    books = ["Livre 1", "Livre 2", "Livre 3", "Livre 4", "Livre 5"]

    # Création d'une Listbox
    listbox = Listbox(bibliotheque_window, width=50, height=10, bg="#212121", fg="white")
    listbox.pack(pady=10)

    # Ajout des éléments à la Listbox
    for book in books:
        listbox.insert(END, book)

    # Ajout d'une scrollbar à la Listbox
    scrollbar = Scrollbar(bibliotheque_window, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Lier la scrollbar à la Listbox
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

def marqueurs():
    pass

def explorer():
    explorer_window = Toplevel(app)
    explorer_window.title("Explorateur du projet")
    explorer_window.resizable(False, False)
    explorer_window.configure(bg="#212121")

def calc_tempo():
    calc_tempo_window = Toplevel(app)
    calc_tempo_window.title("Calculatrice de tempo")
    calc_tempo_window.resizable(False, False)
    calc_tempo_window.configure(bg="#212121")

def timecode_curseur():
    timecode_window = Toplevel(app)
    timecode_window.title("Définir Timecode curseur")
    timecode_window.resizable(False, False)
    timecode_window.configure(bg="#212121")

def notepad():
    notepad_window = Toplevel(app)
    notepad_window.title("Bloc-note")
    notepad_window.resizable(False, False)
    notepad_window.configure(bg="#212121")

    notepad_zone = scrolledtext.ScrolledText(notepad_window, wrap=WORD, font=("Courier New", 12), bg="#212121")
    notepad_zone.pack(expand=True, fill="both")

def decrypt_audio():
    pass

def decrypt_midi_live():
    pass

def decrypt_midi():
    pass

def decrypt_audio_saved():
    pass

def harmonic_annaliser():
    pass

def tonn_annalyse():
    pass

def Scan_partition_decryption():
    pass

def hauteur_correction():
    pass

def partition_option():
    partition_option_window = Toplevel(app)
    partition_option_window.title("Option de parittion")
    partition_option_window.resizable(False, False)

    # interface options partition

def page_mode():
    pass

def masque_onglet():
    if check_var_onglet.get():
        notebook.pack(expand=True, fill="both")
    else:
        notebook.pack_forget()


def on_grid_click(event):
    # Obtenir les coordonnées du clic de souris
    x = event.x
    y = event.y

    # Convertir les coordonnées du clic en indices de la grille MIDI
    column = (x - 10) // 48
    row = (y - 10) // 30

    # Afficher les coordonnées MIDI dans la console (pour le moment)
    # print(f"Clicked on column {column}, row {row}")

def xpanel_menu(event):
    menu_logo.post(event.x_root, event.y_root)

# définitions menu clic droit

def show_context_menu_toolbar(event):
    context_menu_toolbar.post(event.x_root, event.y_root)

def show_context_menu_canvas(event):
    context_menu_canvas.post(event.x_root, event.y_root)

def show_context_menu_notebook(event):
    context_menu_notebook.post(event.x_root, event.y_root)


# select_or_create_file()

app = Tk()

style = ttk.Style()

def set_dark_theme():
    if "dark_theme" not in style.theme_names():
        style.theme_create("dark_theme", parent="alt", settings={
            "TFrame": {"configure": {"background": "#212121"}},
            "TLabel": {"configure": {"foreground": "white", "background": "#212121"}},
            "TCheckbutton": {"configure": {"background": "#212121", "foreground": "white"}},
            "TScale": {"configure": {"background": "#00004B", "foreground": "#2F2F2F", "relief": "flat"}},
            "TButton": {
                "configure": {"background": "#2F2F2F", "foreground": "white", "borderwidth": 1},
                "map": {
                    "background": [("active", "#00004B")],
                    "foreground": [("active", "white")]
                }
            },
            "TEntry": {
                "configure": {
                    "background": "#2F2F2F", 
                    "foreground": "white", 
                    "selectbackground": "#00004B", 
                    "fieldbackground": "#2F2F2F",
                    "selectforeground": "white",
                    "relief": "flat",
                    "padding": 3
                }
            },
            "TNotebook": {"configure": {"background": "#212121", "foreground": "white"}},
            "TNotebook.Tab": {"configure": {"padding": [5, 1], "background": "#2F2F2F", "foreground": "white", "relief": "flat"}},
            "TCombobox": {
                "configure": {
                    "background": "#2F2F2F", 
                    "foreground": "white", 
                    "selectbackground": "#00004B", 
                    "fieldbackground": "#2F2F2F",
                    "selectforeground": "white",
                    "relief": "flat",
                    "padding": 3
                },
                "map": {
                    "background": [("readonly", "#2F2F2F"), ("active", "#00004B")],
                    "foreground": [("readonly", "white"), ("active", "white")],
                    "fieldbackground": [("readonly", "#2F2F2F"), ("active", "#00004B")]
                }
            },
            "TCanvas": {
                "configure": {"background": "#212121", "foreground": "white", "highlightbackground": "white"}
            }
        })
        app.option_add("*TMenubutton*Background", "#2F2F2F")
        app.option_add("*TMenubutton*Foreground", "white")
        app.option_add("*Menu*Background", "#2F2F2F")
        app.option_add("*Menu*Foreground", "white")
        app.option_add("*Menu*activeBackground", "#00004B")
        app.option_add("*Menu*activeForeground", "white")
        app.option_add("*Menu*BorderWidth", 0)
        app.option_add("*Menu*relief", "flat")
        app.option_add("*Canvas.Background", "#212121")
        app.option_add("*Canvas.Foreground", "white")
    style.theme_use("dark_theme")
    app.configure(bg="#212121")

def set_light_theme():
    if "light_theme" not in style.theme_names():
        style.theme_create("light_theme", parent="alt", settings={
            "TFrame": {"configure": {"background": "#FFFFFF"}},
            "TLabel": {"configure": {"foreground": "black", "background": "#FFFFFF"}},
            "TCheckbutton": {"configure": {"background": "#FFFFFF", "foreground": "black"}},
            "TScale": {"configure": {"background": "#B0DEFF", "foreground": "#F1F1F1", "relief": "flat"}},
            "TButton": {
                "configure": {"background": "#F1F1F1", "foreground": "black", "borderwidth": 1},
                "map": {
                    "background": [("active", "#B0DEFF")],
                    "foreground": [("active", "black")]
                }
            },
            "TEntry": {
                "configure": {
                    "background": "#F1F1F1", 
                    "foreground": "black", 
                    "selectbackground": "#B0DEFF", 
                    "fieldbackground": "#F1F1F1",
                    "selectforeground": "black",
                    "relief": "flat",
                    "padding": 3
                }
            },
            "TNotebook": {"configure": {"background": "#FFFFFF", "foreground": "black"}},
            "TNotebook.Tab": {"configure": {"padding": [5, 1], "background": "#F1F1F1", "foreground": "black", "relief": "flat"}},
            "TScrollbar": {"configure": {"background": "#B0DEFF", "foreground": "black", "borderwidth": 1, "relief": "flat"}},
            "TCombobox": {
                "configure": {
                    "background": "#F1F1F1", 
                    "foreground": "black", 
                    "selectbackground": "#B0DEFF", 
                    "fieldbackground": "#F1F1F1",
                    "selectforeground": "black",
                    "relief": "flat",
                    "padding": 3
                },
                "map": {
                    "background": [("readonly", "#F1F1F1"), ("active", "#B0DEFF")],
                    "foreground": [("readonly", "black"), ("active", "black")],
                    "fieldbackground": [("readonly", "#F1F1F1"), ("active", "#B0DEFF")]
                }
            },
            "TCanvas": {
                "configure": {"background": "#FFFFFF", "foreground": "black", "highlightbackground": "black"}
            }
        })
        app.option_add("*TMenubutton*Background", "#F1F1F1")
        app.option_add("*TMenubutton*Foreground", "black")
        app.option_add("*Menu*Background", "#F1F1F1")
        app.option_add("*Menu*Foreground", "black")
        app.option_add("*Menu*activeBackground", "#B0DEFF")
        app.option_add("*Menu*activeForeground", "black")
        app.option_add("*Menu*BorderWidth", 0)
        app.option_add("*Menu*relief", "flat")
        app.option_add("*Canvas.Background", "#FFFFFF")
        app.option_add("*Canvas.Foreground", "black")
    style.theme_use("light_theme")
    app.configure(bg="#FFFFFF")


def set_dark_high_contrast_theme():
    if "dark_high_contrast_theme" not in style.theme_names():
        style.theme_create("dark_high_contrast_theme", parent="alt", settings={
            "TFrame": {"configure": {"background": "#000000", "bordercolor": "#FFFFFF"}},
            "TLabel": {"configure": {"foreground": "#FFFFFF", "background": "#000000"}},
            "TCheckbutton": {"configure": {"background": "#000000", "foreground": "#FFFFFF", "indicatorbackground": "#000000"}},
            "TScale": {"configure": {"background": "#000000", "foreground": "#FFFFFF", "relief": "flat"}},
            "TButton": {
                "configure": {"background": "#000000", "foreground": "#FFFFFF", "bordercolor": "#FFFFFF"},
                "map": {"background": [("active", "#FFFF00"), ("disabled", "#333333")], "foreground": [("active", "#0000FF")]}
            },
            "TEntry": {
                "configure": {"background": "#000000", "foreground": "#FFFFFF", "selectbackground": "#FFFF00",
                              "fieldbackground": "#000000", "selectforeground": "#000000", "relief": "flat", "padding": 3}
            },
            "TNotebook": {"configure": {"background": "#000000", "foreground": "#FFFFFF"}},
            "TNotebook.Tab": {"configure": {"padding": [5, 1], "background": "#000000", "foreground": "#FFFFFF", "relief": "flat"}},
            "TScrollbar": {"configure": {"background": "#000000", "foreground": "#FFFFFF", "bordercolor": "#FFFFFF", "relief": "flat"}},
            "TCombobox": {
                "configure": {"background": "#000000", "foreground": "#FFFFFF", "selectbackground": "#FFFF00",
                              "fieldbackground": "#000000", "selectforeground": "#000000", "relief": "flat", "padding": 3},
                "map": {"background": [("readonly", "#000000"), ("active", "#FFFF00")],
                        "foreground": [("readonly", "#FFFFFF"), ("active", "#000000")],
                        "fieldbackground": [("readonly", "#000000"), ("active", "#FFFF00")]}
            }
        })
        app.option_add("*TMenubutton*Background", "#000000")
        app.option_add("*TMenubutton*Foreground", "#FFFFFF")
        app.option_add("*Menu*Background", "#000000")
        app.option_add("*Menu*Foreground", "#FFFFFF")
        app.option_add("*Menu*activeBackground", "#FFFF00")
        app.option_add("*Menu*activeForeground", "#000000")
        app.option_add("*Menu*BorderWidth", 0)
        app.option_add("*Menu*relief", "flat")
        app.option_add("*Canvas.Background", "#000000")
        app.option_add("*Canvas.Foreground", "#FFFFFF")
    style.theme_use("dark_high_contrast_theme")
    app.configure(bg="#000000")

def set_light_high_contrast_theme():
    if "light_high_contrast_theme" not in style.theme_names():
        style.theme_create("light_high_contrast_theme", parent="alt", settings={
            "TFrame": {"configure": {"background": "#FFFFFF", "bordercolor": "#000000"}},
            "TLabel": {"configure": {"foreground": "#000000", "background": "#FFFFFF"}},
            "TCheckbutton": {"configure": {"background": "#FFFFFF", "foreground": "#000000", "indicatorbackground": "#FFFFFF"}},
            "TScale": {"configure": {"background": "#FFFFFF", "foreground": "#000000", "relief": "flat"}},
            "TButton": {
                "configure": {"background": "#FFFFFF", "foreground": "#000000", "bordercolor": "#000000"},
                "map": {"background": [("active", "#FFFF00"), ("disabled", "#CCCCCC")], "foreground": [("active", "#0000FF")]}
            },
            "TEntry": {
                "configure": {"background": "#FFFFFF", "foreground": "#000000", "selectbackground": "#000000",
                              "fieldbackground": "#FFFFFF", "selectforeground": "#FFFFFF", "relief": "flat", "padding": 3}
            },
            "TNotebook": {"configure": {"background": "#FFFFFF", "foreground": "#000000"}},
            "TNotebook.Tab": {"configure": {"padding": [5, 1], "background": "#FFFFFF", "foreground": "#000000", "relief": "flat"}},
            "TScrollbar": {"configure": {"background": "#FFFFFF", "foreground": "#000000", "bordercolor": "#000000", "relief": "flat"}},
            "TCombobox": {
                "configure": {"background": "#FFFFFF", "foreground": "#000000", "selectbackground": "#000000",
                              "fieldbackground": "#FFFFFF", "selectforeground": "#FFFFFF", "relief": "flat", "padding": 3},
                "map": {"background": [("readonly", "#FFFFFF"), ("active", "#000000")],
                        "foreground": [("readonly", "#000000"), ("active", "#FFFFFF")],
                        "fieldbackground": [("readonly", "#FFFFFF"), ("active", "#000000")]}
            }
        })
        app.option_add("*TMenubutton*Background", "#FFFFFF")
        app.option_add("*TMenubutton*Foreground", "#000000")
        app.option_add("*Menu*Background", "#FFFFFF")
        app.option_add("*Menu*Foreground", "#000000")
        app.option_add("*Menu*activeBackground", "#000000")
        app.option_add("*Menu*activeForeground", "#FFFFFF")
        app.option_add("*Menu*BorderWidth", 0)
        app.option_add("*Menu*relief", "flat")
        app.option_add("*Canvas.Background", "#FFFFFF")
        app.option_add("*Canvas.Foreground", "#000000")
    style.theme_use("light_high_contrast_theme")
    app.configure(bg="#FFFFFF")

# Détection du thème système
def detect_system_theme():
    try:
        if ctypes.windll.shcore.GetScaleFactorForDevice(0) > 0:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            apps_use_light_theme = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
            winreg.CloseKey(key)
            if apps_use_light_theme == 0:
                return "dark"
            else:
                return "light"
    except:
        pass
    return "light"

PREDEFINED_COLORS = {
    "Bleu": "#0000FF",
    "Rouge": "#FF0000",
    "Vert": "#00FF00",
    "Jaune": "#FFFF00",
    "Gris": "#808080",
    "Brun": "#A52A2A",
    "Rose": "#FFC0CB",
    "Violet": "#800080",
}

# Boîte de dialogue personnalisée pour la sélection de thème
class ThemeDialog(simpledialog.Dialog):
    def body(self, master):
        Label(master, text="Choisir un thème:").pack(pady=10)
        
        # Combobox pour les thèmes
        self.theme_combobox = ttk.Combobox(master, values=[
            "Thème Sombre", 
            "Thème Clair", 
            "Thème Sombre Contraste Élevé", 
            "Thème Clair Contraste Élevé", 
            "Thème Système",
            "Personnaliser les Couleurs"
        ])
        self.theme_combobox.set("Choisir un thème")
        self.theme_combobox.pack(pady=10)
        
        # Combobox pour les couleurs prédéfinies
        Label(master, text="Choisir une couleur:").pack(pady=10)
        self.color_combobox = ttk.Combobox(master, values=list(PREDEFINED_COLORS.keys()) + ["Couleur Système"])
        self.color_combobox.set("Bleu")  # Couleur par défaut
        self.color_combobox.pack(pady=10)
        
        return self.theme_combobox
    
    def choose_color(self):
        color_choice = self.color_combobox.get()
        if color_choice == "Couleur Système":
            color = askcolor(title="Choisir une couleur")[1]
        else:
            color = PREDEFINED_COLORS.get(color_choice, "#0000FF")  # Par défaut, retourne bleu
        
        if color:
            self.custom_color = color  # Enregistre la couleur choisie
            # Mettre à jour l'interface ou d'autres actions nécessaires
    
    def apply(self):
        self.result = self.theme_combobox.get()
        if self.result == "Personnaliser les Couleurs":
            self.choose_color()
            self.result = self.custom_color  # Utilise la couleur personnalisée

# Exemple de fonctions pour définir les thèmes avec couleur personnalisée
def set_dark_theme_custom(color):
    app.configure(bg="#212121", fg="white")  # Exemple : appliquer le thème sombre avec la couleur personnalisée

def set_light_theme_custom(color):
    app.configure(bg="#FFFFFF", fg="black")  # Exemple : appliquer le thème clair avec la couleur personnalisée

# Fonction pour afficher la boîte de dialogue et changer le thème
def change_theme():
    dialog = ThemeDialog(app, title="Sélectionner le Thème")
    selected_theme = dialog.result
    if selected_theme == "Thème Sombre":
        set_dark_theme()
    elif selected_theme == "Thème Clair":
        set_light_theme()
    elif selected_theme == "Thème Sombre Contraste Élevé":
        set_dark_high_contrast_theme()
    elif selected_theme == "Thème Clair Contraste Élevé":
        set_light_high_contrast_theme()
    elif selected_theme == "Thème Système":
        system_theme = detect_system_theme()
        if system_theme == "dark":
            set_dark_theme()
        else:
            set_light_theme()
    elif selected_theme.startswith("#"):  # Couleur personnalisée
        set_dark_theme_custom(selected_theme)


def fade_to_color(widget, start_color, end_color, steps=10, delay=30):
    r1, g1, b1 = app.winfo_rgb(start_color)
    r2, g2, b2 = app.winfo_rgb(end_color)
    
    r_step = (r2 - r1) // steps
    g_step = (g2 - g1) // steps
    b_step = (b2 - b1) // steps
    
    def update_color(step):
        if step > steps:
            return
        r = r1 + (r_step * step)
        g = g1 + (g_step * step)
        b = b1 + (b_step * step)
        color = f'#{r//256:02x}{g//256:02x}{b//256:02x}'
        widget.configure(background=color)
        app.after(delay, update_color, step + 1)
    
    update_color(0)

def create_fade_button(parent, text, command, start_color="#2F2F2F", end_color="#00004B"):
    button = ttk.Button(parent, text=text, command=command, style="TButton")
    button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def on_enter(event):
        fade_to_color(button, start_color, end_color)
        
    def on_leave(event):
        fade_to_color(button, end_color, start_color)
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# app.withdraw()

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

app.title(titre_projet + "   -   TEXTA SM edit (ancienne version)")
app.geometry("1100x625+50+50")
app.configure(bg="#212121")

# Barre d'outils
toolbar = ttk.Frame(app)
toolbar.pack(side=TOP, fill=X)

img_tx = ImageTk.PhotoImage(Image.open("IconApp/tx.ico"))
# """
label_tx = ttk.Label(toolbar, text="TX")
# label_tx = ttk.Label(toolbar, text="TEXTA")
label_tx.pack(side=tk.LEFT, padx=5, pady=2)
# """

def select_in_canvas():
    pass

select_button = ttk.Button(toolbar, icon="IconApp/custombar/selections.png")
select_button.pack(side=tk.LEFT, padx=2, pady=2)

gomme_button = ttk.Button(toolbar, icon="IconApp/custombar/gomme.png")
gomme_button.pack(side=tk.LEFT, padx=2, pady=2)

loupe_button = ttk.Button(toolbar, icon="IconApp/custombar/loupe.png")
loupe_button.pack(side=tk.LEFT, padx=2, pady=2)

insert_button = ttk.Button(toolbar, icon="IconApp/custombar/insertion.png")
insert_button.pack(side=tk.LEFT, padx=2, pady=2)

ciseaux_button = ttk.Button(toolbar, icon="IconApp/custombar/ciseaux.png")
ciseaux_button.pack(side=tk.LEFT, padx=2, pady=2)

colle_button = ttk.Button(toolbar, icon="IconApp/custombar/colle.png")
colle_button.pack(side=tk.LEFT, padx=2, pady=2)

quantifications_button = ttk.Button(toolbar, icon="IconApp/custombar/quantifications.png")
quantifications_button.pack(side=tk.LEFT, padx=2, pady=2)

export_select_button = ttk.Button(toolbar, icon="IconApp/custombar/selection à exporter.png")
export_select_button.pack(side=tk.LEFT, padx=2, pady=2)

separator = ttk.Separator(toolbar, orient='vertical')
separator.pack(fill='y', side=LEFT, padx=10, pady=5)

one_ton_plus_button = ttk.Button(toolbar, icon="IconApp/custombar/note_supp.png")
one_ton_plus_button.pack(side=tk.LEFT, padx=2, pady=2)

one_ton_moin_Button = ttk.Button(toolbar, icon="IconApp/custombar/note_inf.png")
one_ton_moin_Button.pack(side=tk.LEFT, padx=2, pady=2)

oct_supp_Button = ttk.Button(toolbar, icon="IconApp/custombar/oct_supp.png")
oct_supp_Button.pack(side=tk.LEFT, padx=2, pady=2)

one_ton_plus_moin_Button = ttk.Button(toolbar, text="- 1/2 ton")
one_ton_plus_moin_Button.pack(side=LEFT, pady=5)

octave_plus_Button = ttk.Button(toolbar, text="+ octave")
octave_plus_Button.pack(side=LEFT, pady=5)

ocate_moin_Button = ttk.Button(toolbar, text="- octave")
ocate_moin_Button.pack(side=LEFT, pady=5)

separator = ttk.Separator(toolbar, orient='vertical')
separator.pack(fill='y', side=LEFT, padx=10, pady=5)

def_automatique_Button = ttk.Button(toolbar, icon="IconApp/custombar")
def_automatique_Button.pack(side=tk.LEFT, padx=2, pady=2)

# defil_auto_Button = ttk.Button(toolbar, text="Défilement automataique")
# defil_auto_Button.pack(side=LEFT, pady=5)

selected_value = StringVar()

options = ["1/1", "2/1", "4/1", "8/1", "16/1"]

combobox = ttk.Combobox(toolbar, textvariable=selected_value, values=options)
combobox.pack(side=LEFT, padx=2, pady=2)

combobox.set("Quantifier la note")

def on_combobox_change(event):
    selected_option = selected_value.get()
    print("Option sélectionnée :", selected_option)

combobox.bind("<<ComboboxSelected>>", on_combobox_change)

separator = ttk.Separator(toolbar, orient='vertical')
separator.pack(fill='y', side=LEFT, padx=10, pady=5)

btn_new_partition = ttk.Button(toolbar, text="Nouvelle partition", command=new_partition)
btn_new_partition.pack(side=LEFT, pady=5)

def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen  # On inverse l'état du plein écran
    app.attributes("-fullscreen", is_fullscreen)  # Active/Désactive le plein écran
    if is_fullscreen:
        fullscreen_button.config(text="Quitter plein écran")  # Change le texte du bouton
    else:
        fullscreen_button.config(text="Plein écran")

is_fullscreen = False  # Variable pour suivre l'état du plein écran

fullscreen_button = ttk.Button(toolbar, text="Plein écran", command=toggle_fullscreen)
fullscreen_button.pack(side=LEFT, pady=5)


check_var_onglet = tk.BooleanVar()

check_onglet = Checkbutton(
    toolbar,
    text="onglet",
    variable=check_var_onglet,
    command=masque_onglet,
    onvalue=1,
    offvalue=0,
    state=tk.NORMAL,
    foreground="white",
    background="#212121",
    relief=FLAT
)
check_onglet.pack(side=RIGHT, pady=2, padx=2)

app_nt = ttk.Notebook()

# Barre latérale
sidebar = ttk.Frame(app, width=15)
sidebar.pack(side=LEFT, fill=Y)

label = ttk.Label(sidebar, text="Inserer :", anchor="w", justify="left", width=10)
label.pack(fill=X)

btn_favorite = ttk.Button(sidebar, text="Favorits", width=15)
btn_favorite.pack(pady=5, padx=5)

btn_tonnalité = ttk.Button(sidebar, text="Tonnalité", width=15)
btn_tonnalité.pack(pady=5, padx=5)

btn_cle = ttk.Button(sidebar, text="Clés", width=15)
btn_cle.pack(pady=5, padx=5)

btn_mesures = ttk.Button(sidebar, text="Mesures", width=15)
btn_mesures.pack(pady=5, padx=5)

btn_accord = ttk.Button(sidebar, text="Symboles d'accords", width=15)
btn_accord.pack(pady=5, padx=5)

btn_guitare = ttk.Button(sidebar, text="Symboles guitares", width=15)
btn_guitare.pack(pady=5, padx=5)

btn_notes_symbole = ttk.Button(sidebar, text="Symbole de notes", width=15)
btn_notes_symbole.pack(pady=5, padx=5)

btn_nuance = ttk.Button(sidebar, text="Nuances", width=15)
btn_nuance.pack(pady=5, padx=5)

btn_lignes_trille = ttk.Button(sidebar, text="Lignes/Trilles", width=15)
btn_lignes_trille.pack(pady=5, padx=5)

btn_other_symbole = ttk.Button(sidebar, text="Autre", width=15)
btn_other_symbole.pack(pady=5, padx=5)

btn_user_symbole = ttk.Button(sidebar, text="Symbole utilisateur", width=15)
btn_user_symbole.pack(pady=5, padx=5)

label = ttk.Label(sidebar, text="Propriétés :", anchor="w", justify="left", width=10)
label.pack(fill=X)

selected_value = StringVar()
options = ["4/4", "3/4", "2/4", "6/8", "Autres"]
combobox = ttk.Combobox(sidebar, textvariable=selected_value, values=options, width=5)
combobox.pack(padx=10, pady=10, anchor=N)
combobox.set("")
def on_combobox_change(event):
    selected_option = selected_value.get()
    # print("Option sélectionnée :", selected_option)
combobox.bind("<<ComboboxSelected>>", on_combobox_change)

selected_value = StringVar()
options = ["Ut", "Fa", "Sol"]
combobox = ttk.Combobox(sidebar, textvariable=selected_value, values=options, width=5)
combobox.pack(padx=10, pady=10, anchor=N)
combobox.set("Clé")
def on_combobox_change(event):
    selected_option = selected_value.get()
    # print("Option sélectionnée :", selected_option)
combobox.bind("<<ComboboxSelected>>", on_combobox_change)

btn_new_mesure = ttk.Button(sidebar, text="New mesure", command=new_mesure)
btn_new_mesure.pack(padx=10, pady=10, anchor=N)

# Barre pour définir durée note
toolbar_2 = ttk.Frame(app)
toolbar_2.pack(side=TOP, fill=X)

btn_ronde = ttk.Button(toolbar_2, text="Ronde", width=6)
btn_ronde.pack(side=LEFT, padx=2, pady=2)

btn_blanche = ttk.Button(toolbar_2, text="Blanche", width=6)
btn_blanche.pack(side=LEFT, padx=2, pady=2)

btn_noire = ttk.Button(toolbar_2, text="Noire", width=6)
btn_noire.pack(side=LEFT, padx=2, pady=2)

btn_croche = ttk.Button(toolbar_2, text="Croche", width=6)
btn_croche.pack(side=LEFT, padx=2, pady=2)

btn_double_croche = ttk.Button(toolbar_2, text="Double croche")
btn_double_croche.pack(side=LEFT, padx=2, pady=2)

btn_pointé = ttk.Button(toolbar_2, text="Note pointé")
btn_pointé.pack(side=LEFT, padx=2, pady=2)

btn_diese = ttk.Button(toolbar_2, text="Diese")
btn_diese.pack(side=LEFT, padx=2, pady=2)

btn_bemol = ttk.Button(toolbar_2, text="Bémol")
btn_bemol.pack(side=LEFT, padx=2, pady=2)

btn_note_style = ttk.Button(toolbar_2, text="Style de partition")
btn_note_style.pack(side=RIGHT, padx=2, pady=2)

# affichage partition
toolbar_part = ttk.Frame(app)
toolbar_part.pack(side=TOP, fill=X)

canvas_frame = ttk.Frame(toolbar_part)
canvas_frame.pack(side=RIGHT, fill=BOTH, expand=True)

canvas = Canvas(canvas_frame, width=400, height=150, bg="white")
canvas.pack(side=TOP, fill=BOTH, expand=True)

scrollbar = ttk.Scrollbar(canvas_frame, orient=HORIZONTAL, command=canvas.xview)
scrollbar.pack(side=BOTTOM, fill=X, expand=True)  # Prend toute la largeur disponible
canvas.configure(xscrollcommand=scrollbar.set)

# Fonction pour dessiner une portée
def draw_staff(canvas, x, y, num_staffs):
    staff_width = 200  # Largeur de chaque portée
    spacing = 0  # Espacement entre les portées
    for i in range(num_staffs):
        for j in range(5):
            canvas.create_line(x, y + j * 10, x + staff_width, y + j * 10)
        # Ajouter une ligne verticale pour séparer les mesures
        canvas.create_line(x + staff_width, y, x + staff_width, y + 40)  # Cette ligne sépare chaque mesure
        x += staff_width + spacing  # Augmenter x pour la prochaine portée

canvas.bind("<Button-1>", draw_note)
canvas.bind("<Button-2>", delete_note)

def handle_shortcut(event):
    context_menu2_canvas.post(event.x_root, event.y_root)

context_menu2_canvas = Menu(app, tearoff=0)
context_menu2_canvas.add_command(label="Selections")
context_menu2_canvas.add_command(label="Gomme")
context_menu2_canvas.add_command(label="Loupe")
context_menu2_canvas.add_command(label="Insertion")
context_menu2_canvas.add_command(label="Ciseaux")
context_menu2_canvas.add_command(label="Colle")
context_menu2_canvas.add_command(label="Quantifications")
context_menu2_canvas.add_command(label="Selections sections à exporter")

canvas.bind("<Control-Button-3>", handle_shortcut)

draw_staff(canvas, 50, 50, 3)

notebook = ttk.Notebook(app)

tab1 = ttk.Frame(notebook, width=50)
tab2 = ttk.Frame(notebook, width=50)
tab3 = ttk.Frame(notebook, width=50)
tab4 = ttk.Frame(notebook, width=50)
tab5 = ttk.Frame(notebook, width=50)

# Ajout des onglets au Notebook avec leurs étiquettes
notebook.add(tab1, text="Dessiner")
notebook.add(tab2, text="Clavier virtuel")
notebook.add(tab3, text="Texte")
notebook.add(tab4, text="MIDI")
notebook.add(tab5, text="Decrypter")

# tab1
draw_part = Canvas(tab1, width=400, height=150, bg="white")
draw_part.pack(side="top", fill=BOTH, expand=True)

def draw_staff(draw_part, x, y, num_staffs):
    staff_width = 200  # Largeur de chaque portée
    spacing = 0  # Espacement entre les portées
    for i in range(num_staffs):
        for j in range(5):
            draw_part.create_line(x, y + j * 10, x + staff_width, y + j * 10, fill="black")
        # Ajouter une ligne verticale pour séparer les mesures
        draw_part.create_line(x + staff_width, y, x + staff_width, y + 40, fill="black")  # Cette ligne sépare chaque mesure
        x += staff_width + spacing  # Augmenter x pour la prochaine portée

draw_staff(draw_part, 50, 50, 3)

zoom_plus = ttk.Button(tab1, text="+")
zoom_plus.pack(side="right")

zoom_moin = ttk.Button(tab1, text="-")
zoom_moin.pack(side="right")

label_info = ttk.Label(tab1, text="Le theme ne s'applique pas encore sur la zone de dessin", anchor="w", justify="left", width=10)
label_info.pack(fill=X, side="bottom")

# tab2

clavier_virtuel = ttk.Frame(tab2)
clavier_virtuel.pack(pady=20)

keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
for i, key in enumerate(keys):
    create_key(clavier_virtuel, key, 0, i)

octave_info = ttk.Label(tab2, text="Octave")
octave_info.pack()

octave_config = ttk.Scale(tab2)
octave_config.pack()

# tab3
code_text = scrolledtext.ScrolledText(tab3, wrap=WORD, font=("Courier New", 12), bg="#212121", fg="white")
code_text.pack(expand=True, fill="both")

exe = ttk.Button(tab3, text="Executer le code")
exe.pack()

# tab4
notebook_midi = ttk.Notebook(tab4)

tab_edit = ttk.Frame(notebook_midi, width=50)
tab_tempo = ttk.Frame(notebook_midi, width=50)

notebook_midi.add(tab_edit, text="Editeur")
notebook_midi.add(tab_tempo, text="Editeur de tempo")

# editeur midi
canvas_grid = Canvas(tab_edit, width=780, height=500, bg='white', bd=2, relief=SUNKEN)
canvas_grid.pack()

for i in range(16):
    canvas_grid.create_line(10 + 48 * i, 10, 10 + 48 * i, 510, fill="black")  # lignes verticales
    canvas_grid.create_line(10, 10 + 30 * i, 770, 10 + 30 * i, fill="black")  # lignes horizontales

canvas_grid.bind("<Button-1>", on_grid_click)


notebook_midi.pack(expand=True, fill="both")

# tab5

info_message = ttk.Label(tab5, text="""
Découvrez  les nouvelles fonctionnalités de Dercypter AI sur TEXTA score edit pro 1.0.
""")
info_message.pack()

# image_path = r"C:, "Users, "Family, "Images, "background.png"

# image = Image.open(image_path)
# background_image = ImageTk.PhotoImage(image)

# canvas = tk.Canvas(width=image.width, height=image.height)
# canvas.pack(fill="both", expand=True)
# canvas.create_image(0, 0, image=background_image, anchor="nw")
# label = tk.Label(text="Hello, this is a custom widget!", bg="white")
# ttk.Button = tk.ttk.Button(text="Click Me")
        
# # Placer les widgets sur le canvas
# canvas.create_window(150, 50, window=label)
# canvas.create_window(150, 100, window=ttk.Button)

notebook.pack(expand=True, fill="both")

# Créer un menu principal
menu_logo = tk.Menu(app, bg="#2F2F2F", fg="white", activebackground="#00004B", activeforeground="white")

# Menu Fichier
file_menu = Menu(app, tearoff=0)
file_menu.add_command(label="Ouvrir un projet", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Nouveau projet", command=new_project)
file_menu.add_command(label="Fermer projet", command=close_project)
file_menu.add_command(label="Nouvelle version projet", command=new_version_project)
file_menu.add_command(label="Enregistrer", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Enregistrer sous", command=save_at, accelerator="Ctrl+Maj+S")
file_menu.add_command(label="Imprimer partition", command=print, accelerator="Ctrl+P")
file_menu.add_separator()
file_menu.add_command(label="Mettre la partition en ligne", command=score_online)
file_menu.add_command(label="Créer une video en ligne Partition", command=score_movie)
file_menu.add_separator()
import_menu = Menu(menu_logo, tearoff=0)
import_menu.add_command(label="Fichier audio", command=import_audio)
import_menu.add_command(label="Fichier MIDI", command=import_MIDI)
import_menu.add_command(label="Fichier XML", command=import_xml)
file_menu.add_cascade(label="Importer", menu=import_menu)
export_menu = Menu(menu_logo, tearoff=0)
export_menu.add_command(label="Fichier audio", command=export_audio)
export_menu.add_command(label="Images", command=export_picture)
export_menu.add_command(label="Fichier PDF", command=export_pdf)
export_menu.add_command(label="Fichier MIDI", command=export_midi)
export_menu.add_command(label="Fichier XML", command=export_xml)
file_menu.add_cascade(label="Exporter", menu=export_menu)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=exit_app, accelerator="Alt+F4")
menu_logo.add_cascade(label="Fichier", menu=file_menu)

# Menu Édition
edit_menu = Menu(app, tearoff=0)
edit_menu.add_command(label="Annuler", command=annule, accelerator="Ctrl+Z")
edit_menu.add_command(label="Rétablir", command=retablir, accelerator="Ctrl+Y")
edit_menu.add_command(label="Historique", command=aff_historique)
edit_menu.add_separator()
edit_menu.add_command(label="Copier", command=cut, accelerator="Ctrl+C")
edit_menu.add_command(label="Couper", command=copy, accelerator="Ctrl+X")
edit_menu.add_command(label="Coller", command=coly, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Sélectionner", command=select)
edit_menu.add_command(label="Tout sélectionner", command=all_select, accelerator="Ctrl+A")
edit_menu.add_command(label="Rechercher / Remplacer", command=shearch)
edit_menu.add_command(label="Réorganiser", command=reorganize)
edit_menu.add_command(label="Mesure automatique", command=mesure_auto)
edit_menu.add_command(label="Annotation perfommance", command=annotation_perfomant)
menu_logo.add_cascade(label="Édition", menu=edit_menu)

# Menu MIDI
midi_menu = Menu(app, tearoff=0)
midi_menu.add_command(label="Ouvrir éditeur clavier", accelerator="F2", command=open_midi_edit)
midi_menu.add_command(label="Ouvrir éditeur rythme", accelerator="F3", command=open_rythme_edit)
midi_menu.add_command(label="Ouvrir éditeur clavier sur partition", accelerator="Ctrl+F2", command=open_midi_edit_on_score)
midi_menu.add_command(label="Editeur de contrôle", command=open_control_edit)
midi_menu.add_command(label="Enregistrement MIDI", command=saved_midi)
midi_menu.add_separator()
midi_menu.add_command(label="Transposer", command=transpose)
midi_menu.add_command(label="Paramètres MIDI", command=setting_midi)
menu_logo.add_cascade(label="MIDI", menu=midi_menu)

# Menu Projet
project_menu = Menu(app, tearoff=0)
project_menu.add_command(label="Nouvelle partition", accelerator="Ctrl+N", command=new_partition)
project_menu.add_command(label="Dupliquer partition", command=duplic_part)
project_menu.add_command(label="Nouvelle version partition", command=new_version_score)
project_menu.add_command(label="Supprimer partition", accelerator="Delete", command=delete_score)
project_menu.add_command(label="Supprimer toutes les partitions vides", accelerator="Ctrl+Delete", command=delete_vierge_scores)
project_menu.add_separator()
project_menu.add_command(label="Bibliothèque", command=bibilotheque)
project_menu.add_command(label="Marqueurs", command=marqueurs)
project_menu.add_command(label="Explorateur", command=explorer)
project_menu.add_command(label="Calculatrice de tempo", command=calc_tempo)
project_menu.add_command(label="Timecode curseur", command=timecode_curseur)
project_menu.add_command(label="Bloc-notes", command=notepad)
menu_logo.add_cascade(label="Projet", menu=project_menu)

# Menu Déchiffrer
decrypt_menu = Menu(app, tearoff=0)
decrypt_menu.add_command(label="Déchiffrer fichier audio", command=decrypt_audio)
decrypt_menu.add_command(label="Déchiffrer MIDI en direct", command=decrypt_midi_live)
decrypt_menu.add_command(label="Déchiffrer fichier MIDI", command=decrypt_midi)
decrypt_menu.add_command(label="Déchiffrer enregistrement audio", command=decrypt_audio_saved)
decrypt_menu.add_separator()
decrypt_menu.add_command(label="Annalyse harmonique", command=harmonic_annaliser)
decrypt_menu.add_command(label="Annalyse tonnalité", command=tonn_annalyse)
decrypt_menu.add_command(label="Scan partition decryption", command=Scan_partition_decryption)
decrypt_menu.add_command(label="Correcteur de la hauteur", command=hauteur_correction)
menu_logo.add_cascade(label="Déchiffrer", menu=decrypt_menu)

# Menu Partition
score_menu = Menu(app, tearoff=0)
score_menu.add_command(label="Options partition", command=partition_option)
score_menu.add_separator()
score_menu.add_checkbutton(label="Mode page", command=page_mode)
score_menu.add_separator()
score_menu.add_command(label="Grouper / dégrouper notes")
score_menu.add_command(label="Convertir en note d'ornement")
score_menu.add_command(label="Définir N-olet")
score_menu.add_command(label="Éclatement")
score_menu.add_separator()
score_menu.add_command(label="Mélanger les portées")
score_menu.add_command(label="Extraire voix")
score_menu.add_command(label="Insérer Legato")
score_menu.add_command(label="Montrer / Cacher")
score_menu.add_command(label="Inverser")
menu_logo.add_cascade(label="Partition", menu=score_menu)

# Menu Options
options_menu = Menu(app, tearoff=0)
options_menu.add_command(label="Préférences")
options_menu.add_command(label="Raccourcis clavier")
options_menu.add_command(label="Thèmes", command=change_theme)
options_menu.add_command(label="Personnaliser")
options_menu.add_command(label="Langue")
options_menu.add_command(label="Mise à jour autommatique (Selon abbonement)")
options_menu.add_command(label="Sauvgarde autommatique")
options_menu.add_command(label="Integrations externes")
menu_logo.add_cascade(label="Options", menu=options_menu)

# Menu Aide
help_menu = Menu(app, tearoff=0)
help_menu.add_command(label="Documentations", accelerator="F1", command=open_doc)
help_menu.add_command(label="Aide sur le site TEXTA music")
help_menu.add_command(label="Foire aux questions")
help_menu.add_separator()
help_menu.add_command(label="Crédits")
help_menu.add_command(label="À propos de TEXTA SM edit")
menu_logo.add_cascade(label="?", menu=help_menu)


label_tx.bind("<Button-1>", xpanel_menu)

# menu (clic droit)
# Barre d'outil
context_menu_toolbar = Menu(app, tearoff=0)
context_menu_toolbar.add_checkbutton(label="Outils")
context_menu_toolbar.add_checkbutton(label="Modificateur de notes")
context_menu_toolbar.add_checkbutton(label="Quantifications")

toolbar.bind("<Button-3>", show_context_menu_toolbar)

# parti1tion
context_menu_canvas = Menu(app, tearoff=0)
context_menu_canvas.add_command(label="Nouvelle mesure")
sub_context_menu_canvas = Menu(app, tearoff=0)
sub_context_menu_canvas.add_command(label="Selections")
sub_context_menu_canvas.add_command(label="Gomme")
sub_context_menu_canvas.add_command(label="Loupe")
sub_context_menu_canvas.add_command(label="Insertion")
sub_context_menu_canvas.add_command(label="Ciseaux")
sub_context_menu_canvas.add_command(label="Colle")
sub_context_menu_canvas.add_command(label="Quantifications")
sub_context_menu_canvas.add_command(label="Selections sections à exporter")
context_menu_canvas.add_cascade(label="Outils", menu=sub_context_menu_canvas)

canvas.bind("<Button-3>", show_context_menu_canvas)

# Onglets

context_menu_notebook = Menu(app, tearoff=0)
context_menu_notebook.add_checkbutton(label="Masquer les onglets", command=masque_onglet)
context_menu_notebook.add_command(label="Type d'affichage")

notebook.bind("<Button-3>", show_context_menu_notebook)

set_dark_theme()

app.mainloop()