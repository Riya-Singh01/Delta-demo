from langchain_groq import ChatGroq
import streamlit as st


llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.2,
    groq_api_key="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" 
)


def analyze_sentiment_and_suggest(text):
    prompt = f"""
    You are an assistant that 
    analyzes the sentiment of a 
    given text and provides useful suggestions
    based on the tone of the text:
    ---
    {text}
    ---
    Based on the sentiment of the text,
    please provide one of the following:
    1. The sentiment of the text: 'Positive', 'Negative', or 'Neutral'.
    2. A helpful suggestion or advice based on the sentiment:
        - If the sentiment is positive, suggest ways to maintain or enhance it.
        - If the sentiment is negative, suggest ways to improve or overcome the negativity.
        - If the sentiment is neutral, suggest ways to add more emotion or perspective to the text.
    """
    
    
    response = llm.invoke(prompt, max_tokens=150)
    return response.content.strip()




st.title("Sentiment Analyzer with Suggestions")
st.write("Enter text below to analyze its sentiment and get advice.")

user_text = st.text_area("Enter your text here:", height=100)

if st.button("Analyze Sentiment"):
    if user_text.strip():
        with st.spinner("Analyzing..."):
            result = analyze_sentiment_and_suggest(user_text)
            st.subheader("Analysis Result:")
            st.write(result)
    else:
        st.warning("Please enter some text.")


def main():
    print("Enter a sentence to analyze the sentiment and receive suggestions (type 'exit' to quit):")
    while True:
        user_input = input("Your input: ")
        
        
        if user_input.lower() == 'exit':
            print("Exiting the sentiment analysis tool.")
            break
        
       
        result = analyze_sentiment_and_suggest(user_input)
        
        
        print(f"Result:\n{result}\n")



main()