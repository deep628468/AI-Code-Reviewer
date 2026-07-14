import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



def explain_issue(issue):

    prompt = f"""
You are an expert Python code reviewer.

Analyze this code issue:

File:
{issue['file']}

Line:
{issue['line']}

Column:
{issue['column']}

Severity:
{issue['severity']}

Issue:
{issue['message']}


Give a short answer in this format:

Problem:
(Explain what is wrong)

Reason:
(Explain why it matters)

Solution:
(Explain how to fix it)

Keep the answer under 100 words.
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": "You review Python code professionally."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.3
    )


    answer = response.choices[0].message.content


    return {

        "explanation": answer,

        "suggestion": answer

    }




def fix_code(code):

    prompt = f"""
You are an expert Python developer.

Review this Python code and fix:

- Syntax errors
- Logical errors
- Code quality problems
- Formatting issues

Return only the corrected Python code.

Do not add explanations.

Code:

{code}
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": "You are a professional Python developer."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.2

    )


    return response.choices[0].message.content

def review_code(code):

    prompt = f"""
You are a senior Python developer performing a professional code review.

Review the following Python code carefully.

Analyze:

1. Code quality
2. Readability
3. Naming conventions
4. Logic mistakes
5. Performance issues
6. Python best practices
7. Possible bugs


Return your response exactly in this format:


## 📊 Code Quality Score

Give a score out of 10.

Example:
8/10


## ❌ Problems Found

Mention important issues only.

Format:

1. Problem name
   Explanation


## 🔍 Reason

Explain why these problems matter.


## ✅ Solution

Give practical fixes with examples if required.


## 💡 Improvement Suggestions

Give 2-3 suggestions to make this code more professional.


Rules:

- Keep the answer simple.
- Avoid unnecessary theory.
- Focus on actionable improvements.
- Maximum 250 words.


Python Code:

{code}
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": "You are an expert Python code reviewer."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.3

    )


    return response.choices[0].message.content