import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import csv

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


def main(url):
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, "lxml")

    def extract_titre(soup):
        h1_title = soup.find('div', id='block-dgssi-page-title').find('h1', class_='main-title')
        return h1_title.text.strip() if h1_title else "Titre non trouvé"

    titre_principal = extract_titre(soup)
    print(f"** {titre_principal} **")

    # Extraction des systèmes affectés
    def extract_systemes_affectes(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_content_divs = div.find_all("div", class_="solutions-content")
            for sol_content_div in solutions_content_divs:
                titre_element = sol_content_div.find("h4")
                if titre_element and titre_element.text.strip() == "Systèmes affectés:":
                    titre_text = titre_element.text.strip()
                    container_div = titre_element.find_next("div", class_="field__item")
                    if container_div:
                        ul = container_div.find("ul")
                        if ul:
                            items = ul.find_all("li")
                            systemes = [item.text.strip() for item in items]
                            return titre_text, systemes
        return None, []

    titre, systemes_affectes = extract_systemes_affectes(soup)
    if titre:
        print(f"{titre}")
        data_sys = [[titre_principal, systeme] for systeme in systemes_affectes]

        # Créer une DataFrame et sauvegarder dans un fichier CSV
        df_sys = pd.DataFrame(data_sys, columns=["Titre", "Système Affecté"])
        # Enregistrement des données dans un fichier CSV sans écraser le contenu existant
        df_sys.to_csv("C:/Users/user/Desktop/systemes_affectes.csv", mode='a', index=False, header=False)
    else:
        print("Titre 'Systèmes affectés:' non trouvé.")

    # Extraction des identificateurs externes
    def extract_identificateurs_externes(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_ident_divs = div.find_all("div", class_="solutions-content")
            for sol_ident_divs in solutions_ident_divs:
                titre_element = sol_ident_divs.find("h4")
                if titre_element and titre_element.text.strip() == "Identificateurs externes:":
                    titre_text = titre_element.text.strip()
                    container_div = titre_element.find_next("div", class_="field__item")
                    if container_div:
                        # Extraction du texte du paragraphe
                        paragraphe = container_div.find("p", class_="Standard")
                        if paragraphe:
                            identificateur_externe = paragraphe.text.strip()
                            return titre_text, [identificateur_externe]

                        # Extraction des éléments de liste
                        ul = container_div.find("ul")
                        if ul:
                            items = ul.find_all("li")
                            identificateurs_list = [item.text.strip() for item in items]
                            return titre_text, identificateurs_list

        return None, []

    # Appel de la fonction extract_identificateurs_externes
    titre, identificateurs = extract_identificateurs_externes(soup)
    if titre:
        print(f"{titre}")
        for identificateur in identificateurs:
            print(f"- {identificateur}")

        # Répéter le titre principal pour chaque identificateur externe
        titres_repeats = [titre_principal] * len(identificateurs)

        # Créer une DataFrame avec des listes de même longueur
        df_identificateurs = pd.DataFrame({"Titre": titres_repeats, "Identificateur externe": identificateurs})
        df_identificateurs.to_csv("C:/Users/user/Desktop/identificateurs_externes.csv", mode='a', index=False,header=False)
    else:
        print("Titre 'Identificateurs externes:' non trouvé.")

    # Extraction du bilan
    def extract_bilan(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_ident_divs = div.find_all("div", class_="solutions-content")
            for sol_ident_divs in solutions_ident_divs:
                titre_element = sol_ident_divs.find("h4")
                if titre_element and titre_element.text.strip() == "Bilan de la vulnérabilité:":
                    titre_text = titre_element.text.strip()
                    container_div = titre_element.find_next("div", class_="field__item")
                    if container_div:
                        paragraphe_bilan = container_div.find("p")
                        if paragraphe_bilan:
                            bilan = paragraphe_bilan.text.strip()
                            return titre_text, bilan
        return None, ""

    titre, bilan = extract_bilan(soup)
    if titre:
        print(f"{titre}")
        print(f"{bilan}")

        df_bilan = pd.DataFrame({"Titre": [titre_principal], "Bilan de la vulnérabilité:": [bilan]})
        df_bilan.to_csv("C:/Users/user/Desktop/bilan.csv", mode='a', index=False, header=False)
    else:
        print("Titre 'Bilan de la vulnérabilité:' non trouvé.")

    # Extraction des solutions
    def extract_solution(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_ident_divs = div.find_all("div", class_="solutions-content")
            for sol_ident_divs in solutions_ident_divs:
                titre_element = sol_ident_divs.find("h4")
                if titre_element and titre_element.text.strip() == "Solution:":
                    titre_text = titre_element.text.strip()
                    container_div = titre_element.find_next("div", class_="field__item")
                    if container_div:
                        paragraphe_solution = container_div.find("p")
                        if paragraphe_solution:
                            solution = paragraphe_solution.text.strip()
                            return titre_text, solution
        return None, ""

    titre, solution = extract_solution(soup)
    if titre:
        print(f"{titre}")
        print(f"{solution}")

        df_solution = pd.DataFrame({"Titre": [titre_principal], "Solution:": [solution]})
        df_solution.to_csv("C:/Users/user/Desktop/solution.csv", mode='a', index=False, header=False)
    else:
        print("Titre 'Solution:' non trouvé.")

    # Extraction des risques
    def extract_risque(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_content_divs = div.find_all("div", class_="solutions-content")
            for sol_content_divs in solutions_content_divs:
                titre_element = sol_content_divs.find("h4")
                if titre_element and titre_element.text.strip() == "Risque:":
                    titre_text = titre_element.text.strip()
                    container_div = titre_element.find_next("div", class_="field__item")
                    if container_div:
                        ul = container_div.find("ul")
                        if ul:
                            items = ul.find_all("li")
                            risques = [item.text.strip() for item in items]
                            return titre_text, risques
        return None, []

    titre, risques = extract_risque(soup)
    if titre:
        print(f"{titre}")
        for risque in risques:
            print(f"- {risque}")

        # Répéter le titre principal autant de fois qu'il y a de risques
        titres_repeats = [titre_principal] * len(risques)

        # Créer une DataFrame avec des listes de même longueur
        df_risques = pd.DataFrame({"Titre": titres_repeats, "Risque:": risques})
        df_risques.to_csv("C:/Users/user/Desktop/risques.csv", mode='a', index=False, header=False)
    else:
        print("Titre 'Risque:' non trouvé.")

    def extract_references(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_content_divs = div.find_all("div", class_="solutions-content")
            for sol_content_div in solutions_content_divs:
                titre_element = sol_content_div.find("h4")
                if titre_element and titre_element.text.strip() == "Référence:":
                    container_div = titre_element.find_next("div", class_="field__item")
                    if container_div:
                        ul = container_div.find("ul")
                        if ul:
                            items = ul.find_all("li")
                            references = [item.text.strip() for item in items]
                            return references
        return []

    # Extraction des références
    refs = extract_references(soup)
    if refs:
        print("Références:")
        for ref in refs:
            print(f"- {ref}")

        # Répéter le titre principal autant de fois qu'il y a de références
        titres_repeats = [titre_principal] * len(refs)

        # Créer une DataFrame avec des listes de même longueur
        df_references = pd.DataFrame({"Titre": titres_repeats, "Référence": refs})
        df_references.to_csv("C:/Users/user/Desktop/references.csv", mode='a', index=False, header=False)
    else:
        print("Titre 'Référence:' non trouvé.")

    def extract_brochure(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_content_divs = div.find_all("div", class_="solutions-content")
            for sol_content_div in solutions_content_divs:
                titre_element = sol_content_div.find("h6")
                if titre_element and titre_element.text.strip() == "Brochure:":
                    # Chercher le lien dans la balise <a> sous la div
                    link = sol_content_div.find("a")
                    if link:
                        lien = link.get("href")
                        if lien:
                            # Construire l'URL complète si nécessaire
                            if not lien.startswith("http"):
                                lien = f"https://www.dgssi.gov.ma{lien}"
                            return lien
        return ""

    # Appel de la fonction extract_brochure
    brochure_url = extract_brochure(soup)
    if brochure_url:
        print(f"Brochure URL: {brochure_url}")
        df_brochure = pd.DataFrame({"Titre": [titre_principal], "URL": [brochure_url]})
        df_brochure.to_csv("C:/Users/user/Desktop/brochure.csv", mode='a', index=False, header=False)
    else:
        print("Brochure non trouvée ou lien non disponible.")

    headers = []
    values = []
    # Extraction des sections contenant des informations
    hdet = soup.find_all("div", {'class': 'row'})
    def get_table_info(hdet):
        for div in hdet:
            table = div.find("table", class_="table table-bordered table-hover table_fixe widthtable")
            if table:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        champ = cells[0].text.strip()
                        valeur = cells[1].text.strip()
                        headers.append(champ)
                        values.append(valeur)

    get_table_info(hdet)

    # Vérification des listes après extraction
    print(f"Headers: {headers}")
    print(f"Values: {values}")

    # Filtrer les valeurs pour éviter les répétitions des champs
    filtered_values = []
    for i in range(len(headers)):
        if headers[i] in values[i]:
            filtered_values.append(values[i].replace(headers[i], '').strip())
        else:
            filtered_values.append(values[i])

    # Créer un DataFrame à partir des données extraites
    data = {'Champ': headers, 'Valeur': filtered_values}
    df = pd.DataFrame(data)
    print(df)

    # Sauvegarde en mode append pour ne pas écraser les anciennes données
    df.to_csv('C:/Users/user/Desktop/tableau.csv', mode='a', index=False, header=False)


# Boucle pour visiter chaque lien et extraire les informations
for link in vulnerabilite_links:
    url = link.get_attribute("href")
    print(f"Visiting {url}")
    main(url)
driver.quit()