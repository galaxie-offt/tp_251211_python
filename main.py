import random

# Ennemi et joueur (dictionnaire)
ennemi = {"nom": "Gobelin", "pv": 50, "attaque": 10, "defense": 5}

# Saisie des infos du joueur
nom = input("Entrez le nom de votre personnage : ")
pv = int(input("Entrez la vie de votre personnage : "))
attaque = int(input("Entrez l'attaque de votre personnage : "))
defense = int(input("Entrez la défense de votre personnage : "))

joueur = {
    "nom": nom,
    "pv": pv,
    "attaque": attaque,
    "defense": defense
}

while ennemi["pv"] > 0:
    print(f"\n--- Combat contre {ennemi['nom']} ---")
    print(f"{ennemi['nom']} : {ennemi['pv']} PV")
    print(f"{joueur['nom']} : {joueur['pv']} PV")

    # Tour du joueur
    action = input("Attaquer (a) ou fuir (f) ? ").lower()
    if action == "f":
        print(f"{joueur['nom']} fuit le combat.")
        break
    elif action != "a":
        print("Action invalide, réessayez.")
        continue

    # Calcul des dégâts du joueur
    degats = max(1, joueur["attaque"] - ennemi["defense"])
    ennemi["pv"] -= degats
    print(f"{joueur['nom']} inflige {degats} dégâts à {ennemi['nom']}.")

    # Vérification de la victoire
    if ennemi["pv"] <= 0:
        print(f"{ennemi['nom']} est vaincu !")
        break

    # Tour de l'ennemi
    try:
        degats_ennemi = max(1, ennemi["attaque"] - joueur["defense"])
        joueur["pv"] -= degats_ennemi
        print(f"{ennemi['nom']} inflige {degats_ennemi} dégâts à {joueur['nom']}.")
        if joueur["pv"] <= 0:
            print(f"{joueur['nom']} a été vaincu !")
            break
    except Exception as e:
        print(f"Erreur lors de l'attaque de l'ennemi : {e}")
        break
