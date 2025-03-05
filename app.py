import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QScrollArea, QComboBox, QMenu, QLineEdit, QMainWindow, QFrame, QPushButton, QButtonGroup, QRadioButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, QLabel, QTabWidget, QSlider, QSizePolicy, QDialog, QColorDialog, QSpinBox, QGroupBox, QCheckBox, QFontComboBox, QProgressDialog, QSpacerItem, QToolBox, QGraphicsOpacityEffect
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize, QPropertyAnimation, QFile, QRect, QEasingCurve
from PyQt5.QtWidgets import QFileDialog

class MidiGridEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.grid_size = 20  # Taille de chaque case de la grille (en pixels)
        self.columns = 100  # Nombre de colonnes (représentant le temps)
        self.rows = 12  # Nombre de lignes (représentant les hauteurs de note)
        self.notes = []  # Liste pour stocker les notes ajoutées

        # Layout principal
        main_layout = QVBoxLayout()

        # Créer la grille d'édition
        self.grid_widget = Grid(self.grid_size, self.columns, self.rows)
        main_layout.addWidget(self.grid_widget)

        # Boutons pour effacer les notes
        controls_layout = QHBoxLayout()
        self.clear_button = QPushButton("Effacer les notes")
        self.clear_button.clicked.connect(self.clear_notes)
        controls_layout.addWidget(self.clear_button)

        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

    def clear_notes(self):
        """Efface toutes les notes de la grille."""
        self.grid_widget.clear_grid()

class Grid(QWidget):
    def __init__(self, grid_size, columns, rows):
        super().__init__()
        self.grid_size = grid_size
        self.columns = columns
        self.rows = rows
        self.notes = []

        self.setMinimumSize(self.columns * self.grid_size, self.rows * self.grid_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(200, 200, 200), 1, Qt.SolidLine)
        painter.setPen(pen)

        # Dessiner la grille
        for col in range(self.columns):
            for row in range(self.rows):
                rect = QRect(col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size)
                painter.drawRect(rect)

        # Dessiner les notes
        pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)
        painter.setPen(pen)
        for note in self.notes:
            painter.fillRect(note, QColor(100, 200, 100))

    def mousePressEvent(self, event):
        """Ajouter ou retirer une note à la grille."""
        x = event.x() // self.grid_size
        y = event.y() // self.grid_size

        rect = QRect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
        
        if rect in self.notes:
            self.notes.remove(rect)  # Retirer la note si elle est déjà présente
        else:
            self.notes.append(rect)  # Ajouter la note

        self.update()

    def clear_grid(self):
        """Effacer toutes les notes de la grille."""
        self.notes.clear()
        self.update()

