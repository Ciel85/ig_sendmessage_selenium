from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import csv
import time
import sys

   
# Options Firefox
options = FirefoxOptions()
options.headless = False # à mettre en True hors test
options.add_argument("--window-size=800,800")
options.add_argument("--no-sandbox")

# Initialiser le pilote Selenium
# driver = webdriver.Chrome() 
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options) #juste pour le test

# Se connecter à Instagram
#driver.get('https://www.instagram.com/accounts/login/')

# Page de connexion
url_login = 'https://www.instagram.com/accounts/login/'

# Tentatives échouées
c_cookie = 1
c_login = 1
error_count = 3

# Données du compte à utiliser pour envoyer les messages
ig_account = ""  # TODO: hacher
ig_pwd = ""  # TODO: hacher

# Connexion à IG
print('###### CONNEXION INSTAGRAM #######')
driver.get(url_login)
time.sleep(2)

# Connexion
if c_login <= error_count:
    try:
        username_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input")
        password_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input")
        username_input.send_keys(ig_account)
        password_input.send_keys(ig_pwd)
        print('[DRIVER]: 02. Connexion')
        time.sleep(4)

        login_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]")
        login_button.click()
        print('[DRIVER]: 03. Envoyer')
        time.sleep(4)
    except:
        print('[ERREUR @ LOC - Login]: Erreur de connexion ou impossible de trouver l/élément HTML. Attente de 10s ...')
        c_login = c_login + 1
        time.sleep(10)
else:
    print('[ERREUR @ LOC - Login]: Trop d/erreurs sont survenues!')
    sys.exit()

# Attendre que la connexion soit réussie (ajouter une verification si necessaire)

# Délai après la connexion avant de continuer
time.sleep(2)

# Lire la liste des noms d'utilisateur depuis le fichier CSV
with open('liste_utilisateurs.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    usernames = next(reader)

        # Boucle pour l'envoi de messages
    for username in usernames:
        try:
            # Cliquez sur la barre de recherche
            
            search_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span")
            search_button.click()
            time.sleep(5)
            search_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input")
            search_input.click()
            time.sleep(2)
            
            # Entrez le nom d'utilisateur
            search_input.send_keys(username)
            search_input.send_keys(Keys.RETURN)
            
            # Attendre que le profil de l'utilisateur apparaisse dans les résultats
            time.sleep(10)  # ajuster le délai en fonction de la vitesse de chargement de la page
            
            # Cliquez sur le profil de l'utilisateur
            profile_link = driver.find_element(By.PARTIAL_LINK_TEXT, username)
            profile_link.click()
            time.sleep(10)
            
            # Cliquez sur le bouton "Message"
            message_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div")
            message_button.click()
            time.sleep(15)
            
            # Saisissez le message que vous souhaitez envoyer
            
            
            message_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]")
            #Message à envoyer
            message = "Script Fonctionnel"
            
            for letter in message:
                message_input.send_keys(letter)
                time.sleep(0.1)  # Attendez un bref instant entre chaque lettre
            # Envoyez le message en appuyant sur la touche "Enter"
            message_input.send_keys(Keys.RETURN)
            
            # Attendre un moment pour éviter d'envoyer trop rapidement
            time.sleep(5)
        
        except Exception as e:
            print(f"Erreur lors de l'envoi d'un message à {username}: {str(e)}")
        
print("[DRIVER]: 04. Message Envoyé! Fermeture de la connexion.")
# Fermez la session Selenium

driver.quit()
