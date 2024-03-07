from dotenv import load_dotenv
load_dotenv()
from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from third_party.linkedin import scrape_linkedIn_profile
from agents.linkedin_lookup_agent import lookup

import os

def ice_breaker(information: str):    
    summary_template = """ 
    Given the information {information} about a person I want you to create: 
    1. A short summary of the person's life and achievements.
    2. Two interesting facts about the person.
    """
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    deployment_name = os.getenv('DEPLOYMENT_NAME')
    azure_endpoint = os.getenv('AZURE_ENDPOINT')
    
    # print(f"API Key: {api_key}")
    # print(f"Deployment Name: {deployment_name}")
    # print(f"Azure Endpoint: {azure_endpoint}")
    
    prompt_template = PromptTemplate(input_variables=['information'], template=summary_template)
    chat_model = AzureChatOpenAI(
        api_key=api_key,
        deployment_name=deployment_name,
        azure_endpoint=azure_endpoint,
        openai_api_version="2024-02-15-preview",
    )

    name = "Eden Marco"
    linkedin_url = lookup(name=name, llm=chat_model)
    print(f"Linkedin URL for {name} is: {linkedin_url}")

    chain = LLMChain(llm=chat_model, prompt=prompt_template)
    res = chain.invoke(input={"information": information})
    print(res["text"]) 


if __name__ == '__main__': 
    bio_data = scrape_linkedIn_profile("")
    ice_breaker(bio_data)
    
    
    
