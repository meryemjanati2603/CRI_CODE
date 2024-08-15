from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Configuration de Selenium
PATH = "C:\\Users\\user\\Desktop\\chromedriver-win64\\chromedriver.exe"
service = Service(PATH)
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
# Accéder à la page principale
driver.get("https://www.dgssi.gov.ma/index.php/fr/bulletins-securite")
driver.maximize_window()
# Attendre que la page soit chargée
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='single-blog-content']")))
# Extraire les liens des vulnérabilités
vulnerabilite_links = driver.find_elements(By.XPATH, "//div[@class='single-blog-content']//h3/a")
# Afficher les liens extraits et visiter chaque lien
for link in vulnerabilite_links:
        # Réextraire les liens à chaque itération
        vulnerabilite_links = driver.find_elements(By.XPATH, "//div[@class='single-blog-content']//h3/a")
        href = link.get_attribute("href")
        print(f"Visiting: {href}")
        # Ouvrir le lien dans un nouvel onglet
        driver.execute_script("window.open(arguments[0], '_blank');", href)
        time.sleep(3)  # Attendre que la nouvelle page se charge
        # Passer au nouvel onglet
        driver.switch_to.window(driver.window_handles[-1])
        # Fermer l'onglet après le scraping
        driver.close()
        # Revenir à l'onglet principal
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)  # Attendre un peu avant de continuer
# Fermer le navigateur après avoir fini
driver.quit()
