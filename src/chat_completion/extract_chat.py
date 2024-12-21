
from src.config.config import get_settings
from langdetect import detect
from openai import OpenAI
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
