import streamlit as st
from langchain_groq import ChatGroq

def correct_grammar(text):
    llm = ChatGroq(
        model="gemma2-9b-it",
        temperature=0,
        groq_api_key="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"  # Replace with your actual API key
    )
    
    prompt = f"""
    Check the grammar of the following text. 
    If it's correct, return it as is. 
    If it has grammar mistakes, correct them without 
    changing the meaning or adding extra words. 
    Also, list the incorrect words and provide feedback 
    on what went wrong.\nText: {text}
    """
    
    response = llm.invoke(prompt)  # Get AIMessage object
    corrected_text = response.content  # Extract actual text

    return corrected_text

st.title("Grammar Checker")
st.write("Enter text below and click 'Check Grammar' to see corrections.")

user_text = st.text_area("Enter your text here", height=100)

if st.button("Check Grammar"):
    if user_text.strip():
        with st.spinner("Checking grammar..."):
            corrected_text = correct_grammar(user_text)
            st.subheader("Corrected Text:")
            st.write(corrected_text)
    else:
        st.warning("Please enter some text.")

    if corrected_text.strip() == text.strip():
        print("\nSentence is already correct:", text)
    else:
        print("\nCorrected Text:", corrected_text)
        
        # The response from the model should ideally contain the list of incorrect words and feedback
        if "incorrect words" in corrected_text.lower():
            # Extract incorrect words and explanations (assuming response structure includes it)
            incorrect_words_feedback = extract_incorrect_words(corrected_text) 
            print("\nIncorrect Words and Feedback:", incorrect_words_feedback)

def extract_incorrect_words(response_text):
    # Implement logic to parse incorrect words and their explanations from the response
    # This will depend on how the LLM outputs feedback, here assuming a simplified approach
    incorrect_words = []
    lines = response_text.splitlines()
    for line in lines:
        if "incorrect" in line.lower():
            incorrect_words.append(line.strip())
    return incorrect_words

if __name__ == "__main__":
    input_text = input("Enter a sentence to check grammar: ")
    correct_grammar(input_text)
