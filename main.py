import json
import os
import random

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
        print(f"{self.nom} inflige {degats} dégâts à {target.nom}.")

    def heal(self, bonus=0):
        if self.cooldowns["soin"] > 0:
            print("Le sort de soin est en recharge.")
            return False
        soin = 20 + bonus
        self.pv = min(self.pv_max, self.pv + soin)
        print(f"{self.nom} se soigne de {soin} PV.")
        self.cooldowns["soin"] = 3
        return True

    def is_alive(self):
        return self.pv > 0

    def reset_cooldowns(self):
        for k in self.cooldowns:
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1

    def afficher_stats(self):
        print(f"\n--- Statistiques de {self.nom} ---")
        print(f"Vie : {self.pv}/{self.pv_max}")
        print(f"Attaque : {self.attaque}")
        print(f"Défense : {self.defense}")
        print(f"Inventaire : {[obj for obj in self.inventaire]}")


class Enemy(Character):
    def __init__(self, nom, pv, attaque, defense):
        super().__init__(nom, pv, attaque, defense)


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
            print(f"{self.nom} utilise une attaque simple et inflige {degats} dégâts.")
        elif choix == "ultime" and self.cooldowns["ultime"] == 0:
            degats = max(1, self.attaque * 2 - target.defense)
            target.pv -= degats
            print(f"{self.nom} utilise une attaque ultime et inflige {degats} dégâts !")
            self.cooldowns["ultime"] = 2
        elif choix == "soin" and self.cooldowns["soin"] == 0:
            soin = 25
            self.pv = min(self.pv_max, self.pv + soin)
            print(f"{self.nom} se soigne de {soin} PV.")
            self.cooldowns["soin"] = 3
        else:
            degats = max(1, self.attaque - target.defense)
            target.pv -= degats
            print(f"{self.nom} utilise une attaque simple et inflige {degats} dégâts.")


class GameEngine:
    def __init__(self):
        self.joueur = None
        self.ennemis = [
            Enemy("Gobelin", 50, 10, 5),
            Enemy("Orc", 70, 15, 8),
            Enemy("Troll", 100, 20, 12),
        ]
        self.boss = Boss("Dragon", 150, 25, 15)
        self.objets = {
            "Épée": {"attaque": 10},
            "Bouclier": {"defense": 10},
            "Armure": {"defense": 15},
            "Potion": {"pv": 20},
            "Amulette": {"attaque": 5, "defense": 5}
        }
        self.objets_donnes = []
        self.combat_en_cours = None
        self.victoires = 0
        self.ennemi_index = 0  # Index de l'ennemi à combattre

    def start_battle(self, ennemi):
        print(f"\n--- Combat contre {ennemi.nom} ---")
        while self.joueur.is_alive() and ennemi.is_alive():
            print(f"\n--- État actuel ---")
            print(f"{self.joueur.nom} : {self.joueur.pv}/{self.joueur.pv_max} PV")
            print(f"{ennemi.nom} : {ennemi.pv} PV")

            action = input("Attaquer (a), soigner (s), quitter (q) ? ").lower()
            if action == "q":
                print("Vous quittez le jeu.")
                self.sauvegarder()
                return False
            elif action == "s":
                self.joueur.heal()
            elif action == "a":
                bonus_attaque = sum(o.get("attaque", 0) for o in self.joueur.inventaire)
                self.joueur.attack_target(ennemi, bonus_attaque)
                if not ennemi.is_alive():
                    print(f"{ennemi.nom} est vaincu !")
                    self.victoires += 1
                    self.ennemi_index += 1  # Avance l'index après victoire
                    self.sauvegarder()
                    return True
            else:
                print("Action invalide, réessayez.")
                continue

            self.sauvegarder()

            ennemi.attack_target(self.joueur)
            self.sauvegarder()

            if not self.joueur.is_alive():
                print(f"{self.joueur.nom} a été vaincu !")
                break

            self.joueur.reset_cooldowns()
        return True

    def loot_objet(self):
        disponibles = [k for k in self.objets.keys() if k not in self.objets_donnes]
        if disponibles:
            loot = random.choice(disponibles)
            self.objets_donnes.append(loot)
            bonus = self.objets[loot]
            self.joueur.inventaire.append(bonus)
            print(f"Vous obtenez un(e) {loot} : {bonus}")
            if "attaque" in bonus:
                self.joueur.attaque += bonus["attaque"]
            if "defense" in bonus:
                self.joueur.defense += bonus["defense"]
            if "pv" in bonus:
                self.joueur.pv_max += bonus["pv"]

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
        print(f"Partie sauvegardée dans {nom_fichier}.")

    def charger(self, nom_fichier):
        try:
            with open(nom_fichier, "r") as f:
                data = json.load(f)
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
                    print("Ennemi non trouvé dans la liste.")
            else:
                self.combat_en_cours = None

            print(f"Partie chargée depuis {nom_fichier}.")
            return True
        except FileNotFoundError:
            print("Aucune sauvegarde trouvée.")
            return False

    def supprimer_sauvegarde(self, nom_fichier):
        if os.path.exists(nom_fichier):
            os.remove(nom_fichier)
            print(f"Sauvegarde {nom_fichier} supprimée.")


# --- Lancement du jeu ---
game = GameEngine()

# --- Gestion des sauvegardes ---
sauvegardes = [f for f in os.listdir() if f.startswith("sauvegarde_") and f.endswith(".json")]
if sauvegardes:
    print("Sauvegardes trouvées :")
    for s in sauvegardes:
        print(f" - {s}")
    choix = input("Nom du fichier de sauvegarde à charger (ou nouveau nom pour nouvelle partie) : ")
    if choix in sauvegardes:
        game.joueur = Character("", 1, 1, 1)
        game.charger(choix)
    else:
        nom = choix
        game.joueur = Character(nom, 100, 15, 10)
else:
    nom = input("Nom du personnage : ")
    game.joueur = Character(nom, 100, 15, 10)

# --- Boucle principale ---
for i in range(game.ennemi_index, len(game.ennemis)):
    ennemi = game.ennemis[i]
    game.combat_en_cours = ennemi
    game.joueur.afficher_stats()
    print(f"\n--- Nouveau combat contre {ennemi.nom} ---")
    if not game.start_battle(ennemi):
        break
    if not game.joueur.is_alive():
        break
    game.joueur.pv = game.joueur.pv_max
    game.loot_objet()
    game.sauvegarder()
    choix = input("Appuyez sur Entrée pour continuer ou q pour quitter : ")
    if choix.lower() == "q":
        break

# --- Combat contre le boss ---
if game.joueur.is_alive() and choix.lower() != "q" and game.victoires == len(game.ennemis):
    game.combat_en_cours = game.boss
    game.joueur.afficher_stats()
    print("\n--- Combat final contre le Dragon (Boss) ---")
    if game.start_battle(game.boss):
        if game.joueur.is_alive():
            print("Félicitations, vous avez vaincu le boss !")
            game.supprimer_sauvegarde(f"sauvegarde_{game.joueur.nom}.json")
