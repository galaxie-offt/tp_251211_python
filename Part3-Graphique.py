import tkinter as tk
from tkinter import messagebox
import json
import os
import random
from PIL import Image, ImageTk  # pip install pillow

# Définition des classes et de leurs statistiques
CLASSES = {
    "Barbare": {"pv": 85, "attaque": 17, "defense": 5},
    "Mage": {"pv": 90, "attaque": 20, "defense": 5},
    "Archer": {"pv": 100, "attaque": 15, "defense": 7}
}

class Character:
    def __init__(self, nom, pv, attaque, defense):
        self.nom = nom
        self.pv = pv
        self.pv_max = pv
        self.attaque = attaque
        self.defense = defense
        self.inventaire = []
        self.cooldowns = {"soin": 0}

    def attack_target(self, target, bonus=0):
        degats = max(1, self.attaque + bonus - target.defense)
        target.pv -= degats
        return degats

    def heal(self, bonus=0):
        if self.cooldowns["soin"] > 0:
            return False
        soin = 20 + bonus
        self.pv = min(self.pv_max, self.pv + soin)
        self.cooldowns["soin"] = 3
        return True

    def is_alive(self):
        return self.pv > 0

    def reset_cooldowns(self):
        for k in self.cooldowns:
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1

    def afficher_stats(self):
        stats = f"--- Statistiques de {self.nom} ---\n"
        stats += f"Vie : {self.pv}/{self.pv_max}\n"
        stats += f"Attaque : {self.attaque}\n"
        stats += f"Défense : {self.defense}\n"
        stats += f"Inventaire : {[obj for obj in self.inventaire]}"
        return stats

class Enemy(Character):
    def __init__(self, nom, pv, attaque, defense):
        super().__init__(nom, pv, attaque, defense)

    def attack_target(self, target, bonus=0):
        degats = max(1, self.attaque + bonus - target.defense)
        target.pv -= degats
        return degats

class Boss(Enemy):
    def __init__(self, nom, pv, attaque, defense):
        super().__init__(nom, pv, attaque, defense)
        self.cooldowns = {"ultime": 0, "soin": 0}

    def attack_target(self, target):
        if self.cooldowns["ultime"] > 0:
            self.cooldowns["ultime"] -= 1
        if self.cooldowns["soin"] > 0:
            self.cooldowns["soin"] -= 1

        choix = random.choice(["simple", "ultime", "soin"])
        if choix == "simple":
            degats = max(1, self.attaque - target.defense)
            target.pv -= degats
            return f"{self.nom} utilise une attaque simple et inflige {degats} dégâts."
        elif choix == "ultime" and self.cooldowns["ultime"] == 0:
            degats = max(1, self.attaque * 2 - target.defense)
            target.pv -= degats
            self.cooldowns["ultime"] = 2
            return f"{self.nom} utilise une attaque ultime et inflige {degats} dégâts !"
        elif choix == "soin" and self.cooldowns["soin"] == 0:
            soin = 25
            self.pv = min(self.pv_max, self.pv + soin)
            self.cooldowns["soin"] = 3
            return f"{self.nom} se soigne de {soin} PV."
        else:
            degats = max(1, self.attaque - target.defense)
            target.pv -= degats
            return f"{self.nom} utilise une attaque simple et inflige {degats} dégâts."

