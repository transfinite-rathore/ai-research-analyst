from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from .graph.nodes.research_aggregator import aggregate_results
from .graph.states.research_state import ResearchState

from .graph.nodes.new_search import news_search
from .graph.nodes.researcher import research_node
from .graph.nodes.reddit_search import reddit_search
from .graph.nodes.paper_search import papers_search
from .graph.nodes.web_search import search_query




def route_research(state: ResearchState):

    sends = []

    # WEB TASKS
    for task in state.get("web_search_task", []):

        sends.append(
            Send(
                "web_search",
                {
                    "task": task
                }
            )
        )

    # REDDIT TASKS
    for task in state.get("reddit_search_task", []):

        sends.append(
            Send(
                "reddit_search",
                {
                    "task": task
                }
            )
        )

    # NEWS TASKS
    for task in state.get("news_search_task", []):

        sends.append(
            Send(
                "news_search",
                {
                    "task": task
                }
            )
        )

    # PAPER TASKS
    for task in state.get("paper_search_task", []):

        sends.append(
            Send(
                "papers_search",
                {
                    "task": task
                }
            )
        )

    return sends




# =====================================================
# BUILD SUBGRAPH
# =====================================================

graph = StateGraph(ResearchState)


# =====================================================
# NODES
# =====================================================

graph.add_node(
    "researcher",
    research_node
)

graph.add_node(
    "web_search",
    search_query
)

graph.add_node(
    "reddit_search",
    reddit_search
)

graph.add_node(
    "news_search",
    news_search
)

graph.add_node(
    "papers_search",
    papers_search
)

graph.add_node(
    "aggregate_results",
    aggregate_results
)


# =====================================================
# EDGES
# =====================================================

graph.add_edge(
    START,
    "researcher"
)

graph.add_conditional_edges(
    "researcher",
    route_research
)

graph.add_edge(
    "web_search",
    "aggregate_results"
)

graph.add_edge(
    "reddit_search",
    "aggregate_results"
)

graph.add_edge(
    "news_search",
    "aggregate_results"
)

graph.add_edge(
    "papers_search",
    "aggregate_results"
)

graph.add_edge(
    "aggregate_results",
    END
)


# =====================================================
# EXPORT
# =====================================================

def get_research_graph():

    return graph