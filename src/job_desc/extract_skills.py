from src.config.config import get_settings
from openai import OpenAI

settings = get_settings()
client = OpenAI(api_key=settings.API_key)
Prompt_Path = "C:/Users/yousf/Bureau/Hackathon-EY/hackathonEY/src/job_desc/extract_skills_prompt.txt"


def load_prompt(job_description: str) -> str:
    try:
        with open(Prompt_Path, 'r') as file:
            prompt_template = file.read()
        return prompt_template.format(JOB_DESCRIPTION=job_description)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise


def extract_skills(job_description: str):
    prompt = load_prompt(job_description)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
