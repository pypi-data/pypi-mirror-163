from orchestrator.orchestrator_http import OrchestratorHTTP
from orchestrator.exceptions import OrchestratorMissingParameters
from urllib.parse import urlencode
import requests

__all__ = ["Process"]


class Process(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None, process_id=None, process_title=None, process_version=None, process_key=None, access_token=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id)
        if not process_id:
            raise OrchestratorMissingParameters(
                message="Required parameter(s) missing: process_id",
                error_message="Required parameter(s) missing: process_id",
            )
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        self.id = process_id
        self.access_token = access_token
        self.tenant_name = tenant_name
        self.title = process_title
        self.version = process_version
        self.key = process_key
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):
        return f"Process Id: {self.id} \nTitle: {self.title} \nVersion: {self.version} \nKey: {self.key} \nFolder Id: {self.folder_id}"

    def info(self):
        endpoint = "/Processes"
        query_param = urlencode({
            "$filter": f"Key eq '{self.key}'"
        })
        url = f"{self.base_url}{endpoint}?{query_param}"
        return self._get(url)["value"][0]

    def versions(self):
        endpoint = "/Processes"
        uipath_svc = f"/UiPath.Server.Configuration.OData.GetProcessVersions(processId='{self.id}')"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)["value"]

    def parameters(self):
        endpoint = "/Processes"
        uipath_svc = f"/UiPath.Server.Configuration.OData.GetArguments(key='{self.key}')"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)
