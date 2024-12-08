from typing import Tuple

from black import format_str
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOllama

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.bluesky_lookup_agent import lookup as bluesky_lookup_agent
from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.bluesky import scrape_bluesky_posts


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=False)

    bluesky_handle = bluesky_lookup_agent(name=name)
    bluesky_posts = scrape_bluesky_posts(bluesky_profile_handle=bluesky_handle)

    summary_template = """
    Given the information about a person from LinkedIn {information}, and their latest BlueSky posts {bluesky_posts}, 
    I want you to create:
    1. A short summary
    2. Two interesting facts about them

    Use information from both LinkedIn and BlueSky to create the summary.
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "bluesky_posts"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    # llm = ChatOllama(model="llama3")
    # llm = ChatOllama(model="mistral")

    chain = summary_prompt_template | llm | summary_parser

    res:Summary = chain.invoke(input={"information": linkedin_data, "bluesky_posts": bluesky_posts})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with("Shawn Flahave")