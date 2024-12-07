from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_bluesky_profile_url

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
    )
    template = """
       Given the name {name_of_person} I want you to find a link to their BlueSky profile page and extract from it their BlueSky handle.
       Include only the person's BlueSky handle in the final answer
    """
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google for BlueSky profile page",
            func=get_bluesky_profile_url,
            description="useful for when you need get the BlueSky profile page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    blueksy_handle = result["output"]

    # Remove the leading "@" symbol if present
    if blueksy_handle[0] == "@":
        blueksy_handle = blueksy_handle[1:]

    return blueksy_handle


if __name__ == "__main__":
    print(lookup(name="Shawn Flahave"))