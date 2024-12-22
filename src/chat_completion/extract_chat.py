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
        4. Suggest job titles based on the CV and estimate the level for each suggested job (e.g., Junior Data Scientist, Mid-level Data Analyst, etc.).
        5. A brief 2-3 sentence comment summarizing the profile, highlighting key strengths and professional focus.

        Please output the result in JSON format as follows:
        {{
            "skills": ["Skill1", "Skill2", ...],
            "seniority": "Seniority Level",
            "years_of_experience": TotalYears,
            "suggested_jobs": [
                {{ "job_title": "Job Title 1", "estimated_level": "Junior" }},
                {{ "job_title": "Job Title 2", "estimated_level": "Mid-level" }}
            ],
            "profile_summary": "Brief 2-3 sentence summary of the profile"
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
        4. Suggérer des titres de poste basés sur le CV et estimer le niveau pour chaque poste suggéré (par exemple, Junior Data Scientist, Analyste Data Intermédiaire, etc.).
        5. Un commentaire bref de 2 à 3 phrases résumant le profil, mettant en valeur les points forts et l'orientation professionnelle.

        Veuillez donner le résultat au format JSON comme suit :
        {{
            "competences": ["Compétence1", "Compétence2", ...],
            "niveau_de_seniorite": "Niveau de Séniorité",
            "annees_d_experience": TotalAnnées,
            "postes_suggérés": [
                {{ "titre_poste": "Poste 1", "niveau_estime": "Junior" }},
                {{ "titre_poste": "Poste 2", "niveau_estime": "Intermédiaire" }}
            ],
            "resume_profil": "Commentaire bref de 2-3 phrases résumant le profil"
        }}

        Voici le texte du CV :
        {cv_text}
        """
    else:
        return {"error": "Language not supported or not detected."}

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
