import random

class Character:
    def __init__(self, nom, pv, attaque, defense):
        self.nom = nom
        self.pv = pv
        self.attaque = attaque
        self.defense = defense

    def attack_target(self, target):
        degats = max(1, self.attaque - target.defense)
        target.pv -= degats
        print(f"{self.nom} inflige {degats} dégâts à {target.nom}.")

    def is_alive(self):
        return self.pv > 0

class Enemy(Character):
    def __init__(self, nom, pv, attaque, defense):
        super().__init__(nom, pv, attaque, defense)

class GameEngine:
    def __init__(self, joueur, ennemi):
        self.joueur = joueur
        self.ennemi = ennemi

    def start_battle(self):
        print(f"Combat entre {self.joueur.nom} et {self.ennemi.nom} !")
        while self.joueur.is_alive() and self.ennemi.is_alive():
            print(f"\n--- État actuel ---")
            print(f"{self.joueur.nom} : {self.joueur.pv} PV")
            print(f"{self.ennemi.nom} : {self.ennemi.pv} PV")

            action = input("Attaquer (a) ou fuir (f) ? ").lower()
            if action == "f":
                print(f"{self.joueur.nom} fuit le combat.")
                break
            elif action != "a":
                print("Action invalide, réessayez.")
                continue

            # Tour du joueur
            self.joueur.attack_target(self.ennemi)
            if not self.ennemi.is_alive():
                print(f"{self.ennemi.nom} est vaincu !")
                break

            # Tour de l'ennemi
            self.ennemi.attack_target(self.joueur)
            if not self.joueur.is_alive():
                print(f"{self.joueur.nom} a été vaincu !")
                break

class LootSystem:
    def __init__(self):
        self.equipements = ["Épée", "Bouclier", "Armure", "Potion"]
        self.bonus = [10, 15, 20, 5]

    def drop_loot(self):
        loot = random.choice(self.equipements)
        bonus = random.choice(self.bonus)
        print(f"Vous obtenez un(e) {loot} avec un bonus de {bonus} !")
        return loot, bonus

# Création des personnages
nom = input("Nom du personnage : ")
pv = int(input("Vie : "))
attaque = int(input("Attaque : "))
defense = int(input("Défense : "))
joueur = Character(nom, pv, attaque, defense)

# Création de l'ennemi
nom_ennemi = input("Nom de l'ennemi : ")
pv_ennemi = int(input("Vie de l'ennemi : "))
attaque_ennemi = int(input("Attaque de l'ennemi : "))
defense_ennemi = int(input("Défense de l'ennemi : "))
ennemi = Enemy(nom_ennemi, pv_ennemi, attaque_ennemi, defense_ennemi)

# Lancer le combat
game = GameEngine(joueur, ennemi)
game.start_battle()

# Loot à la fin du combat
if not ennemi.is_alive():
    loot_system = LootSystem()
    loot_system.drop_loot()
