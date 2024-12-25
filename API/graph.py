from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage

from langchain_cohere import ChatCohere
from langgraph.graph import StateGraph, START, END

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
import os
from dotenv import load_dotenv

load_dotenv()


try:
    os.mkdir('conversations_db')
except:
    os.path.isdir('conversations_db')

conn = sqlite3.connect('conversations_db/database.db', check_same_thread=False)
checkpointer = SqliteSaver(conn)

llm = ChatCohere(model="command-r-plus", max_tokens=512, api_key=os.getenv("COHERE_API_KEY"))

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# nodes
graph_builder.add_node("chatbot", chatbot)

# edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# compiling graph
graph = graph_builder.compile(checkpointer=checkpointer)

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
