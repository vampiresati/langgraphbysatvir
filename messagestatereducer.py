from typing import Annotated

from langgraph.graph import START, END, StateGraph, MessagesState
from util.langgraph_util import display
from langchain_core.messages import AIMessage, HumanMessage
from operator import add
from typing import TypedDict,Annotated

# Extend MessagesState with our own field
class State(MessagesState):
    discount: Annotated[int,add]


def connect_to_sale(state: State):
    return {
        "messages": [
            AIMessage(content="connect to sale")
        ],
        "discount": 10
    }


def sale_team_response(state: State):
    return {
        "messages": [
            AIMessage(content="offer for you")
        ],
        "discount": 20
    }


graph = StateGraph(State)

graph.add_node("connect_to_sale", connect_to_sale)
graph.add_node("sale_team_response", sale_team_response)

graph.add_edge(START, "connect_to_sale")
graph.add_edge("connect_to_sale", "sale_team_response")
graph.add_edge("sale_team_response", END)

chatbot = graph.compile()

display(chatbot)

result = chatbot.invoke({
    "messages": [
        HumanMessage(content="I want to buy product")
    ],
    "discount": 0
})


for m in result["messages"]:
    print(m.content)

print(f"total discount is {result['discount']}")