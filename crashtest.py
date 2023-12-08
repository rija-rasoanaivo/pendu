import pygame # Importation du module Pygame
import pygame_menu # Importation du module pygame_menu
import random # Importation du module random
from pygame.locals import * # Importation des constantes de Pygame

# Initialisation de Pygame
pygame.init() # Initialise les modules Pygame
screen = pygame.display.set_mode((900, 600)) # Crée une fenêtre de 800x600 pixels
clock = pygame.time.Clock() # Crée un objet pour aider à gérer le temps

# Définition des couleurs
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

def convert_to_lowercase(file_name):
    with open(file_name, 'r') as file:
        content = file.read()  # Lire le contenu du fichier

    # Convertir le contenu en minuscules
    content_lower = content.lower()

    with open(file_name, 'w') as file:
        file.write(content_lower)  # Réécrire le fichier avec le texte converti en minuscules

def capture_text():
    text = ''
    font = pygame.font.Font( None, 36)
    input_box = pygame.Rect(300, 300, 140, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False

    while True:
        for event in pygame.event.get(): # Pour chaque événement Pygame #pygame.event.get() permet de récupérer les événements Pygame
            if event.type == pygame.QUIT: # Si l'événement est de type 'QUIT' (fermeture de la fenêtre) 
                pygame.quit() # Ferme la fenêtre Pygame #pygame.quit() permet de fermer la fenêtre Pygame
                quit() # Quitte le programme #quit() permet de quitter le programme
            if event.type == pygame.MOUSEBUTTONDOWN: # Si l'événement est de type 'MOUSEBUTTONDOWN' (appui sur un bouton de la souris)
                if input_box.collidepoint(event.pos): # Si le clic est sur la zone de saisie #.collidepoint permet de vérifier si un point est dans un rectangle #event.pos est la position du clic
                    active = not active # Change l'état de la zone de saisie #not permet de changer l'état de la zone de saisie
                else:
                    active = False # Désactive la zone de saisie
                color = color_active if active else color_inactive 
            if event.type == pygame.KEYDOWN: # Si l'événement est de type 'KEYDOWN' (appui sur une touche)
                if active:
                    if event.key == pygame.K_RETURN:
                        with open("mots.txt", "a") as file: # Ouvre le fichier 'mot.txt' en mode écriture #a permet d'ajouter du texte à la fin du fichier
                            file.write("\n" + text) # Ajoute le texte à la fin du fichier #\n permet de passer à la ligne suivante
                        print(f"Le mot '{text}' a été ajouté à la liste.")
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((WHITE))

        add_text_surface = font.render("Ajouter un mot :", True, BLACK)
        screen.blit(add_text_surface, (300, 250))

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)

def set_difficulty(value, difficulty):
    global mots, lettres_tapees  # Pour accéder à ces variables globales

    # Charger les mots depuis le fichier 'mot.txt'
    with open("mots.txt", "r") as file:
        all_words = file.read().split()  # Lire tous les mots du fichier

    if difficulty == 1:  # Difficulté difficile (mots de plus de 10 lettres)
        mots = [word.lower() for word in all_words if len(word) > 10]
    elif difficulty == 2:  # Difficulté facile (mots de moins de 10 lettres)
        mots = [word.lower() for word in all_words if len(word) <= 10]

    lettres_tapees = set()  # Réinitialiser les lettres tapées

# Modifier la fonction add_word_to_list pour lancer la capture de texte
def add_word_to_list():
    capture_text()


