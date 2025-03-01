from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

def generate_topics(field: str) -> str:
    # Initialize LLM
    llm = OpenAI(api_key="your_openai_api_key")

    # Define prompt
    topic_prompt = PromptTemplate(
        input_variables=["field"],
        template="Generate 5 popular topics in the field of {field}. Return them as a comma-separated list."
    )

    # Create chain
    topic_chain = LLMChain(llm=llm, prompt=topic_prompt)

    # Run chain
    return topic_chain.run(field=field)
