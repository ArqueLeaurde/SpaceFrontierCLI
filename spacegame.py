import random
import time
import sys

class Ressource:
    def __init__(self, nom, quantite):
        self.nom = nom
        self.quantite = quantite

class Planete:
    def __init__(self, nom):
        self.nom = nom
        self.taille = random.randint(7000, 10000)  
        self.ressources = [Ressource("Carburant", random.randint(1, 5))]
        self.colonisee = False
        self.visitee = False
        self.redevance = random.randint(1, 3)  
        self.besoin_carburant = random.randint(1, 5)
        self.besoin_gold = random.randint(5, 10)
        self.prix_carburant = random.randint(2, 6)  
        self.missions = [Mission(random.choice(["Transport", "Chasse", "Collecte"]), random.randint(15, 30), random.randint(0, 9)) for _ in range(2)]

    def coloniser(self, vaisseau):
        if not self.colonisee and vaisseau.carburant >= self.besoin_carburant and vaisseau.space_gold >= self.besoin_gold:
            vaisseau.carburant -= self.besoin_carburant
            vaisseau.space_gold -= self.besoin_gold
            self.colonisee = True
            print(f"La planète {self.nom} est colonisée ! Vous gagnez {self.redevance} Galactic Gold par tour.")
        else:
            print(f"Impossible de coloniser {self.nom}. Besoin de {self.besoin_carburant} carburant et {self.besoin_gold} Galactic Gold.")

class Vaisseau:
    def __init__(self):
        self.carburant = 15  
        self.space_gold = 10
        self.ressources = []
        self.efficacite = 1.0 
        self.moteur_eco_niveau = 0  # Max 2 levels
        self.armes_plasma_niveau = 0  # Max 3 levels

    def collecter_ressources(self, planete):
        if planete.ressources:
            for ressource in planete.ressources:
                self.ressources.append(ressource)
            print(f"Ressources collectées sur {planete.nom}.")
            planete.ressources = []
            self.space_gold += 5
            print(f"Vous avez gagné 5 Galactic Gold pour la collecte.")
        else:
            print("Pas de ressources disponibles.")

    def ameliorer(self):
        print("\n🔧 Améliorations disponibles :")
        print(f"1. Moteur économique (Niveau {self.moteur_eco_niveau}/2) - Réduit la consommation de carburant.")
        print(f"   Coût : {20 + self.moteur_eco_niveau * 10} GG")
        print(f"2. Armes à plasma (Niveau {self.armes_plasma_niveau}/3) - Réduit l’écart cible en chasse.")
        print(f"   Coût : {25 + self.armes_plasma_niveau * 15} GG")

        choix = input("\nQuel upgrade souhaitez-vous acheter ? (1/2) : ")
        
        if choix == "1" and self.moteur_eco_niveau < 2:
            cost = 20 + self.moteur_eco_niveau * 10
            if self.space_gold >= cost:
                self.space_gold -= cost
                self.moteur_eco_niveau += 1
                self.efficacite *= 0.8  # Less fuel consumption
                print("🚀 Moteur économique amélioré ! Consommation de carburant réduite.")
            else:
                print("❌ Pas assez de Galactic Gold !")

        elif choix == "2" and self.armes_plasma_niveau < 3:
            cost = 25 + self.armes_plasma_niveau * 15
            if self.space_gold >= cost:
                self.space_gold -= cost
                self.armes_plasma_niveau += 1
                print("🔫 Armes à plasma améliorées ! Viser est plus facile en chasse.")
            else:
                print("❌ Pas assez de Galactic Gold !")
        else:
            print("❌ Amélioration impossible.")


