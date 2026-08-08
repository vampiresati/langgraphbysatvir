from langgraph.graph import START,END,StateGraph
from util.langgraph_util import display
from typing import TypedDict

class JobApplication(TypedDict):
    name: str
    yearsofexperience: int

def interview(applicant: JobApplication):
    print(f"you have direct interview-> {applicant}")
    return applicant
def skill_test(applicant: JobApplication):
    print(f"you have to give skill test-> {applicant}")
    return applicant
def conditional_response(applicant: JobApplication):
    if applicant['yearsofexperience'] >= 5:
        return "interview"
    return "skill_test"

graph = StateGraph(JobApplication)
graph.add_node("interview",interview)
graph.add_node("skill_test",skill_test)

graph.add_conditional_edges(START,conditional_response)
graph.add_edge("interview",END)
graph.add_edge("skill_test",END)

runnable = graph.compile()
display(runnable)
runnable.invoke({"name":"My name is alice","yearsofexperience":1})
runnable.invoke({"name":"My name is satvir","yearsofexperience":5})