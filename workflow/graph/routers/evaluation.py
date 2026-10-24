from ..states.analyst_state import AnalystState
import logging

from logging_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

MAX_ITERATIONS = 1
QUALITY_THRESHOLD = 3.5

def evaluation_router(state: AnalystState):
    score = state["evaluation"]["content_quality_score"]
    iteration = state.get("research_iteration", 0)
    logger.info(f"research round -> {iteration}, score -> {score}")

    if score <= QUALITY_THRESHOLD and iteration < MAX_ITERATIONS:
        logger.info(f"Evaluator chose refinement (score {score}, round {iteration})")
        return "refinement"

    logger.info(f"Evaluator chose insights (score {score})")
    return "insights"