class GameEngine:
    def __init__(self):
        self.joueur = None
        self.ennemis = [
            Enemy("Gobelin", 50, 12, 5),
            Enemy("Orc", 75, 19, 8),
            Enemy("Troll", 120, 28, 12),
        ]
        self.boss = Boss("Dragon", 200, 30, 15)
        self.objets_donnes = []
        self.combat_en_cours = None
        self.victoires = 0
        self.ennemi_index = 0

    def start_battle(self, ennemi):
        self.combat_en_cours = ennemi
        self.joueur.reset_cooldowns()
        ennemi.reset_cooldowns()
        while self.joueur.is_alive() and ennemi.is_alive():
            return True
        return False

    def generer_objets(self):
        types = [
            {"nom": "Épée", "min_attaque": 5, "max_attaque": 10},
            {"nom": "Bouclier", "min_defense": 5, "max_defense": 10},
            {"nom": "Armure", "min_defense": 8, "max_defense": 15},
            {"nom": "Amulette", "min_attaque": 3, "max_attaque": 8, "min_defense": 3, "max_defense": 8},
            {"nom": "Potion", "min_pv": 15, "max_pv": 25},
            {"nom": "Anneau de régénération", "min_pv": 8, "max_pv": 15, "min_attaque": 2, "max_attaque": 5},
            {"nom": "Cape de vitesse", "min_attaque": 3, "max_attaque": 7, "min_defense": 3, "max_defense": 7},
            {"nom": "Tome de connaissance", "min_attaque": 5, "max_attaque": 9},
            {"nom": "Ceinture de force", "min_attaque": 2, "max_attaque": 5, "min_defense": 6, "max_defense": 10},
            {"nom": "Gants de précision", "min_attaque": 4, "max_attaque": 8, "min_defense": 1, "max_defense": 4}
        ]
        random.shuffle(types)
        objets = []
        for i in range(3):
            typ = types[i]
            obj = {"nom": typ["nom"]}
            if "min_attaque" in typ:
                obj["attaque"] = random.randint(typ["min_attaque"], typ["max_attaque"])
            if "min_defense" in typ:
                obj["defense"] = random.randint(typ["min_defense"], typ["max_defense"])
            if "min_pv" in typ:
                obj["pv"] = random.randint(typ["min_pv"], typ["max_pv"])
            objets.append(obj)
        return objets

    def sauvegarder(self, nom_fichier=None):
        if nom_fichier is None:
            nom_fichier = f"sauvegarde_{self.joueur.nom}.json"
        data = {
            "joueur": {
                "nom": self.joueur.nom,
                "pv": self.joueur.pv,
                "pv_max": self.joueur.pv_max,
                "attaque": self.joueur.attaque,
                "defense": self.joueur.defense,
                "inventaire": self.joueur.inventaire,
                "cooldowns": self.joueur.cooldowns
            },
            "ennemi": {
                "nom": self.combat_en_cours.nom if self.combat_en_cours else None,
                "pv": self.combat_en_cours.pv if self.combat_en_cours else None,
                "attaque": self.combat_en_cours.attaque if self.combat_en_cours else None,
                "defense": self.combat_en_cours.defense if self.combat_en_cours else None,
                "cooldowns": self.combat_en_cours.cooldowns if self.combat_en_cours else {}
            },
            "victoires": self.victoires,
            "objets_donnes": self.objets_donnes,
            "ennemi_index": self.ennemi_index
        }
        with open(nom_fichier, "w") as f:
            json.dump(data, f, indent=4)

    def charger(self, nom_fichier):
        try:
            with open(nom_fichier, "r") as f:
                data = json.load(f)
            if self.joueur is None:
                self.joueur = Character("", 1, 1, 1)
            self.joueur.nom = data["joueur"]["nom"]
            self.joueur.pv = data["joueur"]["pv"]
            self.joueur.pv_max = data["joueur"]["pv_max"]
            self.joueur.attaque = data["joueur"]["attaque"]
            self.joueur.defense = data["joueur"]["defense"]
            self.joueur.inventaire = data["joueur"]["inventaire"]
            self.joueur.cooldowns = data["joueur"]["cooldowns"]
            self.objets_donnes = data["objets_donnes"]
            self.victoires = data["victoires"]
            self.ennemi_index = data.get("ennemi_index", 0)

            if data["ennemi"]["nom"]:
                for e in self.ennemis + [self.boss]:
                    if e.nom == data["ennemi"]["nom"]:
                        e.pv = data["ennemi"]["pv"]
                        e.attaque = data["ennemi"]["attaque"]
                        e.defense = data["ennemi"]["defense"]
                        e.cooldowns = data["ennemi"]["cooldowns"]
                        self.combat_en_cours = e
                        break
                else:
                    messagebox.showerror("Erreur", "Ennemi non trouvé dans la liste.")
            else:
                self.combat_en_cours = None
            return True
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Aucune sauvegarde trouvée.")
            return False

    def supprimer_sauvegarde(self, nom_fichier):
        if os.path.exists(nom_fichier):
            os.remove(nom_fichier)

