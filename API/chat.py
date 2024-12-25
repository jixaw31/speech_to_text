from typing import Annotated
from typing_extensions import TypedDict
from io import BufferedReader

from langchain_cohere import ChatCohere
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.prompts import ChatPromptTemplate

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
import os

from graph import graph
from dotenv import load_dotenv
load_dotenv()

# configuring the thread
config = {"configurable": {"thread_id": "1"}}

# You can edit system message and tailor it to your needs
new_messages = [
    SystemMessage(content = """You're an assistant who is an expert in financial markets.
                               Always, introduce your background in
                               no more than 15 words.""")
]
# updating graph with SystemMessage(assigning the agent a background)
graph.update_state(
    config,
    {"messages": new_messages},
)
# lets assume we've recorded such strategy:
recorded_voice = """
                سلام من میخوام یه استراتیجی داشته باشم که اگر مووینگ ابریج 20 روزه مووینگ ابریج 50 روزه رو برابره قد کرد
                برام بخورم اگر رو به پایین قد کرد برام بفروشم استاپلاسی هم که
                 میخوام 3 درصده تارگیتی هم که میخوام بذارم میخوام همیشه دو برابر استاپلاس هم باشیم
                 keep this in mind, but don't respond to it. I'll question you later about it.
                """

# updating graph with SystemMessage(the recorded strategy)
graph.update_state(
    config,
    {"messages": [SystemMessage(content = recorded_voice)]},
)

