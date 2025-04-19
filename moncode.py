import tkinter as tk
from tkinter import ttk, messagebox
import random

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculatrice d'IMC Fun")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Couleurs thématiques
        self.colors = {
            "bg": "#1e3d59",           # Bleu foncé
            "accent1": "#f5f0e1",      # Beige clair
            "accent2": "#ff6e40",      # Orange
            "accent3": "#ffc13b",      # Jaune
            "text_light": "#ffffff",   # Blanc
            "text_dark": "#333333"     # Gris foncé
        }
        
        # Configurer les couleurs de base
        self.root.configure(bg=self.colors["bg"])
        
        # Configurer les styles
        self.setup_styles()
        
        # Créer les widgets
        self.create_widgets()
        
        # Easter egg: cliquer 5 fois sur le titre change les couleurs
        self.click_count = 0

    def setup_styles(self):
        style = ttk.Style()
        
        # Style pour les cadres
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("TLabelframe", background=self.colors["bg"], foreground=self.colors["text_light"])
        style.configure("TLabelframe.Label", background=self.colors["bg"], foreground=self.colors["accent3"], font=("Arial", 12, "bold"))
        
        # Style pour les étiquettes
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["accent1"], font=("Arial", 11))
        style.configure("Title.TLabel", background=self.colors["bg"], foreground=self.colors["accent3"], font=("Arial", 24, "bold"))
        style.configure("Result.TLabel", background=self.colors["bg"], foreground=self.colors["accent3"], font=("Arial", 16, "bold"))
        style.configure("Category.TLabel", background=self.colors["bg"], foreground=self.colors["accent1"], font=("Arial", 14))
        
        # Style pour les boutons
        style.configure("TButton", background=self.colors["accent2"], foreground=self.colors["text_dark"], font=("Arial", 12, "bold"))
        style.configure("Fun.TButton", background=self.colors["accent3"], foreground=self.colors["text_dark"], font=("Arial", 14, "bold"), padding=(20, 10))
        style.map("Fun.TButton",
                 background=[("active", self.colors["accent2"])],
                 foreground=[("active", self.colors["text_light"])])

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Titre avec effet de clic
        self.title_label = ttk.Label(
            main_frame, 
            text="Calculatrice d'IMC Fun", 
            style="Title.TLabel"
        )
        self.title_label.pack(pady=15)
        self.title_label.bind("<Button-1>", self.title_click)

        # Frame pour les entrées avec un style amélioré
        input_frame = ttk.LabelFrame(main_frame, text="Vos mesures", padding=15)
        input_frame.pack(fill="x", pady=15)

        # Poids avec icône emoji
        weight_frame = ttk.Frame(input_frame)
        weight_frame.pack(fill="x", pady=5)
        
        weight_emoji = ttk.Label(weight_frame, text="⚖️", font=("Arial", 16))
        weight_emoji.pack(side="left", padx=(0, 10))
        
        weight_label = ttk.Label(
            weight_frame, 
            text="Poids (kg):", 
            font=("Arial", 12)
        )
        weight_label.pack(side="left")
        
        self.weight_var = tk.StringVar()
        weight_entry = tk.Entry(
            weight_frame, 
            textvariable=self.weight_var, 
            width=8, 
            font=("Arial", 12, "bold"),
            bg=self.colors["accent1"],
            fg=self.colors["text_dark"],
            relief="flat",
            bd=10
        )
        weight_entry.pack(side="right", padx=10)

        # Taille avec icône emoji
        height_frame = ttk.Frame(input_frame)
        height_frame.pack(fill="x", pady=5)
        
        height_emoji = ttk.Label(height_frame, text="📏", font=("Arial", 16))
        height_emoji.pack(side="left", padx=(0, 10))
        
        height_label = ttk.Label(
            height_frame, 
            text="Taille (cm):", 
            font=("Arial", 12)
        )
        height_label.pack(side="left")
        
        self.height_var = tk.StringVar()
        height_entry = tk.Entry(
            height_frame, 
            textvariable=self.height_var, 
            width=8, 
            font=("Arial", 12, "bold"),
            bg=self.colors["accent1"],
            fg=self.colors["text_dark"],
            relief="flat",
            bd=10
        )
        height_entry.pack(side="right", padx=10)

        # Bouton de calcul animé
        self.btn_text = tk.StringVar()
        self.btn_text.set("Calculer mon IMC!")
        calculate_button = ttk.Button(
            main_frame, 
            textvariable=self.btn_text,
            command=self.calculate_bmi,
            style="Fun.TButton"
        )
        calculate_button.pack(pady=15)
        
        # Animation du bouton
        self.animate_button()

        # Résultat avec design amélioré
        result_frame = ttk.LabelFrame(
            main_frame, 
            text="Résultat", 
            padding=15
        )
        result_frame.pack(fill="x", pady=10)

        # Canvas pour le cercle indicateur
        self.result_canvas = tk.Canvas(
            result_frame, 
            width=150, 
            height=150,
            bg=self.colors["bg"],
            highlightthickness=0
        )
        self.result_canvas.pack(side="left", padx=10)
        
        # Dessiner un cercle initial gris
        self.indicator_circle = self.result_canvas.create_oval(25, 25, 125, 125, fill="#555555", width=0)
        self.indicator_text = self.result_canvas.create_text(75, 75, text="--", fill=self.colors["text_light"], font=("Arial", 22, "bold"))

        # Zone de texte des résultats
        result_text_frame = ttk.Frame(result_frame)
        result_text_frame.pack(side="left", fill="both", expand=True)
        
        self.bmi_var = tk.StringVar()
        self.bmi_var.set("--")
        bmi_label = ttk.Label(
            result_text_frame, 
            textvariable=self.bmi_var,
            style="Result.TLabel"
        )
        bmi_label.pack(anchor="w", pady=(0, 5))

        self.category_var = tk.StringVar()
        self.category_var.set("Entrez vos données et cliquez sur Calculer")
        self.category_label = ttk.Label(
            result_text_frame, 
            textvariable=self.category_var,
            style="Category.TLabel",
            wraplength=200
        )
        self.category_label.pack(anchor="w")

        # Message fun
        self.fun_message_var = tk.StringVar()
        self.fun_message_var.set("Prêt à découvrir votre IMC ?")
        fun_message = ttk.Label(
            main_frame,
            textvariable=self.fun_message_var,
            font=("Arial", 10, "italic"),
            foreground=self.colors["accent1"]
        )
        fun_message.pack(pady=5)

        # Tableau d'informations IMC amélioré
        info_frame = ttk.LabelFrame(
            main_frame, 
            text="Catégories d'IMC", 
            padding=10
        )
        info_frame.pack(fill="x", pady=10)

        # Utiliser un Treeview pour un tableau plus joli
        columns = ("catégorie", "imc", "signification")
        tree = ttk.Treeview(info_frame, columns=columns, show="headings", height=6)
        tree.pack(fill="both", expand=True)

        # Définir les en-têtes
        tree.heading("catégorie", text="Catégorie")
        tree.heading("imc", text="IMC")
        tree.heading("signification", text="Signification")
        
        # Ajuster les colonnes
        tree.column("catégorie", width=120)
        tree.column("imc", width=80)
        tree.column("signification", width=180)
        
        # Ajouter les données
        tree.insert("", "end", values=("Insuffisance", "< 18.5", "Poids insuffisant"))
        tree.insert("", "end", values=("Normal", "18.5 - 24.9", "Poids santé"))
        tree.insert("", "end", values=("Surpoids", "25.0 - 29.9", "Embonpoint"))
        tree.insert("", "end", values=("Obésité I", "30.0 - 34.9", "Obésité modérée"))
        tree.insert("", "end", values=("Obésité II", "35.0 - 39.9", "Obésité sévère"))
        tree.insert("", "end", values=("Obésité III", "≥ 40.0", "Obésité morbide"))
        
        # Effet de survol pour le tableau
        def on_tree_select(event):
            selected_item = tree.selection()[0]
            category = tree.item(selected_item, "values")[0]
            tree.item(selected_item, tags=("selected",))
            
        tree.bind("<<TreeviewSelect>>", on_tree_select)
        tree.tag_configure("selected", background=self.colors["accent2"])

        # Bouton pour effacer les données
        clear_button = ttk.Button(
            main_frame, 
            text="Effacer",
            command=self.clear_data,
        )
        clear_button.pack(pady=5)

    def title_click(self, event):
        # Easter egg: changer les couleurs après 5 clics
        self.click_count += 1
        if self.click_count >= 5:
            self.click_count = 0
            # Changer les couleurs aléatoirement
            new_colors = [
                "#ff9a8b", "#ffac8b", "#ffc58b", 
                "#b8f2e6", "#aed9e0", "#5e6472",
                "#ffa69e", "#b8bedd", "#3f8efc"
            ]
            self.colors["accent2"] = random.choice(new_colors)
            self.colors["accent3"] = random.choice(new_colors)
            self.setup_styles()
            messagebox.showinfo("Easter Egg!", "Vous avez découvert l'easter egg! Couleurs modifiées!")

    def animate_button(self):
        # Animation du texte du bouton
        texts = ["Calculer mon IMC!", "C'est parti!", "Découvrir mon IMC!", "Voir mon résultat!"]
        self.btn_text.set(random.choice(texts))
        self.root.after(3000, self.animate_button)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get().replace(',', '.'))
            height = float(self.height_var.get().replace(',', '.')) / 100  # conversion cm en m
            
            if weight <= 0 or height <= 0:
                raise ValueError("Les valeurs doivent être positives")
            
            bmi = weight / (height * height)
            self.bmi_var.set(f"IMC: {bmi:.1f}")
            
            # Déterminer la catégorie et la couleur
            if bmi < 18.5:
                category = "Insuffisance pondérale"
                color = "#64B5F6"  # Bleu clair
                message = "Un peu léger! Un bon repas s'impose?"
            elif bmi < 25:
                category = "Poids normal"
                color = "#81C784"  # Vert
                message = "Parfait! Continuez comme ça!"
            elif bmi < 30:
                category = "Surpoids"
                color = "#FFD54F"  # Jaune
                message = "Un peu d'exercice serait bien!"
            elif bmi < 35:
                category = "Obésité classe I"
                color = "#FFA726"  # Orange
                message = "Il serait temps de faire attention!"
            elif bmi < 40:
                category = "Obésité classe II"
                color = "#FF7043"  # Orange foncé
                message = "Une consultation médicale serait judicieuse."
            else:
                category = "Obésité classe III"
                color = "#E53935"  # Rouge
                message = "Consultez un médecin rapidement!"
            
            self.category_var.set(category)
            self.fun_message_var.set(message)
            
            # Mettre à jour le cercle indicateur
            self.result_canvas.itemconfig(self.indicator_circle, fill=color)
            self.result_canvas.itemconfig(self.indicator_text, text=f"{bmi:.1f}")
            
            # Animation de réussite
            self.root.after(100, lambda: self.flash_result(color))
            
        except ValueError as e:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
            self.bmi_var.set("--")
            self.category_var.set("Erreur dans les données")
            self.fun_message_var.set("Oups! Quelque chose ne va pas!")

    def flash_result(self, color, count=0):
        # Effet clignotant pour le résultat
        if count < 6:
            new_color = self.colors["accent2"] if count % 2 == 0 else color
            self.category_label.configure(foreground=new_color)
            self.root.after(200, lambda: self.flash_result(color, count + 1))
        else:
            self.category_label.configure(foreground=self.colors["accent1"])

    def clear_data(self):
        # Effacer les données
        self.weight_var.set("")
        self.height_var.set("")
        self.bmi_var.set("--")
        self.category_var.set("Entrez vos données et cliquez sur Calculer")
        self.fun_message_var.set("Prêt à découvrir votre IMC ?")
        self.result_canvas.itemconfig(self.indicator_circle, fill="#555555")
        self.result_canvas.itemconfig(self.indicator_text, text="--")


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()