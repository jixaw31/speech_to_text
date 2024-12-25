from typing import Annotated
from typing_extensions import TypedDict

from langchain_cohere import ChatCohere
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

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