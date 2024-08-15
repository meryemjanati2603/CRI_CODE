import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# URL de la page à scraper
url = "https://www.dgssi.gov.ma/index.php/fr/bulletins/vulnerabilites-critiques-affectant-plusieurs-produits-dapple-3"
page = requests.get(url)

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")

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
        for systeme in systemes_affectes:
            print(f"- {systeme}")

        df_systemes = pd.DataFrame({"Système affecté": systemes_affectes})
        df_systemes.to_csv("C:/Users/user/Desktop/systemes_affectes.csv", index=False, header=False)
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
                        paragraphe = container_div.find("p", class_="Standard")
                        if paragraphe:
                            identificateur_externe = paragraphe.text.strip()
                            return titre_text, identificateur_externe
        return None, ""

    titre, identificateur_externe = extract_identificateurs_externes(soup)
    if titre:
        print(f"{titre}")
        print(f"{identificateur_externe}")
        df_identificateurs = pd.DataFrame({"Identificateur externe": [identificateur_externe]})
        df_identificateurs.to_csv("C:/Users/user/Desktop/identificateurs_externes.csv", index=False, header=False)
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

        df_bilan = pd.DataFrame({"Bilan de la vulnérabilité:":[bilan]})
        df_bilan.to_csv("C:/Users/user/Desktop/bilan.csv", index=False, header=False)
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

        df_solution = pd.DataFrame({"Solution:": [solution]})
        df_solution.to_csv("C:/Users/user/Desktop/solution.csv", index=False, header=False)
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

        df_risques = pd.DataFrame({"Risque:": risques})
        df_risques.to_csv("C:/Users/user/Desktop/risques.csv", index=False, header=False)
    else:
        print("Titre 'Risque:' non trouvé.")

    # Extraction des références
    def extract_references(soup):
        hdet = soup.find_all("div", {'class': 'row'})
        for div in hdet:
            solutions_content_divs = div.find_all("div", class_="solutions-content")
            for sol_content_divs in solutions_content_divs:
                titre_element = sol_content_divs.find("h4")
                if titre_element and titre_element.text.strip() == "Référence:":
                    titre_text = titre_element.text.strip()
                    container_div = titre_element.find_next("div", class_="field__item")
                    if container_div:
                        ul = container_div.find("ul")
                        if ul:
                            items = ul.find_all("li")
                            references = [item.text.strip() for item in items]
                            return titre_text, references
        return None, []

    titre, references = extract_references(soup)
    if titre:
        print(f"{titre}")
        for reference in references:
            print(f"- {reference}")

        df_references = pd.DataFrame({"Référence:": references})
        df_references.to_csv("C:/Users/user/Desktop/references.csv", index=False, header=False)
    else:
        print("Titre 'Référence:' non trouvé.")

    # Extraction de la brochure
    def extract_brochure(soup):
        # Cherche toutes les div avec la classe "row"
        hdet = soup.find_all("div", {'class': 'row'})

        for div in hdet:
            # Cherche toutes les div avec la classe "solutions-content"
            solutions_content_divs = div.find_all("div", class_="solutions-content")

            for sol_content_div in solutions_content_divs:
                # Cherche l'élément <h6> avec le texte "Brochure:"
                titre_element = sol_content_div.find("h6")
                if titre_element and titre_element.text.strip() == "Brochure:":
                    titre_text = titre_element.text.strip()
                    # Cherche le lien dans la balise <a> sous la div
                    link = sol_content_div.find("a")
                    if link:
                        lien = link.get("href")
                        if lien:
                            # Construire l'URL complète si nécessaire
                            if not lien.startswith("http"):
                                lien = f"https://www.dgssi.gov.ma{lien}"
                            return titre_text, lien

        return None, ""
    # Appel de la fonction extract_brochure
    titre, brochure_url = extract_brochure(soup)
    if titre:
        print(f"{titre}")
        print(f"URL de la brochure: {brochure_url}")
        df_brochure = pd.DataFrame({"Titre": [titre], "URL": [brochure_url]})
        df_brochure.to_csv("C:/Users/user/Desktop/brochure.csv", index=False, header=False)
    else:
        print("Titre 'Brochure:' non trouvé ou lien non disponible.")

    headers = []
    values = []
    titres = []
    data_associee = []

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

    # Créer un fichier CSV avec les champs et valeurs
    file_path = 'C:/Users/user/Desktop/tableau.csv'

    def create_file(file_path, headers, filtered_values):
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['Champ', 'Valeur'])  # Écrire les en-têtes des colonnes
                for champ, valeur in zip(headers, filtered_values):
                    w.writerow([champ, valeur])  # Écrire les paires champ-valeur
            print("File created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    create_file(file_path, headers, filtered_values)
main(page)