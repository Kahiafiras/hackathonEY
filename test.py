
from src.config.config import get_settings
from langdetect import detect
from openai import OpenAI
import openai


settings = get_settings()
client = OpenAI(api_key=settings.API_key)



def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown" 

def extract_cv_details(cv_text):
    lang = detect_language(cv_text)
    
    if lang == "en":
        prompt = f"""
        You are an expert recruiter helping to analyze CVs written in English. Your task is to extract specific information from a CV provided as text. Please return:

        1. A list of key skills mentioned in the CV.
        2. The seniority level (e.g., Junior, Mid-level, Senior, or similar).
        3. The total years of professional experience based on the text.

        Please output the result in JSON format as follows:
        {{
            "skills": ["Skill1", "Skill2", ...],
            "seniority": "Seniority Level",
            "years_of_experience": TotalYears
        }}

        Here is the CV text:
        {cv_text}
        """
    elif lang == "fr":
        prompt = f"""
        Vous êtes un expert en recrutement et vous aidez à analyser des CVs rédigés en français. Votre tâche consiste à extraire des informations spécifiques d'un CV fourni sous forme de texte. Veuillez fournir :

        1. Une liste des compétences clés mentionnées dans le CV.
        2. Le niveau de séniorité (par exemple, Junior, Intermédiaire, Senior ou équivalent).
        3. Le total des années d'expérience professionnelle basé sur le texte.

        Veuillez donner le résultat au format JSON comme suit :
        {{
            "competences": ["Compétence1", "Compétence2", ...],
            "niveau_de_seniorite": "Niveau de Séniorité",
            "annees_d_experience": TotalAnnées
        }}

        Voici le texte du CV :
        {cv_text}
        """
    else:
        return {"error": "Language not supported or not detected."}

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content





if __name__ == "__main__":
    # Example usage
    cv_text = """
    # AZIZI SIRINE

    # Eléve ingénieure en Intelligence Artificielle et Data Science

    # P A R C O U R S A C A D E M I Q U E S

    # TELECOM

    Data scientist (stagiaire) 07/2024 - 09/2024

    Mise en place d’une solution IA pour le traitement et l’analyse des données radio inter-serveurs.

    Mots-clés : Machine learning, Deep learning, Python, TensorFlow, Keras, PyTorch,

    # C O N T A C T

    +216-58644673

    syrineazizi75@gmail.com

    N'07 Bellevue el ouardia Tunis, 1009 Tunisie

    Sirine Azizi

    # F O R M A T I O N S

    Cycle Ingénieur Informatique, spécialité Data science et Intelligence Artificielle [2025], Université Ibn Khaldoun

    Master 1 en Data Mining-Data Visualisation [2023], FSEGJ

    Licence Nationale Technologie de l'Informatique, Spécialité Multimédia et Développement Web [2022], ISET Beja

    # C O M P É T E N C E S

    - Machine Learning
    - Deep Learning
    - NLP/ Transformes/ LLMS
    - Python
    - IA /IA Generative
    - Data collection/ Data processing
    - UML / Agile SCRUM
    - Git

    # L A N G U A G E S

    - Français
    - Anglais
    - Arabe

    # E N G A G E M E N T A S S O S I A T I F

    Détection des insectes Bactrocera olea qui détruit les olives.

    Mots-clés : Machine learning, Deep learning, YOLO, Python

    Impact: Prévention des pertes agricoles et optimisation des rendements grâce à l’IA.

    Langage de programmation: python

    Frameworks AI/ML: Tensorflow, Keras, PyTorch

    Outils de visualisation de données : Matplotlib, seaborn, pandas, numpy

    Métriques de Performances: Accuracy, F1-Score

    # C2S

    Développeur web et mobiles (stagiaire) 01/2022 - 06/2022

    Conception et réalisation d’une application web et mobile

    Technologies utilisées: C, ASP.NET, Visual Studio 2019, Razor, UML, BD SQL SERVER, flutter, Android studio.

    Mots-clés : Web, services Web, base de données, travail d'équipe, SCRUM

    # NAVICOM

    Développeur web (stagiaire) 08/2021 - 10/2021

    Conception et réalisation d’une application web

    Technologies et langages utilisées : HTML, CSS, PHP, UML, BD MySQL.

    Mots-clés : Web, services Web, base de données, travail d'équipe, SCRUM.

    # SIEGE BIAT

    Stage d'initiation 03/2020 - 04/2020

    Programme Etude des dossiers de crédits de gestion.

    Etude des dossiers de crédits et l'analyse de l'environnement économique

    # P R O J E T S

    Détection de malaria usant SVM et Vgg19

    Impact: Amélioration du diagnostic de la malaria grâce à l'IA pour une détection précoce.

    Langage de programmation: python

    Frameworks AI/ML: Scikit-learn, Keras, TensorFlow

    Outils de visualisation de données : Matplotlib, seaborn

    Métriques de Performances: Accuracy, Precision, Recall

    Détection des sentiments en IA

    Développement d’une application de détection et la reconnaissance faciale en utilisant Python

    # C E R T I F I C A T I O N S

    Workshop/Fundamentales of Deep Learning (NVIDIA: 2024)

    Google Advanced Data Analytics Certificat Professionnel (Google: 2024)

    Microsoft Azure Data Scientist Associate (DP-100) Certificat Professionnel (Microsoft: 2024)

    # C O M P É T I T I O N S E T H A C K A T H O N S

    HR Manager, Club ATIA UIK 1ère place : Gagnante du hackathon Tunisian Smart Cities avec un prototype de poubelle connectée pour optimiser la gestion des déchets urbains à Soukra.

    Membre, Club UIK ROBOTIC 2ème place : Finaliste du hackathon FTUSA avec un chatbot interactif améliorant l'expérience client dans le secteur de l'assurance.

    Organisatrice, Journées Portes Ouvertes à l’UIK.



    """
    result = extract_cv_details(cv_text)
    print(result)