class MidiTab(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QVBoxLayout()

        # Ajouter l'éditeur MIDI sur grille
        self.midi_grid_editor = MidiGridEditor()
        main_layout.addWidget(self.midi_grid_editor)

        self.setLayout(main_layout)

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.measure_positions = [QPoint(50, 50)]  # Première mesure par défaut
        self.num_staff_lines = 5  # Nombre de lignes dans la portée
        self.measure_width = 200  # Largeur de chaque mesure
        self.staff_spacing = 40   # Espacement entre les portées

        self.clef = 'sol'
        self.accidentals = []
        self.notes = []

        self.current_measure_note_value = 0

    def set_time_signature(self, beats, note_value):
        """Definir la signature temporelle; exemple (4, 4) pour 4/4"""
        self.time_signature = (beats, note_value)
        self.update()

    def load_canvas_data(self, data):
        """Charger les données du fichier dans le canvas."""
        self.clef = data.get("clef", None)
        self.accidentals = data.get("accidentals", [])
        self.measure_positions = [QPoint(measure["position"]["x"], measure["position"]["y"]) for measure in data.get("measures", [])]
        self.notes = []

        # Charger les notes dans chaque mesure
        for measure in data.get("measures", []):
            for note in measure["notes"]:
                position = QPoint(note["position"]["x"], note["position"]["y"])
                self.notes.append({'position': position, 'type': note["type"]})

        # Forcer la mise à jour du canvas pour redessiner
        self.update()

    def get_canvas_data(self):
        """Récupère toutes les données du canvas pour les sauvegarder."""
        data = {
            "clef": self.clef,
            "accidentals": self.accidentals,
            "measures": []
        }
        
        # Créer une liste des mesures avec leurs notes
        for measure in self.measure_positions:
            # Filtrer les notes correspondant à cette mesure
            measure_notes = [note for note in self.notes if note['position'].x() > measure.x()]
            
            # Ajouter la mesure et ses notes
            data["measures"].append({
                "position": measure,
                "notes": measure_notes
            })

        return data

    def set_clef(self, clef_type):
        """Définir la clé (clé de sol, clé de fa, etc.)."""
        self.clef = clef_type
        self.update()

    def add_accidental(self, accidental_type):
        """Ajouter une altération (dièse, bémol)."""
        self.accidentals.append(accidental_type)
        self.update()

    def add_measure(self):
        last_measure = self.measure_positions[-1]
        new_measure_x = last_measure.x() + self.measure_width + 10  # Ajouter une petite marge
        self.measure_positions.append(QPoint(new_measure_x, 50))
        self.update()

    def add_note(self, note_type, position):
        """Ajouter une note avec un type (noire, blanche, etc.)."""
        note_value = self.get_note_value(note_type)
        
        # Initialiser la signature temporelle si elle n'existe pas
        if not hasattr(self, 'time_signature'):
            self.time_signature = (4, 4)  # Par défaut à 4/4 si aucune signature temporelle n'est définie
        
        # Vérifier si l'ajout de cette note dépasse la mesure actuelle
        if self.current_measure_note_value + note_value <= self.time_signature[0]:
            self.notes.append({'position': position, 'type': note_type})
            self.current_measure_note_value += note_value  # Mettre à jour la valeur des notes de la mesure
            self.update()
        else:
            print("La mesure est déjà remplie selon la signature temporelle.")

    def get_note_value(self, note_type):
        note_values = {
            'ronde' : 1,
            'blanche' : 0.5,
            'noire' : 0.25,
            'croche' : 0.125,
            'doubleCroche' : 0.0625,
            'quatrupleCroche' : 0.03125,
        }
        return note_values.get(note_type, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dessiner la portée à une position donnée (par exemple 50, 50)
        self.draw_staff(painter, 50, 50)  # Vous pouvez ajuster x et y ici

        # Dessiner la clé de sol
        if self.clef:
            self.draw_clef(painter, self.clef)

        # Dessiner les altérations
        self.draw_accidentals(painter)

        # Dessiner les notes
        self.draw_notes(painter)

        # Dessiner les barres de mesure
        for position in self.measure_positions:
            self.draw_staff(painter, position.x(), position.y(), self.num_staff_lines)

    def draw_staff(self, painter, x, y, num_lines=5, line_spacing=10):
        """Dessiner les lignes de la portée."""
        for i in range(num_lines):
            y_pos = y + i * line_spacing
            painter.drawLine(x, y_pos, x + self.measure_width, y_pos)  # Lignes horizontales de la portée

        # Séparer les mesures avec une ligne verticale
        painter.drawLine(x + self.measure_width, y, x + self.measure_width, y + (num_lines - 1) * line_spacing)

    def draw_clef(self, painter, clef_type):
        """Dessiner la clé (Sol, Fa, etc.)."""
        font = QFont('Times', 30)
        painter.setFont(font)

        if clef_type == 'sol':
            painter.drawText(60, 85, '𝄞')  # Clé de Sol
        elif clef_type == 'fa':
            painter.drawText(60, 85, '𝄢')  # Clé de Fa

    def draw_accidentals(self, painter):
        """Dessiner les altérations (dièses, bémols) sur la portée."""
        font = QFont('Times', 20)
        painter.setFont(font)

        x = 100
        for accidental in self.accidentals:
            if accidental == '#':
                painter.drawText(x, 65, '#')  # Dièse
            elif accidental == 'b':
                painter.drawText(x, 65, '♭')  # Bémol
            x += 20

    def draw_notes(self, painter):
        """Dessiner les notes sur la portée."""
        for note in self.notes:
            position = note['position']
            note_type = note['type']

            # Sélectionner l'image de la note en fonction de son type
            if note_type == 'noire':
                note_image = QImage("IconApp/objets_canvas/noire.png")
            elif note_type == 'blanche':
                note_image = QImage("IconApp/objets_canvas/blanche.png")
            elif note_type == 'ronde':
                note_image = QImage("IconApp/objets_canvas/ronde.png")

            # Redimensionner l'image avant de la dessiner
            note_image = note_image.scaled(96, 64)
            painter.drawImage(position, note_image)

    def draw_measures(self, painter):
        """Dessiner les barres de mesure."""
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)

        for measure in self.measure_positions:
            painter.drawLine(measure.x(), 50, measure.x(), 90)

    def mousePressEvent(self, event):
        """Ajouter une note en cliquant sur la portée."""
        if event.button() == Qt.LeftButton:
            mouse_x = event.x()
            mouse_y = event.y()
            closest_y = self.get_closest_line(mouse_y)

            # Ajouter une note noire à la position cliquée
            self.add_note('noire', QPoint(mouse_x, closest_y))

    def get_closest_line(self, y):
        """Trouver la ligne la plus proche sur la portée."""
        top_margin = 50
        line_spacing = 10
        # closest_line = round((y - top_margin) / line_spacing) * line_spacing + top_margin
        # return closest_line
        return round((y - top_margin) / line_spacing) * line_spacing + top_margin

    def resizeEvent(self, event):
        """Mettre à jour la taille du canvas en fonction des mesures."""
        if self.measure_positions:
            total_width = self.measure_positions[-1].x() + 150  # Largeur totale en fonction des mesures
            self.setFixedWidth(max(self.width(), total_width))  # Ajuste la largeur minimale du canvas
    
class ScoreEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Supprimer un layout existant s'il y en a un
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        # Création du layout principal
        main_layout = QVBoxLayout()

        # Création du canvas (doit être définie avant de l'utiliser)
        self.canvas = Canvas()

        # Zone de défilement pour le canvas
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.canvas)
        scroll_area.setWidgetResizable(True)

        # Créer une frame pour contenir les boutons et autres contrôles
        self.frame = QFrame()
        self.frame.setStyleSheet("""
        QFrame {
            padding: 3px;
        }
        """)
        frame_layout = QHBoxLayout(self.frame)

        # ComboBox pour sélectionner la clé
        self.clef_combo = QComboBox()
        self.clef_combo.addItems(["Clé de Sol", "Clé de Fa", "Clé d'Ut"])
        self.clef_combo.currentIndexChanged.connect(self.change_clef)
        frame_layout.addWidget(self.clef_combo, alignment=Qt.AlignLeft)

        # ComboBox pour sélectionner le temps
        self.time_signature_combo = QComboBox()
        self.time_signature_combo.addItems(["4/4", "3/4", "2/4", "6/8"])
        self.time_signature_combo.currentIndexChanged.connect(self.change_time_signature)
        frame_layout.addWidget(self.time_signature_combo, alignment=Qt.AlignLeft)

        # ComboBox pour sélectionner le type de note
        self.note_type_combo = QComboBox()
        self.note_type_combo.addItems(["Noire", "Blanche", "Ronde"])
        self.note_type_combo.currentIndexChanged.connect(self.change_note_type)
        frame_layout.addWidget(self.note_type_combo, alignment=Qt.AlignLeft)

        # Bouton pour ajouter une mesure
        measure_button = QPushButton("Ajouter mesure")
        measure_button.clicked.connect(self.canvas.add_measure)
        frame_layout.addWidget(measure_button, alignment=Qt.AlignLeft)

        # Création d'un groupe de boutons pour le comportement exclusif
        button_group = QButtonGroup(self)
        button_group.setExclusive(True)

        # Fonction pour gérer la sélection d'un bouton
        def on_button_clicked(button):
            for b in button_group.buttons():
                b.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(175, 175, 175);
                        border-radius: 10px;
                        min-width: 20px;
                        min-height: 20px;
                    }
                """)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgb(150, 150, 250);
                    border-radius: 10px;
                    min-width: 20px;
                    min-height: 20px;
                }
            """)

        # Création des QPushButton avec des icônes uniquement
        select_button = QPushButton()
        select_button.setIcon(QIcon("IconApp/Toolbar/selections.png"))
        select_button.setIconSize(QSize(20, 20))
        select_button.setCheckable(True)  # Rendre le bouton "checkable"
        select_button.clicked.connect(lambda: on_button_clicked(select_button))
        frame_layout.addWidget(select_button, alignment=Qt.AlignLeft)

        insert_button = QPushButton()
        insert_button.setIcon(QIcon("IconApp/Toolbar/insertions.png"))
        insert_button.setIconSize(QSize(20, 20))
        insert_button.setCheckable(True)  # Rendre le bouton "checkable"
        insert_button.clicked.connect(lambda: on_button_clicked(insert_button))
        frame_layout.addWidget(insert_button, alignment=Qt.AlignLeft)

        delet_button = QPushButton()
        delet_button.setIcon(QIcon("IconApp/Toolbar/gomme.png"))
        delet_button.setIconSize(QSize(20, 20))
        delet_button.setCheckable(True)  # Rendre le bouton "checkable"
        delet_button.clicked.connect(lambda: on_button_clicked(delet_button))
        frame_layout.addWidget(delet_button, alignment=Qt.AlignLeft)

        colle_button = QPushButton()
        colle_button.setIcon(QIcon("IconApp/Toolbar/colle.png"))
        colle_button.setIconSize(QSize(20, 20))
        colle_button.setCheckable(True)  # Rendre le bouton "checkable"
        colle_button.clicked.connect(lambda: on_button_clicked(colle_button))
        frame_layout.addWidget(colle_button, alignment=Qt.AlignLeft)

        coupe_button = QPushButton()
        coupe_button.setIcon(QIcon("IconApp/Toolbar/ciseaux.png"))
        coupe_button.setIconSize(QSize(20, 20))
        coupe_button.setCheckable(True)  # Rendre le bouton "checkable"
        coupe_button.clicked.connect(lambda: on_button_clicked(coupe_button))
        frame_layout.addWidget(coupe_button, alignment=Qt.AlignLeft)

        # Ajouter les boutons au groupe
        button_group.addButton(select_button)
        button_group.addButton(insert_button)
        button_group.addButton(delet_button)
        button_group.addButton(colle_button)
        button_group.addButton(coupe_button)

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)  # Définir la ligne verticale
        separator_line.setFrameShadow(QFrame.Plain)  # Effet de la ligne
        frame_layout.addWidget(separator_line)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        frame_layout.addSpacerItem(spacer)

        # Ajouter la frame au layout principal
        main_layout.addWidget(self.frame)

        # Ajouter le canvas et la zone de défilement dans le layout principal
        main_layout.addWidget(scroll_area)

        # Appliquer le layout principal
        self.setLayout(main_layout)

        # Variables pour la clé, la signature temporelle, et le type de note sélectionnés
        self.selected_clef = 'sol'
        self.selected_time_signature = '4/4'
        self.selected_note_type = 'noire'

    def change_clef(self):
        """Changer la clé en fonction de la sélection."""
        clef = self.clef_combo.currentText()
        if clef == "Clé de Sol":
            self.canvas.set_clef('sol')
        elif clef == "Clé de Fa":
            self.canvas.set_clef('fa')
        elif clef == "Clé d'Ut":
            self.canvas.set_clef('ut')

    def change_time_signature(self):
        """Changer la signature temporelle."""
        self.selected_time_signature = self.time_signature_combo.currentText()

        # Diviser la signature temporelle en battements et valeur de note
        beats, note_value = map(int, self.selected_time_signature.split("/"))
        self.canvas.set_time_signature(beats, note_value)

    def change_note_type(self):
        """Changer le type de note en fonction de la sélection."""
        self.selected_note_type = self.note_type_combo.currentText()

