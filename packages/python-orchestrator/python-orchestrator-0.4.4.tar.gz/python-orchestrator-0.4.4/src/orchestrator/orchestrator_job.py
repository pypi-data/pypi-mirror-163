from pprint import pprint
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from orchestrator.exceptions import OrchestratorMissingParameters
from urllib.parse import urlencode
from orchestrator.orchestrator_logs import Log


class Job(OrchestratorHTTP):
    STOP_ARGS = [
        "Stopping",
        "Terminating",
        "Faulted",
        "Successful",
        "Stopped",
        "Suspended",
        "Resumed"
    ]

    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, job_id=None, job_key=None, job_name=None, access_token=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not job_key or not job_id:
            raise OrchestratorMissingParameters(
                message="Required parameter(s) missing: job_id/job_id",
                error_message="Missing parameters")
        self.tenant_name = tenant_name
        self.access_token = access_token
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        self.folder_id = folder_id
        self.folder_name = folder_name
        self.id = job_id
        self.key = job_key
        self.name = job_name
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):
        return f"Key: {self.key}\nName: {self.name}"

    def info(self):
        endpoint = f"/Jobs({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def stop(self):
        """
        Stops the given job
        """
        endpoint = f"/Jobs({self.id})"
        uipath_svc = "/UiPath.Server.Configuration.OData.StopJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        cancel_body = {
            "strategy": "SoftStop"
        }
        return self._post(url, body=cancel_body)

    def kill(self):
        """
        Kill the given job
        """
        endpoint = f"/Jobs({self.id})"
        uipath_svc = "/UiPath.Server.Configuration.OData.StopJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        cancel_body = {
            "strategy": "Kill"
        }
        return self._post(url, body=cancel_body)

    def restart(self):
        """
        Restarts the given job
        """
        endpoint = f"/Jobs"
        uipath_svc = "/UiPath.Server.Configuration.OData.RestartJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        restart_body = {
            "jobId": self.id
        }
        return self._post(url, body=restart_body)

    def resume(self):
        """
        Restarts the given job
        """
        endpoint = f"/Jobs"
        uipath_svc = "/UiPath.Server.Configuration.OData.ResumeJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        resume_body = {
            "jobKey": self.key
        }
        return self._post(url, body=resume_body)

    def get_logs(self, traces=["Info", "Error", "Warn", "Fatal"]):
        # need a Log Message class
        endpoint = "/RobotLogs"
        fmt_traces = tuple(traces)
        query_param = urlencode({
            "$filter": f"ProcessName eq '{self.name}' and Level in {fmt_traces} and JobKey eq {self.key}",
            "$orderby": "TimeStamp desc"
        })
        pprint({
            "$filter": f"ProcessName eq '{self.name}' and Level in {fmt_traces} and JobKey eq {self.key}",
            "$orderby": "TimeStamp desc"
        })
        url = f"{self.base_url}{endpoint}?{query_param}"
        logs = self._get(url)["value"]
        # pprint(data[0])
        return [Log(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.session, log["Message"], log["Level"], self.key, log["TimeStamp"]) for log in logs]

    def should_stop(self):
        """Returns True if a terminating signal is sent from Orchestrator, false otherwise"""
        data = self.info()
        status = data["State"]
        if status in self.STOP_ARGS:
            return True
        else:
            return False