def start_the_game():# Chargement des mots depuis le fichier 'mot.txt'
    with open("mots.txt", "r") as file: # Ouvre le fichier 'mot.txt' en mode lecture
        mots = file.read().split() # Lit le contenu du fichier et le stocke dans une liste 'mots'

    # Choix aléatoire d'un mot dans la liste de mots
    mot = random.choice(mots) # Sélectionne un mot au hasard dans la liste 'mots'
    print(f"Le mot à deviner est : {mot}") # Affiche le mot à deviner dans la console

    # Initialisation des variables
    lettres_verifiees = set() # Crée un ensemble vide pour stocker les lettres déjà vérifiées
    nb_essais = 11 # Initialise le nombre d'essais à 11

    # Définition des éléments du pendu
    elements_pendu = [ # Crée une liste d'éléments du pendu #elements_pendu est une liste de fonctions
        lambda: pygame.draw.rect(screen, BLACK, (100, 350, 300, 2)),#sol 
        lambda: pygame.draw.rect(screen, BLACK, (175, 50, 2, 300)),#verticale
        lambda: pygame.draw.rect(screen, BLACK, (175, 50, 200, 2)),#horizontale
        lambda: pygame.draw.line(screen, BLACK, (175, 100), (200, 50), 2), #diagonale
        lambda: pygame.draw.rect(screen, MAGENTA, (375, 50, 2, 50)),#corde
        lambda: pygame.draw.ellipse(screen, RED, (350, 100, 50, 50), 1),#tête
        lambda: pygame.draw.rect(screen, RED, (375, 150, 1, 100)),#corp
        lambda: pygame.draw.line(screen, RED, (375, 175), (340, 150), 1),#bras gauche
        lambda: pygame.draw.line(screen, RED, (375, 175), (410, 150), 1),#bras droit
        lambda: pygame.draw.line(screen, RED, (375, 250), (340, 275), 1),#jambe gauche
        lambda: pygame.draw.line(screen, RED, (375, 250), (410, 275), 1)#jambe droite
    ] # lambda est une fonction anonyme qui permet de stocker des fonctions dans une liste #pygame draw permet de dessiner des formes

    # Fonction pour dessiner le pendu
    def dessiner_pendu(essais_restants): # Définit une fonction qui prend en paramètre le nombre d'essais restants
        for i in range(11 - essais_restants): # Pour chaque élément du pendu à dessiner #i est un compteur qui va de 0 à 11 - essais_restants 
            elements_pendu[i]() # Dessine l'élément du pendu #[i] permet de parcourir la liste #() permet d'appeler la fonction #elements_pendu[i] est une fonction

    # Charger une police pour le texte
    font = pygame.font.Font(None, 36) #pygame.font.Font permet de charger une police #None est la police par défaut #36 est la taille de la police 

    lettres_tapees = set() # Crée un ensemble vide pour stocker les lettres déjà tapées

    # Boucle principale du jeu
    running = True # Définit une variable pour savoir si le jeu est en cours d'exécution #True signifie que le jeu est en cours d'exécution
    while running: # Tant que le jeu est en cours d'exécution 
        screen.fill(WHITE) # Remplit l'écran avec la couleur blanche 
        for event in pygame.event.get(): # Pour chaque événement Pygame #pygame.event.get() permet de récupérer les événements Pygame
            if event.type == pygame.QUIT: # Si l'événement est de type 'QUIT' (fermeture de la fenêtre)
                running = False # Met la variable 'running' à False (le jeu ne sera plus en cours d'exécution)

            # Capture des événements de saisie
            if event.type == pygame.KEYDOWN: # Si l'événement est de type 'KEYDOWN' (appui sur une touche) #pygame.KEYDOWN est une constante 
                if event.key >= pygame.K_a and event.key <= pygame.K_z: # Si la touche appuyée est une lettre de l'alphabet #pygame.K_a et pygame.K_z sont des constantes qui représentent les touches du clavier
                    lettre = chr(event.key) # Récupère la lettre correspondant à la touche appuyée #chr permet de récupérer le caractère correspondant au code ASCII #event.key est un code ASCII
                    if lettre not in lettres_tapees: # Si la lettre n'a pas déjà été tapée
                        lettres_tapees.add(lettre) # Ajoute la lettre à l'ensemble des lettres tapées #.add permet d'ajouter un élément à un ensemble
                    lettres_verifiees.add(lettre) # Ajoute la lettre à l'ensemble des lettres vérifiées #.add permet d'ajouter un élément à un ensemble
                    if lettre not in mot: # Si la lettre n'est pas dans le mot à deviner
                        nb_essais -= 1 # Décrémente le nombre d'essais restants #nb_essais = nb_essais - 1
        mot_a_afficher = ''.join([lettre if lettre in lettres_verifiees else '_ ' for lettre in mot]) # Crée une chaîne de caractères à partir des lettres vérifiées #.join permet de concaténer les éléments d'une liste #lettre if lettre in lettres_verifiees else '_' for lettre in mot est une compréhension de liste #lettre if lettre in lettres_verifiees else '_' est une expression conditionnelle #lettre est une variable qui prend successivement les valeurs de la liste mot #lettre if lettre in lettres_verifiees else '_' est une expression conditionnelle qui renvoie lettre si lettre est dans lettres_verifiees et '_' sinon #for lettre in mot permet de parcourir la liste mot
        
        # Affichage du texte
        text = font.render(f"Tu as {nb_essais} essais. Devine une lettre : {mot_a_afficher}", True, BLACK) # Crée un objet 'text' qui contient le texte à afficher #font.render permet de créer un objet texte #f permet d'insérer des variables dans une chaîne de caractères #text est le texte à afficher #True permet d'activer l'antialiasing #BLACK est la couleur du texte
        screen.blit(text, (20, 490)) # Affiche le texte en haut à gauche de l'écran #.blit permet d'afficher un texte ou une image à l'écran #text est le texte à afficher #(100, 500) est la position du texte à l'écran
        text_lettres_tapees = font.render(f"Lettres tapées : {' '.join(sorted(lettres_tapees))}", True, BLACK) # Crée un objet 'text_lettres_tapees' qui contient le texte à afficher #font.render permet de créer un objet texte #f permet d'insérer des variables dans une chaîne de caractères #text_lettres_tapees est le texte à afficher #True permet d'activer l'antialiasing #BLACK est la couleur du texte
        screen.blit(text_lettres_tapees, (20, 460)) # Affiche le texte en bas à gauche de l'écran #.blit permet d'afficher un texte ou une image à l'écran #text est le texte à afficher #(100, 500) est la position du texte à l'écran

        if nb_essais == 0: # Si le nombre d'essais est égal à 0
            text_end = font.render(f"Dommage... Le mot était '{mot}'. Voulez-vous rejouer ? (o/n)", True, RED) # Crée un objet 'text_end' qui contient le texte à afficher #RED est la couleur du texte
            text_retour_menu = font.render(f"Revenir au menu ? (m)", True, BLACK) # Crée un objet 'text_retour_menu' qui contient le texte à afficher #BLACK est la couleur du texte
            screen.blit(text_end, (20, 400)) # Affiche le texte au centre à gauche de l'écran
            screen.blit(text_retour_menu, (20, 430)) # Affiche le texte au centre à gauche de l'écran
            pygame.display.flip() # Met à jour l'affichage
            wait_for_input = True # Définit une variable pour savoir si on attend une entrée de l'utilisateur #True signifie qu'on attend une entrée de l'utilisateur
            while wait_for_input: # Tant qu'on attend une entrée de l'utilisateur
                for event in pygame.event.get(): # Pour chaque événement Pygame
                    if event.type == pygame.KEYDOWN: # Si l'événement est de type 'KEYDOWN' (appui sur une touche)
                        if event.key == pygame.K_o:  # Appuyer sur la touche 'o' pour recommencer #pygame.K_o est une constante qui représente la touche 'o'
                            mot = random.choice(mots) # Sélectionne un mot au hasard dans la liste 'mots'
                            lettres_verifiees = set() # Réinitialise l'ensemble des lettres vérifiées
                            nb_essais = 11 # Réinitialise le nombre d'essais restants
                            lettres_tapees = set() # Réinitialise l'ensemble des lettres tapées
                            wait_for_input = False # Met la variable 'wait_for_input' à False (on ne doit plus attendre une entrée de l'utilisateur)
                        elif event.key == pygame.K_n:  # Appuyer sur la touche 'n' pour quitter #pygame.K_n est une constante qui représente la touche 'n'
                            running = False  # Met la variable 'running' à False (le jeu ne sera plus en cours d'exécution)
                            wait_for_input = False # Met la variable 'wait_for_input' à False (on ne doit plus attendre une entrée de l'utilisateur)
                        elif event.key == pygame.K_m: # Appuyer sur la touche 'm' pour revenir au menu
                            running = False # Met la variable 'running' à False (le jeu ne sera plus en cours d'exécution)
                            return # Retourne au menu
        elif mot_a_afficher == mot: 
            text_end = font.render(f"Bravo! Voulez-vous rejouer ? (o/n)", True, GREEN)
            text_retour_menu = font.render(f"Revenir au menu ? (m)", True, BLACK)
            screen.blit(text_end, (20, 400))
            screen.blit(text_retour_menu, (20, 430))
            pygame.display.flip()
            wait_for_input = True
            while wait_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_o:  # Appuyer sur la touche 'o' pour recommencer
                            mot = random.choice(mots)
                            lettres_verifiees = set()
                            nb_essais = 11
                            lettres_tapees = set()
                            wait_for_input = False
                        elif event.key == pygame.K_n:  # Appuyer sur la touche 'n' pour quitter
                            running = False
                            wait_for_input = False
                        elif event.key == pygame.K_m: # Appuyer sur la touche 'm' pour revenir au menu
                            running = False # Met la variable 'running' à False (le jeu ne sera plus en cours d'exécution)
                            return # Retourne au menu
        dessiner_pendu(nb_essais) # Dessine le pendu

        pygame.display.flip() # Met à jour l'affichage
        clock.tick(60) # Attend 1/60ème de seconde #clock.tick permet de gérer le temps #60 est le nombre d'images par seconde

    pygame.quit()  # Ferme la fenêtre Pygame lorsque la boucle se termine

menu = pygame_menu.Menu('Jeu du pendu', 400, 300, #pygame_menu.Menu permet de créer un menu #400 est la largeur du menu #300 est la hauteur du menu
                       theme=pygame_menu.themes.THEME_BLUE) #pygame_menu.themes permet de choisir un thème pour le menu #pygame_menu.themes.THEME_BLUE est un thème prédéfini
menu.add.text_input('Nom :', default='Rija Rasoanaivo') #pygame_menu.Menu.add.text_input permet d'ajouter un champ de saisie de texte #default permet de définir une valeur par défaut
menu.add.selector('Difficulté :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty) 
menu.add.button('Jouer', start_the_game)
menu.add.button("Ajouter un mot", add_word_to_list)
menu.add.button('Quitter', pygame_menu.events.EXIT)
menu.mainloop(screen) #pygame_menu.Menu.mainloop permet d'afficher le menu #screen est la surface sur laquelle afficher le menu
