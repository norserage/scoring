import sys

sys.path.append(".")
sys.path.append("../")
sys.path.append("./testers")
sys.path.append("../testers")
sys.path.append("./tests")

from ScoringEngine.engine import set_helper, EngineHelperCommon

class MockEngineHelperBase(EngineHelperCommon):
    def get_current_event(self):
        return None

    def get_service_config_old(self, team_server_id, service_id):
        if team_server_id == 1:
            return {}
        elif team_server_id == 2:
            return {'url': '/test', 'regex': '404'}

    def get_engine_services(self, engine_id):
        return []

    def get_random_user(self, password_database):
        return {}

    def save_new_service_status(self, event, service, status, extra_info):
        self.status = status
        self.info = extra_info

    def get_status(self):
        return self.status, self.info


set_helper(MockEngineHelperBase())

