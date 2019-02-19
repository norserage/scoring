from ScoringEngine.engine import thread_start, helper, DBEngineHelper
from ScoringEngine import validate_env

validate_env(engine=True)

helper = DBEngineHelper()

thread_start()
