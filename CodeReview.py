from langchain_groq import ChatGroq
import json

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    groq_api_key = "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"
)

python_code = """
def add(a, b):
return a + b
"""

# Structured prompt for JSON output
code_review_prompt = f"""
You are a professional Python code reviewer. 
Analyze the following function and provide a structured review.

Return the response in strict JSON format with three keys:
- "errors": A list of syntax or logical errors.
- "suggestions": A list of improvements.
- "optimized_code": The corrected and optimized version of the function.

Ensure your response is **valid JSON only**.

```python
{python_code}
"""
response = llm.invoke(code_review_prompt)
try: review_result = json.loads(response.content)
print("\n Code Review Results:")
print(json.dumps(review_result, indent=4))
