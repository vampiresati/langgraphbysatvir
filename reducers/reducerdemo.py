from langgraph.graph import START,END,StateGraph
from util.langgraph_util import display
from typing import TypedDict,Annotated
from operator import add
from langchain_core.messages import AnyMessage
from langchain_core.messages import AIMessage,HumanMessage

class chatbot(TypedDict):
    message: Annotated[list[AnyMessage],add]
    discount: Annotated[int,add]

def connect_to_sale(state: chatbot):
    return {"message":[AIMessage(content="connect to sale")],"discount":10}
def sale_team_response(state: chatbot):
    return {"message":[AIMessage(content="offer for you")],"discount":20}



graph = StateGraph(chatbot)
graph.add_node("connect_to_sale",connect_to_sale)
graph.add_node("sale_team_response",sale_team_response)

graph.add_edge(START,"connect_to_sale")
graph.add_edge("connect_to_sale","sale_team_response")
graph.add_edge("sale_team_response",END)

chatbot = graph.compile()
display(chatbot)
message=chatbot.invoke({"message":[HumanMessage(content="i want to buy product")],"discount":0})
for m in message['message']:
    print(f"you have discount off->{m}")
print(f"total discount is {message['discount']}")
