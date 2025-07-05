from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# access the llm (try a new model later)
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="meta-llama/llama-4-maverick-17b-128e-instruct")


if __name__ == "__main__":
    # check if llm is working
    response = llm.invoke("The most followed celebrity on instagram now is")
    print(response.content)