from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os
import requests


def decrypt_md5_online(md5_hash):
    url = f"https://hashes.com/en/decrypt/hash/{md5_hash}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Check the website for results:", url)
    else:
        print("Failed to connect to the database.")

md5_hash = "54cc5f2a6e307de1b0af57d2651a0159"  # Example: "hello"
api_key =decrypt_md5_online(md5_hash)
# api_key = os.environ["OPENAI_API_KEY"]
def generate_topics(field: str) -> str:
    # Initialize LLM
    llm = OpenAI(api_key=api_key)

    # Define prompt
    topic_prompt = PromptTemplate(
        input_variables=["field"],
        template="Generate 5 popular topics in the field of {field}. Return them as a comma-separated list."
    )

    # Create chain
    topic_chain = LLMChain(llm=llm, prompt=topic_prompt)

    # Run chain
    return topic_chain.run(field=field)
