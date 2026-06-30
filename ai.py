from openai import OpenAI
import json

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

def analyze_resume(resume_text, user_goal):
    prompt = f"""
    You are a senior software engineer and hiring manager.
    
    Evaluate the resume based on the user's goal.

    User goal:"{user_goal}"

    STRICT RULES:
    -Extract only relevant skills for this goal
    -REMOVE irrelevant tools [excel for backend,etc]
    -Identify real gaps
    -Generate roadmap only for missing fields
    -Make output DIFFERENT based on goal

    Return only JSON:
    {{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions":[]
    }}

    Resume: 
    {resume_text}


    """
    try:
        response = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a strict hiring manager.."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()

        start = content.find('{')
        end = content.rfind('}') + 1

        return json.loads(content[start:end])
    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": f"AI analysis error: {str(e)}"
        }
