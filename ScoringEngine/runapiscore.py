from ScoringEngine.engine import thread_start, setup_helper, DBEngineHelper
from ScoringEngine import validate_env

validate_env(engine=True)

setup_helper(db=False)

thread_start()
