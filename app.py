from graph.nodes.intent_analyzer import analyze_input
from graph.nodes.planner import planning_node
from graph.nodes.researcher import research_node


intial_state = {
    "query": {
        "user_query": "Explain quantum computing"
    }
}

final_state = analyze_input(intial_state)
# print(final_state)
# print("````````````````````````````````````````````")
final_state = planning_node(final_state)
# print(final_state)
final_state = research_node(final_state)
print(final_state)
