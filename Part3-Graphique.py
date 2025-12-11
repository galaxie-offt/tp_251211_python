import tkinter as tk
from tkinter import messagebox
import json
import os
import random

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
        self.window.geometry("600x500")
        self.create_widgets()
        self.load_saves()

    def create_widgets(self):
        self.label_joueur = tk.Label(self.window, text="Nom du personnage :")
        self.label_joueur.pack(pady=10)
        self.entry_nom = tk.Entry(self.window)
        self.entry_nom.pack()

        self.label_classe = tk.Label(self.window, text="Choisissez une classe :")
        self.label_classe.pack(pady=10)

        self.classe_var = tk.StringVar()
        for classe in CLASSES.keys():
            rb = tk.Radiobutton(self.window, text=classe, variable=self.classe_var, value=classe)
            rb.pack()

        self.button_nouveau = tk.Button(self.window, text="Nouvelle partie", command=self.nouvelle_partie)
        self.button_nouveau.pack(pady=5)
        self.button_charger = tk.Button(self.window, text="Charger une sauvegarde", command=self.charger_partie)
        self.button_charger.pack(pady=5)
        self.sauvegardes_liste = tk.Listbox(self.window)
        self.sauvegardes_liste.pack(pady=10)
        self.button_supprimer = tk.Button(self.window, text="Supprimer une sauvegarde", command=self.supprimer_sauvegarde)
        self.button_supprimer.pack(pady=5)

        self.combat_frame = tk.Frame(self.window)
        self.combat_frame.pack_forget()
        self.choix_frame = tk.Frame(self.window)
        self.choix_frame.pack_forget()

    def load_saves(self):
        sauvegardes = [f for f in os.listdir() if f.startswith("sauvegarde_") and f.endswith(".json")]
        self.sauvegardes_liste.delete(0, tk.END)
        for s in sauvegardes:
            self.sauvegardes_liste.insert(tk.END, s)

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

    def start_game(self):
        # Masquer les widgets du menu
        self.label_joueur.pack_forget()
        self.entry_nom.pack_forget()
        self.label_classe.pack_forget()
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.pack_forget()
        self.button_nouveau.pack_forget()
        self.button_charger.pack_forget()
        self.sauvegardes_liste.pack_forget()
        self.button_supprimer.pack_forget()

        # Créer et afficher les widgets du combat
        self.combat_frame.pack()

        # Créer les labels si ce n’est pas déjà fait
        if not hasattr(self, 'label_stats'):
            self.label_stats = tk.Label(self.combat_frame, text="", justify="left")
            self.label_stats.pack(pady=10)
        if not hasattr(self, 'label_ennemi'):
            self.label_ennemi = tk.Label(self.combat_frame, text="", justify="left")
            self.label_ennemi.pack(pady=10)
        if not hasattr(self, 'label_log'):
            self.label_log = tk.Label(self.combat_frame, text="", justify="left")
            self.label_log.pack(pady=10)

        # Créer les boutons si ce n’est pas déjà fait
        if not hasattr(self, 'button_attaquer'):
            self.button_attaquer = tk.Button(self.combat_frame, text="Attaquer", command=self.attaquer)
            self.button_attaquer.pack(pady=5)
        if not hasattr(self, 'button_soin'):
            self.button_soin = tk.Button(self.combat_frame, text="Soigner", command=self.soin)
            self.button_soin.pack(pady=5)
        if not hasattr(self, 'button_quitter'):
            self.button_quitter = tk.Button(self.combat_frame, text="Quitter", command=self.quitter)
            self.button_quitter.pack(pady=5)

        self.prochain_combat()

    def prochain_combat(self):
        if self.game.ennemi_index < len(self.game.ennemis):
            ennemi = self.game.ennemis[self.game.ennemi_index]
            self.game.combat_en_cours = ennemi
            self.maj_interface()
        elif self.game.victoires == len(self.game.ennemis):
            self.game.combat_en_cours = self.game.boss
            self.maj_interface()
        else:
            messagebox.showinfo("Fin", "Vous avez vaincu tous les ennemis !")
            self.window.quit()

    def maj_interface(self):
        self.label_stats.config(text=self.game.joueur.afficher_stats())
        if self.game.combat_en_cours:
            self.label_ennemi.config(text=f"--- {self.game.combat_en_cours.nom} ---\nVie : {self.game.combat_en_cours.pv}\nAttaque : {self.game.combat_en_cours.attaque}\nDéfense : {self.game.combat_en_cours.defense}")
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
            self.game.victoires += 1
            self.game.ennemi_index += 1
            self.game.sauvegarder()
            # Régénération complète avant le choix d'objet
            self.game.joueur.pv = self.game.joueur.pv_max
            self.choix_objet()
        self.label_log.config(text=log)
        self.maj_interface()
        self.game.sauvegarder()
        self.game.joueur.reset_cooldowns()
        self.ennemi_attaque()

    def choix_objet(self):
        self.combat_frame.pack_forget()
        self.choix_frame.pack()
        self.choix_frame.destroy()
        self.choix_frame = tk.Frame(self.window)
        self.choix_frame.pack()
        objets = self.game.generer_objets()
        for i, obj in enumerate(objets):
            texte = f"{obj['nom']} : "
            if "attaque" in obj:
                texte += f"attaque {obj['attaque']} "
            if "defense" in obj:
                texte += f"défense {obj['defense']} "
            if "pv" in obj:
                texte += f"PV {obj['pv']} "
            bouton = tk.Button(self.choix_frame, text=texte, command=lambda o=obj: self.choisir_objet(o))
            bouton.pack(pady=5)

    def choisir_objet(self, obj):
        self.game.joueur.inventaire.append(obj)
        if "defense" in obj:
            self.game.joueur.defense += obj["defense"]
        if "pv" in obj:
            self.game.joueur.pv_max += obj["pv"]
        # Toujours full vie après le choix d'objet
        self.game.joueur.pv = self.game.joueur.pv_max

        self.choix_frame.pack_forget()
        self.combat_frame.pack()
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
            self.label_log.config(text=f"Le sort de soin est en recharge ({self.game.joueur.cooldowns['soin']} tours restants).")

    def ennemi_attaque(self):
        if not self.game.combat_en_cours or not self.game.joueur.is_alive():
            return
        log = self.game.combat_en_cours.attack_target(self.game.joueur)
        self.label_log.config(text=log)
        self.maj_interface()
        self.game.sauvegarder()
        if not self.game.joueur.is_alive():
            messagebox.showinfo("Défaite", f"{self.game.joueur.nom} a été vaincu !")
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
