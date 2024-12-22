from src.config.config import get_settings
from openai import OpenAI

settings = get_settings()
client = OpenAI(api_key=settings.API_key)

Prompt_Path = "C:/Users/yousf/Bureau/Hackathon-EY/hackathonEY/src/job_desc/generate_test_template.txt"


def load_prompt(skill, difficulty, number_questions) -> str:
    try:
        with open(Prompt_Path, 'r') as file:
            prompt_template = file.read()
        return prompt_template.format(skill=skill, difficulty_level=difficulty, number_of_questions=number_questions)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise


def generate_test(skill, difficulty, number_questions=1):
    prompt = load_prompt(skill, difficulty, number_questions)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
