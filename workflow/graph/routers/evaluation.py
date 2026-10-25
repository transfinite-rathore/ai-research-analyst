from ..states.analyst_state import AnalystState
import logging
from config.config_manager import get_config
from logging_config import setup_logger
from config.latency_tracker import track_time

config=get_config()
setup_logger()
logger = logging.getLogger(__name__)

MAX_ITERATIONS = config["evaluation_max_iteration"]
QUALITY_THRESHOLD = config["evaluation_quality_threshold"]

@track_time
def evaluation_router(state: AnalystState):
    score = state["evaluation"]["content_quality_score"]
    iteration = state.get("research_iteration", 0)
    logger.info(f"research round -> {iteration}, score -> {score}")

    if score <= QUALITY_THRESHOLD and iteration < MAX_ITERATIONS:
        logger.info(f"Evaluator chose refinement (score {score}, round {iteration})")
        return "refinement"

    logger.info(f"Evaluator chose insights (score {score})")
    return "insights"