class Mission:
    def __init__(self, type_mission, recompense, cible):
        self.type_mission = type_mission
        self.recompense = recompense
        self.cible = cible

    def accomplir(self, vaisseau, position_actuelle):
        if self.type_mission == "Transport":
            self.minigame_transport(vaisseau)
        elif self.type_mission == "Chasse":
            self.minigame_chasse(vaisseau)
        elif self.type_mission == "Collecte":
            self.minigame_collecte(vaisseau)

    def minigame_transport(self, vaisseau):
        print("🚀 Mini-jeu Transport : Appuyez sur ENTER lorsque le compteur atteint 0 !")
        
        # Affichage progressif du compteur
        for i in range(3, -1, -1):  
            sys.stdout.write(f"\r⏳ {i} ")  # Affichage sur la même ligne
            sys.stdout.flush()
            time.sleep(1)  
        
        print("\nGO!")  
        start_time = time.time()
        input()  # Le joueur appuie sur ENTER
        reaction_time = time.time() - start_time

        if 0.8 <= reaction_time <= 1.2:
            print(f"✅ Mission réussie ! Vous gagnez {self.recompense} Galactic Gold.")
            vaisseau.space_gold += self.recompense
        else:
            print("❌ Mission échouée ! Trop lent ou trop rapide.")
            
    def minigame_chasse(self, vaisseau):
        print("🎯 Mini-jeu Chasse : Trouvez le bon numéro entre 1 et 10 !")
        target_range = max(1, 10 - vaisseau.armes_plasma_niveau)  # Reduces target range
        target = random.randint(1, target_range)
        for _ in range(3):
            guess = int(input(f"Votre tir (1-{target_range}) : "))
            if guess == target:
                print(f"💥 Touché ! Mission réussie. Vous gagnez {self.recompense} Galactic Gold.")
                vaisseau.space_gold += self.recompense
                return
            else:
                print("❌ Raté ! Essayez encore.")
        print("😞 Mission échouée ! Le vaisseau ennemi a fui.")


    def minigame_collecte(self, vaisseau):
        print("🧠 Mini-jeu Collecte : Mémorisez cette séquence de nombres !")
        sequence = [random.randint(1, 9) for _ in range(5)]
        print("Séquence : " + " ".join(map(str, sequence)))
        time.sleep(3)
        print("\n" * 50)
        reponse = input("Entrez la séquence (séparée par des espaces) : ").strip()
        if reponse == " ".join(map(str, sequence)):
            print(f"✅ Bonne mémoire ! Mission réussie. Vous gagnez {self.recompense} Galactic Gold.")
            vaisseau.space_gold += self.recompense
        else:
            print("❌ Mauvaise réponse ! Mission échouée.")