class GameGUI:
    def __init__(self):
        self.game = GameEngine()
        self.window = tk.Tk()
        self.window.title("Jeu de Combat Graphique")
        self.window.attributes("-fullscreen", True)
        self.window.bind("<F11>", self.toggle_fullscreen)
        self.window.bind("<Escape>", self.exit_fullscreen)

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.menu_canvas = None
        self.combat_canvas = None
        self.hero_img = None
        self.enemy_imgs = {}
        self.hero_sprite = None
        self.enemy_sprite = None
        self.label_stats = None
        self.label_ennemi = None
        self.label_log = None
        self.button_attaquer = None
        self.button_soin = None
        self.button_quitter = None
        self.choix_frame = None
        self.fullscreen = True

        # widgets du menu (références gardées pour les callbacks)
        self.label_titre = None
        self.label_joueur = None
        self.entry_nom = None
        self.label_classe = None
        self.classe_var = None
        self.sauvegardes_liste = None

        self.create_menu()

    # ---------- Gestion fenêtre ----------

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.window.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.window.attributes("-fullscreen", False)

    # ---------- Menu sur Canvas ----------

    def create_menu(self):
        self.menu_canvas = tk.Canvas(self.window, highlightthickness=0, bd=0)
        self.menu_canvas.pack(fill="both", expand=True)

        # image de fond plein écran
        menu_img = Image.open("assets/menu_bg.png")
        menu_img = menu_img.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        self.menu_bg = ImageTk.PhotoImage(menu_img)
        self.menu_canvas.create_image(0, 0, image=self.menu_bg, anchor="nw")

        # coordonnées du "centre" virtuel du menu
        panel_x = self.screen_width // 2
        panel_y = self.screen_height // 2

        # Titre
        self.label_titre = tk.Label(
            self.window,
            text="RPG Combat",
            font=("Arial", 28, "bold"),
            bg="#000000",
            fg="white"
        )
        self.menu_canvas.create_window(panel_x, panel_y - 130, window=self.label_titre)

        # Nom du perso
        self.label_joueur = tk.Label(
            self.window,
            text="Nom du personnage :",
            bg="#000000",
            fg="white"
        )
        self.menu_canvas.create_window(panel_x, panel_y - 80, window=self.label_joueur)

        self.entry_nom = tk.Entry(self.window, width=25, font=("Arial", 12))
        self.menu_canvas.create_window(panel_x, panel_y - 50, window=self.entry_nom)

        # Choix de classe
        self.label_classe = tk.Label(
            self.window,
            text="Choisissez une classe :",
            bg="#000000",
            fg="white"
        )
        self.menu_canvas.create_window(panel_x, panel_y - 10, window=self.label_classe)

        self.classe_var = tk.StringVar()
        # on utilise trois RadioButtons séparés, chacun posé via create_window
        y_base = panel_y + 15
        for i, classe in enumerate(CLASSES.keys()):
            rb = tk.Radiobutton(
                self.window,
                text=classe,
                variable=self.classe_var,
                value=classe,
                bg="#000000",
                fg="white",
                selectcolor="#404040",
                anchor="w"
            )
            self.menu_canvas.create_window(panel_x - 60, y_base + i * 25, window=rb, anchor="w")

        # Boutons Nouvelle partie / Charger
        button_nouveau = tk.Button(
            self.window,
            text="Nouvelle partie",
            width=18,
            command=self.nouvelle_partie
        )
        button_charger = tk.Button(
            self.window,
            text="Charger une sauvegarde",
            width=18,
            command=self.charger_partie
        )
        self.menu_canvas.create_window(panel_x - 90, panel_y + 110, window=button_nouveau)
        self.menu_canvas.create_window(panel_x + 90, panel_y + 110, window=button_charger)

        # Liste des sauvegardes
        label_saves = tk.Label(
            self.window,
            text="Sauvegardes :",
            bg="#000000",
            fg="white"
        )
        self.menu_canvas.create_window(panel_x, panel_y + 150, window=label_saves)

        self.sauvegardes_liste = tk.Listbox(self.window, width=35, height=3)
        self.menu_canvas.create_window(panel_x, panel_y + 185, window=self.sauvegardes_liste)

        button_supprimer = tk.Button(
            self.window,
            text="Supprimer une sauvegarde",
            command=self.supprimer_sauvegarde
        )
        self.menu_canvas.create_window(panel_x, panel_y + 220, window=button_supprimer)

        self.load_saves()

    def load_saves(self):
        sauvegardes = [f for f in os.listdir() if f.startswith("sauvegarde_") and f.endswith(".json")]
        self.sauvegardes_liste.delete(0, tk.END)
        for s in sauvegardes:
            self.sauvegardes_liste.insert(tk.END, s)

    # ---------- Actions du menu ----------

    def nouvelle_partie(self):
        nom = self.entry_nom.get().strip()
        classe = self.classe_var.get()
        if not nom:
            messagebox.showerror("Erreur", "Veuillez entrer un nom.")
            return
        if not classe:
            messagebox.showerror("Erreur", "Veuillez choisir une classe.")
            return
        stats = CLASSES[classe]
        self.game.joueur = Character(nom, stats["pv"], stats["attaque"], stats["defense"])
        self.start_game()

    def charger_partie(self):
        selection = self.sauvegardes_liste.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner une sauvegarde.")
            return
        fichier = self.sauvegardes_liste.get(selection[0])
        self.game.joueur = Character("", 1, 1, 1)
        if self.game.charger(fichier):
            self.start_game()

    def supprimer_sauvegarde(self):
        selection = self.sauvegardes_liste.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner une sauvegarde.")
            return
        fichier = self.sauvegardes_liste.get(selection[0])
        self.game.supprimer_sauvegarde(fichier)
        self.load_saves()

    # ---------- Écran de combat (inchangé sauf suppression menu_panel) ----------

    def start_game(self):
        # on enlève le canvas de menu
        self.menu_canvas.pack_forget()

        self.combat_canvas = tk.Canvas(self.window, highlightthickness=0, bd=0)
        self.combat_canvas.pack(fill="both", expand=True)

        bg_img = Image.open("assets/combat_bg.gif")
        bg_img = bg_img.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        self.combat_bg = ImageTk.PhotoImage(bg_img)
        self.combat_canvas.create_image(0, 0, image=self.combat_bg, anchor="nw")

        hero_img = Image.open("assets/hero.png")
        hero_img = hero_img.resize((128, 128), Image.LANCZOS)
        self.hero_img = ImageTk.PhotoImage(hero_img)

        self.enemy_imgs = {}
        enemy_files = {
            "Gobelin": "assets/gobelin.png",
            "Orc": "assets/orc.png",
            "Troll": "assets/troll.png",
            "Dragon": "assets/dragon.png",
        }
        for nom, path in enemy_files.items():
            img = Image.open(path)
            img = img.resize((128, 128), Image.LANCZOS)
            self.enemy_imgs[nom] = ImageTk.PhotoImage(img)

        hero_x = self.screen_width // 4
        hero_y = int(self.screen_height * 0.65)
        self.hero_sprite = self.combat_canvas.create_image(hero_x, hero_y, image=self.hero_img)
        self.enemy_sprite = None

        self.label_stats = tk.Label(self.window, justify="left", bg="black", fg="white")
        self.label_ennemi = tk.Label(self.window, justify="left", bg="black", fg="white")
        self.label_log = tk.Label(self.window, justify="left", bg="black", fg="white")

        self.combat_canvas.create_window(self.screen_width * 0.16, self.screen_height * 0.18, window=self.label_stats)
        self.combat_canvas.create_window(self.screen_width * 0.84, self.screen_height * 0.18, window=self.label_ennemi)
        self.combat_canvas.create_window(self.screen_width * 0.5,  self.screen_height * 0.8, window=self.label_log)

        self.button_attaquer = tk.Button(self.window, text="Attaquer", width=12, command=self.attaquer)
        self.button_soin = tk.Button(self.window, text="Soigner", width=12, command=self.soin)
        self.button_quitter = tk.Button(self.window, text="Quitter", width=12, command=self.quitter)

        self.combat_canvas.create_window(self.screen_width * 0.42, self.screen_height * 0.9, window=self.button_attaquer)
        self.combat_canvas.create_window(self.screen_width * 0.50, self.screen_height * 0.9, window=self.button_soin)
        self.combat_canvas.create_window(self.screen_width * 0.58, self.screen_height * 0.9, window=self.button_quitter)

        self.prochain_combat()

    # ---------- Reste de la classe identique ----------

    def prochain_combat(self):
        if self.game.ennemi_index < len(self.game.ennemis):
            ennemi = self.game.ennemis[self.game.ennemi_index]
            self.game.combat_en_cours = ennemi
        elif self.game.victoires == len(self.game.ennemis):
            self.game.combat_en_cours = self.game.boss
        else:
            messagebox.showinfo("Fin", "Vous avez vaincu tous les ennemis !")
            self.window.quit()
            return

        if self.enemy_sprite:
            self.combat_canvas.delete(self.enemy_sprite)
        img = self.enemy_imgs.get(self.game.combat_en_cours.nom)
        if img:
            enemy_x = int(self.screen_width * 0.75)
            enemy_y = int(self.screen_height * 0.65)
            self.enemy_sprite = self.combat_canvas.create_image(enemy_x, enemy_y, image=img)

        self.maj_interface()

    def maj_interface(self):
        self.label_stats.config(text=self.game.joueur.afficher_stats())
        if self.game.combat_en_cours:
            e = self.game.combat_en_cours
            self.label_ennemi.config(
                text=f"--- {e.nom} ---\nVie : {e.pv}\nAttaque : {e.attaque}\nDéfense : {e.defense}"
            )
        else:
            self.label_ennemi.config(text="Aucun ennemi en combat")

    def attaquer(self):
        if not self.game.combat_en_cours or not self.game.joueur.is_alive():
            return
        bonus = sum(o.get("attaque", 0) for o in self.game.joueur.inventaire)
        degats = self.game.joueur.attack_target(self.game.combat_en_cours, bonus)
        log = f"{self.game.joueur.nom} inflige {degats} dégâts à {self.game.combat_en_cours.nom}."
        if not self.game.combat_en_cours.is_alive():
            log += f"\n{self.game.combat_en_cours.nom} est vaincu !"
            self.button_attaquer.config(state="disabled")
            self.button_soin.config(state="disabled")
            self.game.victoires += 1
            self.game.ennemi_index += 1
            self.game.sauvegarder()
            self.game.joueur.pv = self.game.joueur.pv_max
            self.choix_objet()
        self.label_log.config(text=log)
        self.maj_interface()
        self.game.sauvegarder()
        self.game.joueur.reset_cooldowns()
        self.ennemi_attaque()

    def choix_objet(self):
        if self.choix_frame:
            self.choix_frame.destroy()
        self.choix_frame = tk.Frame(self.window, bg="#202020")
        self.combat_canvas.create_window(self.screen_width * 0.5, self.screen_height * 0.5, window=self.choix_frame)

        label = tk.Label(self.choix_frame, text="Choisissez un objet :", bg="#202020", fg="white")
        label.pack(pady=5)

        objets = self.game.generer_objets()
        for obj in objets:
            texte = f"{obj['nom']} : "
            if "attaque" in obj:
                texte += f"ATT+{obj['attaque']} "
            if "defense" in obj:
                texte += f"DEF+{obj['defense']} "
            if "pv" in obj:
                texte += f"PV+{obj['pv']} "
            b = tk.Button(self.choix_frame, text=texte, command=lambda o=obj: self.choisir_objet(o))
            b.pack(pady=3)



    def choisir_objet(self, obj):
        self.game.joueur.inventaire.append(obj)
        if "defense" in obj:
            self.game.joueur.defense += obj["defense"]
        if "pv" in obj:
            self.game.joueur.pv_max += obj["pv"]
        self.game.joueur.pv = self.game.joueur.pv_max

        if self.choix_frame:
            self.choix_frame.destroy()
            self.choix_frame = None

        self.maj_interface()
        self.button_attaquer.config(state="normal")
        self.button_soin.config(state="normal")
        self.prochain_combat()

    def soin(self):
        if not self.game.combat_en_cours or not self.game.joueur.is_alive():
            return
        if self.game.joueur.heal():
            log = f"{self.game.joueur.nom} se soigne de 20 PV."
            self.label_log.config(text=log)
            self.maj_interface()
            self.game.sauvegarder()
            self.game.joueur.reset_cooldowns()
            self.ennemi_attaque()
        else:
            self.label_log.config(
                text=f"Le sort de soin est en recharge ({self.game.joueur.cooldowns['soin']} tours restants)."
            )

    def ennemi_attaque(self):
        if not self.game.combat_en_cours or not self.game.joueur.is_alive():
            return
        log = self.game.combat_en_cours.attack_target(self.game.joueur)
        self.label_log.config(text=log)
        self.maj_interface()
        self.game.sauvegarder()
        if not self.game.joueur.is_alive():
            messagebox.showinfo("Défaite", f"{self.game.joueur.nom} a été vaincu !")
            self.button_attaquer.config(state="disabled")
            self.button_soin.config(state="disabled")
            self.window.quit()

    def quitter(self):
        self.game.sauvegarder()
        messagebox.showinfo("Sauvegarde", "Partie sauvegardée.")
        self.window.quit()

    def run(self):
        self.window.mainloop()



if __name__ == "__main__":
    app = GameGUI()
    app.run()
