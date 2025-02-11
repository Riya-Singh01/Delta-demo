import streamlit as st
from langchain_groq import ChatGroq

llm= ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    groq_api_key="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",
)

st.title("SIMPLE LLM Chatbot")
st.write("Enter Your Query below:")
user_input=st.text_input("YOUR QUESTION:","")

if st.button("Get Answer"):
    response=llm.invoke(user_input)
    st.write("###Response:")
    st.write(response)