def generer_nom_planete():
    prefixes = ["Zeta", "Alpha", "Gamma", "Delta", "Theta", "Kappa"]
    suffixes = ["Prime", "X", "Beta", "Nova", "Terra"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def boucle_de_jeu():
    vaisseau = Vaisseau()
    planetes = [Planete(generer_nom_planete()) for _ in range(15)]  # 15 planètes normales
    boss_planete = Planete("Omega Nexus")  # Boss final
    planetes.append(boss_planete)  # Ajout en dernière position
    position_actuelle = 0
    distance_seuil_boss = 12  # Distance avant de n'avoir que le boss en option

    while vaisseau.carburant > 0:
        # Calcul des revenus passifs basés sur les planètes colonisées
        revenu_passif = sum(p.redevance for p in planetes if p.colonisee)
        planete = planetes[position_actuelle]
        print(f"\n🚀 Vous êtes sur {planete.nom}. ⛽ Carburant: {vaisseau.carburant} | 💰 Galactic Gold: {vaisseau.space_gold} (+{revenu_passif} GG/tour)")
        planete.visitee = True

        print(f"1. Prendre une mission")
        print(f"2. Coloniser {planete.nom}" if not planete.colonisee else "")
        print(f"3. Collecter des ressources")
        print(f"4. Voyager vers une autre planète")
        print(f"5. Acheter du carburant ({planete.prix_carburant} GG/unité)")
        print(f"6. Améliorer le vaisseau")

        choix = input("Votre action : ")
        action_effectuee = False  # ✅ Permet de gérer les gains correctement

        if choix == "1":
            if planete.missions:
                mission = planete.missions.pop(0)
                mission.accomplir(vaisseau, position_actuelle)
                action_effectuee = True  # ✅ Une mission a été effectuée
            else:
                print("Aucune mission disponible.")

        elif choix == "2" and not planete.colonisee:
            planete.coloniser(vaisseau)
            action_effectuee = True  # ✅ Colonisation effectuée

        elif choix == "3":
            vaisseau.collecter_ressources(planete)
            action_effectuee = True  # ✅ Ressources collectées

        elif choix == "4":
            print("\n🌍 Planètes disponibles pour le voyage :")
            destinations_possibles = []

            if position_actuelle >= distance_seuil_boss:
                print("\n⚠️  Une présence mystérieuse perturbe les systèmes du vaisseau...")
                time.sleep(2)
                print("📡 Un signal inconnu intercepte vos communications...")
                time.sleep(2)
                print(f"🔴 Destination verrouillée : {boss_planete.nom} (Distance: {abs(len(planetes) - 1 - position_actuelle)})")
                destinations_possibles.append(len(planetes) - 1) # Uniquement le boss
            else:
                distances = random.sample(range(1, 4), min(3, len(planetes) - position_actuelle - 1))
                for d in distances:
                    destination_index = min(position_actuelle + d, len(planetes) - 1)
                    destinations_possibles.append(destination_index)

                for i, idx in enumerate(destinations_possibles):
                    print(f"{i}. {planetes[idx].nom} (Distance: {abs(idx - position_actuelle)})")

            choix_planete = int(input("\n🔭 Entrez le numéro de la planète cible : "))
            if 0 <= choix_planete < len(destinations_possibles):
                cible = destinations_possibles[choix_planete]
                cout = int(abs(cible - position_actuelle) * vaisseau.efficacite)

                if vaisseau.carburant >= cout:
                    print("\n🚀 Préparation au décollage...")
                    time.sleep(1)
                    print("\n✨ Voyage interstellaire en cours...\n")
                    time.sleep(1)

                    print(f"\n🌍 Arrivée sur {planetes[cible].nom} !")
                    position_actuelle = cible
                    vaisseau.carburant -= cout
                    action_effectuee = True  # ✅ Voyage effectué
                else:
                    print("⛽ Pas assez de carburant pour ce voyage !")

        elif choix == "5":
            max_achat = vaisseau.space_gold // planete.prix_carburant
            if max_achat > 0:
                quantite = int(input(f"Combien d'unités de carburant souhaitez-vous acheter ? (Max {max_achat}) : "))
                if 0 < quantite <= max_achat:
                    vaisseau.space_gold -= quantite * planete.prix_carburant
                    vaisseau.carburant += quantite
                    print(f"⛽ Vous avez acheté {quantite} unités de carburant.")
                    action_effectuee = True  # ✅ Achat effectué
                else:
                    print("❌ Achat annulé ou quantité invalide.")
            else:
                print("❌ Pas assez de Galactic Gold pour acheter du carburant !")

        elif choix == "6":
            vaisseau.ameliorer()
            action_effectuee = True  # ✅ Amélioration effectuée

        # ✅ Appliquer les revenus des planètes colonisées **seulement si une action a été faite**
        if action_effectuee:
            for p in planetes:
                if p.colonisee:
                    vaisseau.space_gold += p.redevance

    print("💥 Plus de carburant ! Fin du jeu.")


def combat_final(vaisseau):
    print("\n⚠️ ALERTE : Vous êtes arrivé sur Omega Nexus !")
    print("Un ennemi redoutable, le Seigneur Galactique Xypher, vous attend pour un combat final ! ⚔️")
    
    boss_hp = 50
    joueur_hp = 30 + vaisseau.armes_plasma_niveau * 5  # Plus d'améliorations = plus de vie
    boss_attack_counter = 0  # Pour gérer les attaques spéciales du boss

    while boss_hp > 0 and joueur_hp > 0:
        print(f"\n🔥 Xypher: {boss_hp} HP  |  🛡️ Votre vaisseau: {joueur_hp} HP")
        print("1. Attaque laser (5-10 dégâts)")
        print("2. Tir plasma (7-15 dégâts, plus efficace avec amélioration)")
        print("3. Défense (réduit les dégâts du boss)")
        print("4. Attaque spéciale (Peut infliger 20-30 dégâts mais consomme des ressources)")

        choix = input("Que faites-vous ? ")

        if choix == "1":
            degats = random.randint(5, 10)
            boss_hp -= degats
            print(f"💥 Vous infligez {degats} dégâts !")
        elif choix == "2":
            degats = random.randint(7, 15) + vaisseau.armes_plasma_niveau * 2
            boss_hp -= degats
            print(f"🔫 Vous infligez {degats} dégâts avec vos armes à plasma !")
        elif choix == "3":
            print("🛡️ Vous vous protégez, réduisant les dégâts du boss ce tour.")
            joueur_hp += 5  # Un petit bonus de défense
        elif choix == "4":
            if vaisseau.space_gold >= 10:  # Consomme des Galactic Gold pour activer l'attaque spéciale
                vaisseau.space_gold -= 10
                degats = random.randint(20, 30)
                boss_hp -= degats
                print(f"⚡ Attaque spéciale ! Vous infligez {degats} dégâts à Xypher !")
            else:
                print("❌ Pas assez de Galactic Gold pour utiliser l'attaque spéciale.")
        else:
            print("❌ Choix invalide !")
            continue

        # Attaque du boss
        boss_degats = random.randint(5, 12)
        joueur_hp -= boss_degats
        print(f"💀 Xypher vous attaque et inflige {boss_degats} dégâts !")
        
        # Si le boss est à moins de 20% de sa vie, il passe à la phase 2
        if boss_hp <= 10 and boss_attack_counter == 0:
            print("\n⚠️ Phase 2 : Xypher se transforme ! Ses attaques sont plus puissantes !")
            boss_attack_counter += 1  # On passe à la phase 2

            # Augmenter les dégâts de Xypher et lui donner des capacités spéciales
            boss_degats += 3  # Augmenter les dégâts de Xypher

        if joueur_hp <= 0:
            print("\n💀 GAME OVER... Xypher a détruit votre vaisseau.")
            break

    if joueur_hp > 0:
        print("\n🏆 🎉 VICTOIRE ! Vous avez vaincu Xypher et sauvé la galaxie !")


boucle_de_jeu()