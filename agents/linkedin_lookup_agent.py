from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

# now import initize agent and tool and agent type
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain import hub
from tools.tools import get_profile_url

import os 

# When you create and agent it requires tools 
#  1. like capability to search in an engine, on google drive or some other service there can be multiple such tools
#  passed to the agent. 
#  2. It also takes an LLM model to use. Agents use the LLM to reason which actions to take and in which order. 
#  3. Agent type is defining what agent to use. OpenAI tools, XML, json chat, etc. 
# agent types are derived from prompt engineering technique mainly the zero shot and ReACT techniques. Agent will 
# use the LLM and tools to do its job.  

def lookup(name: str, llm: AzureChatOpenAI) -> str:
    # first open an instance of chat model 
    template = """
               Given the full name of the person {name_of_person} I want you to find the LinkedIn URL of the person.
               Your answer should contain only a URL.
               """ 
    
    # define tool 
    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile", 
            func=get_profile_url, 
            description="Use google api to get the name linked in profile."
            )
        ]
    
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
                    tools=tools_for_agent, 
                    llm=llm,
                    prompt= react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_for_agent, 
        verbose=True
    )

    prompt_template = PromptTemplate(input_variables=['name'], template=template)

    result = agent_executor.invoke(
            input={"input": prompt_template.format(name_of_person=name)}
            )
    linkedin_url = result["output"]
    return linkedin_url