class DecryptTab(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal horizontal (paramètres à gauche, convertisseur à droite)
        main_layout = QHBoxLayout()

        # Paramètres d'analyse (à gauche)
        params_layout = QVBoxLayout()
        params_label = QLabel("Paramètres d'analyse de partition:")
        
        # Entrée pour la durée des notes
        self.note_duration_input = self.create_input_field("Durée des notes (ms)")

        # Entrée pour le tempo
        self.tempo_input = self.create_input_field("Tempo (BPM)")

        # Entrée pour la précision de la détection des notes
        self.pitch_detection_input = self.create_input_field("Précision de la détection des notes (%)")

        # Ajouter les widgets des paramètres au layout
        params_layout.addWidget(params_label)
        params_layout.addWidget(self.note_duration_input)
        params_layout.addWidget(self.tempo_input)
        params_layout.addWidget(self.pitch_detection_input)
        params_layout.addStretch()

        # Convertisseur d'audio en partition (à droite) 
        convert_layout = QVBoxLayout()
        convert_label = QLabel("Convertir de l'audio en partition:")

        # Entrée pour le fichier audio
        self.audio_file_input = QTextEdit()
        self.audio_file_input.setPlaceholderText("Chemin du fichier audio...")
        self.audio_file_input.setFixedHeight(40)  # Limiter la hauteur de l'entrée texte

        # Bouton pour ouvrir la boîte de dialogue de sélection de fichier
        self.select_audio_button = QPushButton("Sélectionner un fichier audio")
        self.select_audio_button.clicked.connect(self.open_file_dialog)
        
        # Bouton pour convertir l'audio en partition
        self.convert_button = QPushButton("Convertir en partition")
        self.convert_button.clicked.connect(self.convert_audio_to_score)

        # Ajouter les widgets du convertisseur au layout
        convert_layout.addWidget(convert_label)
        convert_layout.addWidget(self.audio_file_input)
        convert_layout.addWidget(self.select_audio_button)
        convert_layout.addWidget(self.convert_button)
        convert_layout.addStretch()

        # Ajouter les layouts des paramètres et du convertisseur au layout principal
        main_layout.addLayout(params_layout)
        main_layout.addLayout(convert_layout)

        self.setLayout(main_layout)

    def create_input_field(self, label_text):
        # Crée un champ de saisie avec un label
        layout = QVBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(input_field)
        container = QWidget()
        container.setLayout(layout)
        return container

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier audio", "", "Fichiers audio (*.mp3 *.wav *.flac);;Tous les fichiers (*)")
        
        if file_name:
            # Si un fichier est sélectionné, mettre à jour le champ texte avec le chemin du fichier
            self.audio_file_input.setPlainText(file_name)

    def convert_audio_to_score(self):
        audio_path = self.audio_file_input.toPlainText()
        note_duration = self.note_duration_input.findChild(QLineEdit).text()
        tempo = self.tempo_input.findChild(QLineEdit).text()
        pitch_detection = self.pitch_detection_input.findChild(QLineEdit).text()

        # Vérification du fichier audio
        if os.path.exists(audio_path):
            # Ici tu pourrais ajouter la vraie logique de conversion
            print(f"Conversion du fichier audio {audio_path} avec:")
            print(f"- Durée des notes: {note_duration} ms")
            print(f"- Tempo: {tempo} BPM")
            print(f"- Précision de détection des notes: {pitch_detection}%")
        else:
            print("Le fichier audio spécifié n'existe pas, vérifiez l'hortographe du répertoire.")

class VirtualKeyboard(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        layout = QVBoxLayout()

        # Clavier virtuel (section des touches de piano)
        self.keyboard_layout = QHBoxLayout()

        # Créer les touches du clavier (do, ré, mi, etc.)
        self.create_keyboard()

        # Ajouter le clavier virtuel au layout principal
        layout.addLayout(self.keyboard_layout)

        self.setLayout(layout)

    def create_keyboard(self):
        """Crée des boutons représentant les touches d'un piano."""
        keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']  # Notes de base
        self.buttons = {}  # Dictionnaire pour stocker les boutons

        for key in keys:
            btn = QPushButton(key)
            btn.setFixedSize(50, 100)
            btn.setStyleSheet("background-color: white;")  # Blanche pour les touches naturelles

            # Connecter chaque bouton à la méthode qui gère les clics
            btn.clicked.connect(lambda checked, k=key: self.on_key_pressed(k))

            # Ajouter le bouton au layout du clavier
            self.keyboard_layout.addWidget(btn)
            self.buttons[key] = btn

    def on_key_pressed(self, key):
        """Gère l'ajout d'une note à la partition lorsqu'une touche est pressée."""
        self.parentWidget().add_note_to_score(key)

class ManualScoreEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QVBoxLayout()

        # Zone d'édition de la partition
        self.canvas = Canvas()

        # Clavier virtuel pour saisir les notes
        self.virtual_keyboard = VirtualKeyboard()

        # Ajouter les widgets au layout
        main_layout.addWidget(self.virtual_keyboard)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

    def add_note_to_score(self, note):
        """Ajoute la note correspondante à la partition."""
        # Par exemple, la position pourrait être calculée automatiquement
        # en fonction de la dernière note ou une position par défaut
        self.canvas.add_note(note)

class ThemeDialog(QDialog):
    def __init__(self, parent=None):
        """theme_dialog [summary]

        Args:
            parent (QfileDialog, optional): widget config. theme. Defaults to None.
        """
        super(ThemeDialog, self).__init__(parent)
        
        self.setWindowTitle("Personnalisation du Thème")
        
        # Initialisation des variables
        self.bg_color = "#FFFFFF"
        self.text_color = "#000000"
        self.button_color = "#0078D4"
        self.border_color = "#CCCCCC"
        self.font_family = "Arial"
        self.font_size = 12
        self.opacity = 1.0
        self.rounded_borders = False
        self.button_shadow = False
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Section pour le choix du thème
        theme_group = QGroupBox("Sélectionner un thème", self)
        theme_layout = QVBoxLayout(theme_group)
        
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Thème Clair", "styles/style.css")
        self.comboBox.addItem("Thème Sombre", "styles/style_2.css")
        self.comboBox.addItem("Thème Coloré", "styles/style_3.css")
        self.comboBox.addItem("Thème Compacte", "styles/style_4.css")
        self.comboBox.addItem("Thème Glass", "styles/style_5.css")
        self.comboBox.addItem("Thème OS", "styles/vide.css")

        self.apply_button = QPushButton("Appliquer")
        self.apply_button.clicked.connect(self.apply_theme)
        
        theme_layout.addWidget(self.comboBox)
        theme_layout.addWidget(self.apply_button)
        
        # Ajouter la section thème au layout principal
        layout.addWidget(theme_group)
        
        # Section de personnalisation des couleurs
        color_group = QGroupBox("Personnaliser les couleurs", self)
        color_layout = QVBoxLayout(color_group)
        
        self.btn_color_bg = QPushButton("Choisir la couleur du fond", self)
        self.btn_color_text = QPushButton("Choisir la couleur du texte", self)
        self.btn_color_button = QPushButton("Choisir la couleur des boutons", self)
        self.btn_color_border = QPushButton("Choisir la couleur des bordures", self)
        
        self.btn_color_bg.clicked.connect(lambda: self.select_color('bg'))
        self.btn_color_text.clicked.connect(lambda: self.select_color('text'))
        self.btn_color_button.clicked.connect(lambda: self.select_color('button'))
        self.btn_color_border.clicked.connect(lambda: self.select_color('border'))
        
        color_layout.addWidget(self.btn_color_bg)
        color_layout.addWidget(self.btn_color_text)
        color_layout.addWidget(self.btn_color_button)
        color_layout.addWidget(self.btn_color_border)
        
        # Ajouter la section de personnalisation des couleurs
        layout.addWidget(color_group)
        
        # Section pour la police
        font_group = QGroupBox("Personnaliser la police", self)
        font_layout = QVBoxLayout(font_group)
        
        self.font_combo = QFontComboBox(self)
        self.font_size_spin = QSpinBox(self)
        self.font_size_spin.setRange(8, 36)
        self.font_size_spin.setValue(12)
        
        font_layout.addWidget(QLabel("Sélectionner la police:"))
        font_layout.addWidget(self.font_combo)
        font_layout.addWidget(QLabel("Taille de la police:"))
        font_layout.addWidget(self.font_size_spin)
        
        self.font_combo.currentFontChanged.connect(self.update_font)
        self.font_size_spin.valueChanged.connect(self.update_font_size)
        
        # Ajouter la section de personnalisation de la police
        layout.addWidget(font_group)
        
        # Section pour les bordures des boutons et champs de texte
        border_group = QGroupBox("Personnaliser les bordures", self)
        border_layout = QVBoxLayout(border_group)
        
        self.border_size_spin = QSpinBox(self)
        self.border_size_spin.setRange(0, 10)
        self.border_size_spin.setValue(1)
        
        self.border_checkbox = QCheckBox("Ajouter des bordures arrondies", self)
        self.border_checkbox.stateChanged.connect(self.toggle_rounded_borders)
        
        self.border_color_btn = QPushButton("Choisir la couleur des bordures", self)
        self.border_color_btn.clicked.connect(lambda: self.select_color('border'))

        border_layout.addWidget(QLabel("Taille des bordures:"))
        border_layout.addWidget(self.border_size_spin)
        border_layout.addWidget(self.border_checkbox)
        border_layout.addWidget(self.border_color_btn)
        
        # Ajouter la section de personnalisation des bordures
        layout.addWidget(border_group)
        
        # Section pour l'ombre des boutons
        shadow_group = QGroupBox("Personnaliser l'ombre des boutons", self)
        shadow_layout = QVBoxLayout(shadow_group)
        
        self.shadow_checkbox = QCheckBox("Activer l'ombre des boutons", self)
        self.shadow_checkbox.stateChanged.connect(self.toggle_button_shadow)
        
        shadow_layout.addWidget(self.shadow_checkbox)
        
        # Ajouter la section de personnalisation de l'ombre des boutons
        layout.addWidget(shadow_group)
        
        # Section pour la transparence
        opacity_group = QGroupBox("Opacité de l'interface", self)
        opacity_layout = QVBoxLayout(opacity_group)
        
        self.opacity_spin = QSpinBox(self)
        self.opacity_spin.setRange(0, 100)
        self.opacity_spin.setValue(100)
        self.opacity_spin.valueChanged.connect(self.update_opacity)
        
        opacity_layout.addWidget(QLabel("Opacité (%) :"))
        opacity_layout.addWidget(self.opacity_spin)
        
        # Ajouter la section de transparence
        layout.addWidget(opacity_group)
        
        # Appliquer les personnalisations
        apply_custom_button = QPushButton("Appliquer les personnalisations", self)
        apply_custom_button.clicked.connect(self.apply_custom_theme)
        
        layout.addWidget(apply_custom_button)
    
    def select_color(self, element):
        """Permet de sélectionner une couleur et de l'appliquer au bon élément."""
        color = QColorDialog.getColor()
        if color.isValid():
            if element == 'bg':
                self.bg_color = color.name()
                self.btn_color_bg.setStyleSheet(f"background-color: {self.bg_color};")
            elif element == 'text':
                self.text_color = color.name()
                self.btn_color_text.setStyleSheet(f"background-color: {self.text_color};")
            elif element == 'button':
                self.button_color = color.name()
                self.btn_color_button.setStyleSheet(f"background-color: {self.button_color};")
            elif element == 'border':
                self.border_color = color.name()
    
    def update_font(self):
        """Met à jour la police en fonction du choix de l'utilisateur."""
        self.font_family = self.font_combo.currentFont().family()
    
    def update_font_size(self):
        """Met à jour la taille de la police en fonction du SpinBox."""
        self.font_size = self.font_size_spin.value()

    def update_opacity(self):
        """Met à jour l'opacité des éléments."""
        self.opacity = self.opacity_spin.value() / 100.0

    def toggle_rounded_borders(self):
        """Active ou désactive les bordures arrondies."""
        self.rounded_borders = self.border_checkbox.isChecked()

    def toggle_button_shadow(self):
        """Active ou désactive l'ombre des boutons."""
        self.button_shadow = self.shadow_checkbox.isChecked()

    def apply_custom_theme(self):
        """Applique toutes les personnalisations à l'application."""
        css = f"""
        QMainWindow {{
            background-color: {self.bg_color};
            opacity: {self.opacity};
        }}
        QLabel {{
            color: {self.text_color};
            font-family: {self.font_family};
            font-size: {self.font_size}px;
        }}
        QPushButton {{
            background-color: {self.button_color};
            border: {self.border_size_spin.value()}px solid {self.border_color};
            font-family: {self.font_family};
            font-size: {self.font_size}px;
            border-radius: {"5px" if self.rounded_borders else "0px"};
            {'box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);' if self.button_shadow else ''}
        }}
        QLineEdit {{
            border: {self.border_size_spin.value()}px solid {self.border_color};
            font-family: {self.font_family};
            font-size: {self.font_size}px;
        }}
        """
        QApplication.instance().setStyleSheet(css)

    def apply_theme(self):
        """Charge et applique le style du fichier sélectionné."""
        qss_file = self.comboBox.currentData()
        self.load_qss(qss_file)
        
    def load_qss(self, qss_file):
        """Charge le fichier QSS et applique le style à l'application."""
        file = QFile(qss_file)
        if file.open(QFile.ReadOnly | QFile.Text):
            qss = file.readAll().data().decode()
            QApplication.instance().setStyleSheet(qss)
        file.close()

class OptionsBar(QWidget):
    def __init__(self, canvas, parent=None, main_window=None):
        super(OptionsBar, self).__init__(parent)
        # self.setFixedHeight(30)

        self.canvas = canvas
        self.main_window = main_window

        self.menu_button = QPushButton("Options", self)
        self.menu_button.clicked.connect(self.show_menu)

        # Connecter les boutons à des fonctions de la fenêtre principale

        self.play_button = QPushButton("Lire la partition")
        self.play_button.clicked.connect(self.ScorePlayer)

        self.help_button = QPushButton("Aide")
        self.help_button.clicked.connect(self.main_window.toggle_help_sidebar)
        self.help_button.setShortcut('F1')

        self.acount_button = QPushButton("Compte")
        self.acount_button.clicked.connect(self.main_window.toggle_acount_sidebar)
        self.acount_button.setShortcut('Alt+C')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.acount_button)
        button_layout.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.addWidget(self.menu_button)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.setContentsMargins(5, 0, 5, 0)
        
        self.setLayout(layout)

        self.setMouseTracking(True)

        self.is_dragging = False

        self.maximized = False

    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(500)  # Durée de l'animation en millisecondes
        animation.setStartValue(button.geometry())
        animation.setEndValue(button.geometry().adjusted(0, 0, 10, 10))  # Par exemple, agrandir légèrement le bouton
        animation.setEasingCurve(QEasingCurve.OutBounce)  # Utilisation d'une courbe d'atténuation
        animation.start()

    def ScorePlayer(self):
        print("Playing the score")

    def animate_window_size(self, start_size, end_size):
        animation = QPropertyAnimation(self.window(), b"size")
        animation.setStartValue(start_size)
        animation.setEndValue(end_size)
        animation.setDuration(500)  # Durée de l'animation en millisecondes
        animation.start()

    def animate_window_position(self, start_pos, end_pos):
        animation = QPropertyAnimation(self.window(), b"pos")
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setDuration(500)  # Durée de l'animation en millisecondes
        animation.start()
        print("acount server open")

    def show_menu(self):
        # Crée le menu contextuel principal
        menu_button_actived = QMenu(self)

        # Menu Fichier
        file_menu = QMenu("Fichier", self)
        
        open_action = file_menu.addAction("Ouvrir un projet")
        new_project_action = file_menu.addAction("Nouveau projet")
        close_project_action = file_menu.addAction("Fermer projet")
        new_version_project_action = file_menu.addAction("Nouvelle version projet")
        save_action = file_menu.addAction("Enregistrer")
        save_as_action = file_menu.addAction("Enregistrer sous")
        print_action = file_menu.addAction("Imprimer partition")

        file_menu.addSeparator()

        score_online_action = file_menu.addAction("Mettre la partition en ligne")
        score_movie_action = file_menu.addAction("Créer une video en ligne Partition")

        file_menu.addSeparator()

        import_menu = QMenu("Importer", self)
        import_audio_action = import_menu.addAction("Fichier audio")
        import_midi_action = import_menu.addAction("Fichier MIDI")
        import_xml_action = import_menu.addAction("Fichier XML")
        
        file_menu.addMenu(import_menu)

        export_menu = QMenu("Exporter", self)
        export_audio_action = export_menu.addAction("Fichier audio")
        export_picture_action = export_menu.addAction("Images")
        export_pdf_action = export_menu.addAction("Fichier PDF")
        export_midi_action = export_menu.addAction("Fichier MIDI")
        export_xml_action = export_menu.addAction("Fichier XML")
        
        file_menu.addMenu(export_menu)

        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Quitter")

        open_action.triggered.connect(self.open_file)
        new_project_action.triggered.connect(self.new_project)
        save_action.triggered.connect(self.save_file)
        # save_as_action.triggered.connect(self.save_at)
        # print_action.triggered.connect(self.print_score)
        # score_online_action.triggered.connect(self.score_online)
        # score_movie_action.triggered.connect(self.score_movie)
        # exit_action.triggered.connect(self.exit_app)

        menu_button_actived.addMenu(file_menu)

        # Menu Édition
        edit_menu = QMenu("Édition", self)
        
        annule_action = edit_menu.addAction("Annuler")
        retablir_action = edit_menu.addAction("Rétablir")
        historique_action = edit_menu.addAction("Historique")
        
        edit_menu.addSeparator()
        
        copy_action = edit_menu.addAction("Copier")
        cut_action = edit_menu.addAction("Couper")
        paste_action = edit_menu.addAction("Coller")
        
        edit_menu.addSeparator()
        
        select_action = edit_menu.addAction("Sélectionner")
        all_select_action = edit_menu.addAction("Tout sélectionner")
        search_action = edit_menu.addAction("Rechercher / Remplacer")
        reorganize_action = edit_menu.addAction("Réorganiser")
        mesure_auto_action = edit_menu.addAction("Mesure automatique")
        annotation_perfomance_action = edit_menu.addAction("Annotation performance")
        
        # annule_action.triggered.connect(self.annule)
        # retablir_action.triggered.connect(self.retablir)
        # copy_action.triggered.connect(self.copy)
        # cut_action.triggered.connect(self.cut)
        # paste_action.triggered.connect(self.paste)
        
        menu_button_actived.addMenu(edit_menu)

        # Menu MIDI
        midi_menu = QMenu("MIDI", self)
        
        open_midi_edit_action = midi_menu.addAction("Ouvrir éditeur clavier")
        open_rythme_edit_action = midi_menu.addAction("Ouvrir éditeur rythme")
        open_midi_edit_on_score_action = midi_menu.addAction("Ouvrir éditeur clavier sur partition")
        control_edit_action = midi_menu.addAction("Éditeur de contrôle")
        saved_midi_action = midi_menu.addAction("Enregistrement MIDI")
        
        midi_menu.addSeparator()
        
        transpose_action = midi_menu.addAction("Transposer")
        setting_midi_action = midi_menu.addAction("Paramètres MIDI")
        
        # open_midi_edit_action.triggered.connect(self.open_midi_edit)
        # open_rythme_edit_action.triggered.connect(self.open_rythme_edit)
        
        menu_button_actived.addMenu(midi_menu)

        # Menu Projet
        project_menu = QMenu("Projet", self)
        
        new_partition_action = project_menu.addAction("Nouvelle partition")
        duplic_part_action = project_menu.addAction("Dupliquer partition")
        new_version_score_action = project_menu.addAction("Nouvelle version partition")
        delete_score_action = project_menu.addAction("Supprimer partition")
        delete_vierge_scores_action = project_menu.addAction("Supprimer toutes les partitions vides")
        
        project_menu.addSeparator()
        
        library_action = project_menu.addAction("Bibliothèque")
        marqueurs_action = project_menu.addAction("Marqueurs")
        explorer_action = project_menu.addAction("Explorateur")
        calc_tempo_action = project_menu.addAction("Calculatrice de tempo")
        timecode_curseur_action = project_menu.addAction("Timecode curseur")
        notepad_action = project_menu.addAction("Bloc-notes")
        
        # new_partition_action.triggered.connect(self.new_partition)
        # delete_score_action.triggered.connect(self.delete_score)
        
        menu_button_actived.addMenu(project_menu)

        # Menu Déchiffrer
        decrypt_menu = QMenu("Déchiffrer", self)
        
        decrypt_audio_action = decrypt_menu.addAction("Déchiffrer fichier audio")
        decrypt_midi_live_action = decrypt_menu.addAction("Déchiffrer MIDI en direct")
        decrypt_midi_action = decrypt_menu.addAction("Déchiffrer fichier MIDI")
        decrypt_audio_saved_action = decrypt_menu.addAction("Déchiffrer enregistrement audio")
        
        decrypt_menu.addSeparator()
        
        harmonic_annaliser_action = decrypt_menu.addAction("Annalyse harmonique")
        tonn_annalyse_action = decrypt_menu.addAction("Annalyse tonalité")
        scan_partition_decryption_action = decrypt_menu.addAction("Scan partition decryption")
        hauteur_correction_action = decrypt_menu.addAction("Correcteur de la hauteur")
        
        # decrypt_audio_action.triggered.connect(self.decrypt_audio)
        
        menu_button_actived.addMenu(decrypt_menu)

        # Menu Partition
        score_menu = QMenu("Partition", self)
        
        partition_option_action = score_menu.addAction("Options partition")
        
        score_menu.addSeparator()
        
        page_mode_action = score_menu.addAction("Mode page")
        
        score_menu.addSeparator()
        
        group_ungroup_notes_action = score_menu.addAction("Grouper / dégrouper notes")
        convert_ornament_note_action = score_menu.addAction("Convertir en note d'ornement")
        define_n_olet_action = score_menu.addAction("Définir N-olet")
        split_action = score_menu.addAction("Éclatement")
        
        score_menu.addSeparator()
        
        mix_staves_action = score_menu.addAction("Mélanger les portées")
        extract_voice_action = score_menu.addAction("Extraire voix")
        insert_legato_action = score_menu.addAction("Insérer Legato")
        show_hide_action = score_menu.addAction("Montrer / Cacher")
        invert_action = score_menu.addAction("Inverser")
        
        # partition_option_action.triggered.connect(self.partition_option)
        
        menu_button_actived.addMenu(score_menu)

        # Menu Options
        options_menu = QMenu("Options", self)
        
        preferences_action = options_menu.addAction("Préférences")
        shortcuts_action = options_menu.addAction("Raccourcis clavier")
        themes_action = options_menu.addAction("Thèmes")
        customize_action = options_menu.addAction("Personnaliser")
        language_action = options_menu.addAction("Langue")
        auto_update_action = options_menu.addAction("Mise à jour automatique")
        auto_save_action = options_menu.addAction("Sauvegarde automatique")
        plug_ins = options_menu.addAction("Informations sur vos Plug-ins")
        
        # preferences_action.triggered.connect(self.preferences)
        themes_action.triggered.connect(self.change_theme)
        
        menu_button_actived.addMenu(options_menu)

        # Menu Aide
        help_menu = QMenu("Aide", self)
        
        open_doc_action = help_menu.addAction("Documentations")
        faq_action = help_menu.addAction("Foire aux questions")
        
        help_menu.addSeparator()
        
        credits_action = help_menu.addAction("Crédits")
        about_action = help_menu.addAction("À propos de TEXTA SM edit")
        
        # open_doc_action.triggered.connect(self.open_doc)
        
        menu_button_actived.addMenu(help_menu)

        # Affiche le menu au niveau du bouton
        menu_button_actived.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def open_file(self):
        # Ouvrir un fichier via un QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un projet", "", "Score Files (*.score);;All Files (*)")
        
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    
                    # Ajouter une méthode pour découper les objets JSON concaténés
                    json_objects = []
                    decoder = json.JSONDecoder()

                    pos = 0
                    while pos < len(content):
                        try:
                            obj, index = decoder.raw_decode(content, pos)
                            json_objects.append(obj)
                            pos = index
                        except ValueError as e:
                            print(f"Erreur de décodage à la position {pos}: {e}")
                            break

                    # Charger chaque objet JSON dans le canvas
                    for obj in json_objects:
                        self.score_editor.canvas.load_canvas_data(obj)

                    print(f"Fichier .score chargé avec succès : {file_name}")

            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON dans le fichier .score : {e}")
            except Exception as e:
                print(f"Erreur lors de l'ouverture du fichier : {e}")

    def new_project(self):
        print("Créer un nouveau projet")
    
    def save_file(self):
        # Ouvre un dialogue pour demander où enregistrer le fichier
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer fichier", "", "Score Files (*.score);;All Files (*)")
        
        if file_name:
            # Récupérer les données du canvas via get_canvas_data
            data = self.canvas.get_canvas_data()

            # Calculer l'effort total (par exemple, le nombre total de notes dans toutes les mesures)
            total_steps = sum(len(measure["notes"]) for measure in data["measures"])
            
            # Créer la fenêtre de dialogue pour afficher la progression
            progress_dialog = QProgressDialog("Enregistrement du fichier...", "Annuler", 0, total_steps, self)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            
            # Enregistrer les données dans un fichier .score
            with open(file_name, 'w') as file:
                for i, measure in enumerate(data["measures"]):
                    for j, note in enumerate(measure["notes"]):
                        # Enregistrer la note dans le fichier
                        json.dump(note, file)

                        # Mettre à jour le texte de la barre de progression pour afficher la note en cours d'enregistrement
                        progress_dialog.setLabelText(f"Enregistrement de la note {note['position']} dans la mesure {i + 1}")
                        
                        # Mettre à jour la progression
                        progress_dialog.setValue(progress_dialog.value() + 1)

                        # Vérifier si l'utilisateur a annulé l'enregistrement
                        if progress_dialog.wasCanceled():
                            return  # Si l'utilisateur annule, on arrête l'enregistrement
            
            print(f"Fichier enregistré sous : {file_name}")

    def get_canvas_data(self):
        # Exemples de données étendues, avec plus de mesures et plus de notes.
        notes = [
            {"pitch": "C4", "duration": "quarter"},
            {"pitch": "D4", "duration": "half"},
            {"pitch": "E4", "duration": "quarter"},
            {"pitch": "F4", "duration": "whole"},
            {"pitch": "G4", "duration": "eighth"},
            # Tu peux ajouter ici plus de notes pour tester l'enregistrement
        ]
        
        # Exemple de mesures : Supposons que tu as 100 mesures, chaque mesure contenant des notes
        measures = [{"notes": notes} for _ in range(100)]  # Créer 100 mesures avec les mêmes notes
        
        return {
            "clef": "sol",  # Toujours la clé de sol
            "notes": notes,  # Les notes de la partition
            "measures": measures  # Les mesures de la partition (100 mesures ici)
        }

    def change_theme(self):
        dialog = ThemeDialog(self)
        dialog.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(500, 500)
        self.setWindowTitle("TEXTA Score Edit")
        self.setGeometry(100, 100, 800, 600)

        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal vertical
        main_layout = QVBoxLayout()

        # Barre de titre
        self.title_bar = OptionsBar(self, main_window=self)  # Passer la référence de MainWindow

        main_layout.addWidget(self.title_bar)

        # Layout principal horizontal pour le contenu
        content_layout = QHBoxLayout()

        # Volet latéral
        self.sidebar = self.create_sidebar()
        content_layout.addWidget(self.sidebar)

        # Section droite : canvas + onglets
        right_layout = QVBoxLayout()

        # Utilisation de ScoreEditor
        self.score_editor = ScoreEditor()
        right_layout.addWidget(self.score_editor)

        # Onglets sous le canvas
        tabs = self.create_tabs()
        right_layout.addWidget(tabs)
        content_layout.addLayout(right_layout)

        self.h_sidebar = QTextEdit()
        self.h_sidebar.setReadOnly(True)
        self.h_sidebar.setFixedWidth(350)
        self.h_sidebar.hide()  # Le volet est caché par défaut
        content_layout.addWidget(self.h_sidebar)

        # Appliquer le layout horizontal au widget central
        main_layout.addLayout(content_layout)
        central_widget.setLayout(main_layout)

        # Animation de la fenêtre
        self.init_animation()

    def toggle_help_sidebar(self):
        """Afficher ou masquer le volet latéral d'aide."""
        if self.h_sidebar.isVisible():
            self.h_sidebar.hide()  # Cacher si déjà visible
        else:
            # Ajouter le contenu HTML lorsque le volet est visible
            self.h_sidebar.setHtml("""
                <h1>Aide</h1>
                <p>Ceci est le volet d'aide de TEXTA Score Edit.</p>
                <ul>
                    <li>Clavier virtuel : Vous pouvez utiliser le clavier pour entrer des notes.</li>
                    <li>Onglet Dessin : Permet de dessiner des partitions manuellement.</li>
                </ul>
            """)
            self.h_sidebar.show()  # Afficher le volet

    def toggle_acount_sidebar(self):
        if self.h_sidebar.isVisible():
            self.h_sidebar.hide()
        else:
            self.h_sidebar.setHtml("""
                <h1>Compte</h1>
                <p>Ceci est le vollet de votre compte TEXTA.</p>
            """)
            self.h_sidebar.show()
            
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(250)

        sidebar_layout = QVBoxLayout()

        toolbox = QToolBox()
        sidebar_layout.addWidget(toolbox)

        # Onglet 1 : Bibliothèque d'images - Catégorie 1
        tab_1_widget = QWidget()
        tab_1_layout = QVBoxLayout()

        # Ajouter des images dans l'onglet 1
        image1 = QLabel()
        image1.setPixmap(QPixmap('image1.jpg'))
        image2 = QLabel()
        image2.setPixmap(QPixmap('image2.jpg'))

        # Ajouter les images dans le layout de l'onglet 1
        tab_1_layout.addWidget(image1)
        tab_1_layout.addWidget(image2)

        # Assigner le layout à l'onglet
        tab_1_widget.setLayout(tab_1_layout)
        toolbox.addItem(tab_1_widget, 'Catégorie 1')

        # Onglet 2 : Bibliothèque d'images - Catégorie 2
        tab_2_widget = QWidget()
        tab_2_layout = QVBoxLayout()

        # Ajouter d'autres images dans l'onglet 2
        image3 = QLabel()
        image3.setPixmap(QPixmap('image3.jpg'))
        image4 = QLabel()
        image4.setPixmap(QPixmap('image4.jpg'))

        # Ajouter les images dans le layout de l'onglet 2
        tab_2_layout.addWidget(image3)
        tab_2_layout.addWidget(image4)

        # Assigner le layout à l'onglet
        tab_2_widget.setLayout(tab_2_layout)
        toolbox.addItem(tab_2_widget, 'Catégorie 2')
        
        # sidebar_layout.addWidget(QLabel("Insérer :"))
        # sidebar_layout.addWidget(QPushButton("Favorits"))
        # sidebar_layout.addWidget(QPushButton("Récents"))
        # sidebar_layout.addWidget(QPushButton("Tonnalité"))
        # sidebar_layout.addWidget(QPushButton("Clés"))
        # sidebar_layout.addWidget(QPushButton("Mesures"))
        # sidebar_layout.addWidget(QPushButton("Symboles accords"))
        # sidebar_layout.addWidget(QPushButton("Symboles guitares"))
        # sidebar_layout.addWidget(QPushButton("Symboles de notes"))
        # sidebar_layout.addWidget(QPushButton("Nuances"))
        # sidebar_layout.addWidget(QPushButton("Lignes"))
        # sidebar_layout.addWidget(QPushButton("Autres"))
        # sidebar_layout.addWidget(QPushButton("Vos symboles"))

        toolbox.setCurrentIndex(1)

        spacer_sidebar = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        sidebar_layout.addSpacerItem(spacer_sidebar)

        sidebar.setLayout(sidebar_layout)
        return sidebar

    def create_tabs(self):
        tabs = QTabWidget()

        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("Contenu du premier onglet"))
        tab1.setLayout(tab1_layout)

        tab2 = ManualScoreEditor()

        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QTextEdit("Saisissez du texte ici"))
        tab3.setLayout(tab3_layout)

        tab4 = DecryptTab()

        # Ajout des onglets
        tabs.addTab(tab1, "Dessiner")
        tabs.addTab(tab2, "Clavier virtuel")
        tabs.addTab(MidiTab(), "Éditeur MIDI")
        tabs.addTab(tab3, "Editeur de texte")
        tabs.addTab(tab4, "Decrypter")

        return tabs

    def init_animation(self):
        self.window_animation = QPropertyAnimation(self, b"windowOpacity")
        self.window_animation.setStartValue(0)
        self.window_animation.setEndValue(1)
        self.window_animation.setDuration(500)
        self.window_animation.start()

    def open_file(self):
        # Ouvre un fichier via un QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Partitions (*.xml *.musicxml)")
        if file_name:
            # Charger le fichier ici
            print(f"Fichier ouvert: {file_name}")

    def save_file(self):
        # Enregistre un fichier via un QFileDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "Partitions (*.xml *.musicxml)")
        if file_name:
            # Enregistrer le fichier ici
            print(f"Fichier enregistré: {file_name}")

def load_stylesheet(app, filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            app.setStyleSheet(file.read())
    else:
        print(f"Feuille de style non trouvée : {filename}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    load_stylesheet(app, "styles/style.css")
    window = MainWindow()
    window.setWindowTitle("TEXTA score edit")
    window.setWindowIcon(QIcon('IconApp/app/app_icon.png'))
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec_())