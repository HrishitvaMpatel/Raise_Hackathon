import os
import pandas as pd
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- Load CSVs ---
CSV_PATH_1 = os.path.join('data', 'analysis_results.csv')
CSV_PATH_2 = os.path.join('data', 'ANALYSIS.csv')
df1 = pd.read_csv(CSV_PATH_1)
df2 = pd.read_csv(CSV_PATH_2)
df = pd.concat([df1, df2], ignore_index=True)

# Helper: extract keywords
def extract_keywords(query):
    return re.findall(r'"([^"]+)"|(\w+)', query.lower())

def retrieve_relevant_rows(query):
    raw_keywords = extract_keywords(query)
    keywords = [k[0] if k[0] else k[1] for k in raw_keywords]
    def row_match(row):
        row_str = str(row).lower()
        return any(kw in row_str for kw in keywords if kw)
    mask = df.apply(row_match, axis=1)
    return df[mask]

def format_context(rows, max_rows=10):
    if rows.empty:
        return ""
    rows = rows.head(max_rows)
    return rows.to_csv(index=False)

def generate_groq_answer(question, context):
    if context.strip():
        prompt = (
            "You are a data assistant. Given the following CSV data rows as background information, "
            "answer the question concisely and do NOT repeat or enumerate the CSV rows in your answer. "
            "Do NOT mention the frequency or number of occurrences of any entry. "
            "Use the data only for reference and provide a clear, direct answer.\n"
            f"{context}\n\nAnswer the question: {question}"
        )
    else:
        prompt = (
            "You are a data assistant. There is no relevant data in the CSV for the question. "
            "Please answer the question using your own knowledge and reasoning: "
            f"{question}"
        )
    
    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {"role": "system", "content": "You are a data assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    answer = response.choices[0].message.content.strip()
    answer = re.sub(r'\*\*(.*?)\*\*', r'\1', answer)
    return answer
