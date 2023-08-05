"""Library defining the interface to a project."""
import json
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, cast

import grpc

from rime_sdk.firewall import Firewall, location_args_to_data_location
from rime_sdk.internal.backend import RIMEBackend
from rime_sdk.internal.proto_utils import get_bin_size_proto, get_threshold_info_proto
from rime_sdk.protos.firewall.firewall_pb2 import (
    ConvertIDsRequest,
    ConvertIDsResponse,
    CreateFirewallFromComponentsRequest,
    CreateFirewallRequest,
    CreateFirewallResponse,
    FirewallComponents,
    FirewallConvIDType,
    FirewallRules,
)
from rime_sdk.protos.project.project_pb2 import GetProjectRequest
from rime_sdk.protos.result_synthesizer.result_message_pb2 import CLIConfig
from rime_sdk.protos.test_run_results.test_run_results_pb2 import (
    ListTestRunsRequest,
    ListTestRunsResponse,
)
from rime_sdk.test_run import TestRun


class ProjectInfo(NamedTuple):
    """This object contains static information that describes a project."""

    project_id: str
    """How to refer to the project in the backend."""
    name: str
    """Name of the project."""
    description: str
    """Description of the project"""


class Project:
    """An interface to a RIME project.

    This object provides an interface for editing, updating, and deleting projects.

    Attributes:
        backend: RIMEBackend
            The RIME backend used to query about the status of the job.
        project_id: str
            The identifier for the RIME project that this object monitors.
    """

    def __init__(self, backend: RIMEBackend, project_id: str) -> None:
        """Contains information about a RIME Project.

        Args:
            backend: RIMEBackend
                The RIME backend used to query about the status of the job.
            project_id: str
                The identifier for the RIME project that this object monitors.
        """
        self._backend = backend
        self._project_id = project_id

    @property
    def project_id(self) -> str:
        """Return the id of this project."""
        return self._project_id

    @property
    def info(self) -> ProjectInfo:
        """Return information about this project."""
        project_req = GetProjectRequest(project_id=self._project_id)
        with self._backend.get_project_manager_stub() as project_manager:
            response = project_manager.GetProject(project_req)
        return ProjectInfo(
            self._project_id,
            response.project.project.name,
            response.project.project.description,
        )

    @property
    def name(self) -> str:
        """Return the name of this project."""
        return self.info.name

    @property
    def description(self) -> str:
        """Return the description of this project."""
        return self.info.description

    def list_test_runs(self) -> Iterator[TestRun]:
        """List the stress test runs associated with the project."""
        with self._backend.get_test_run_results_stub() as test_run_results:
            # Iterate through the pages of projects and break at the last page.
            page_token = ""
            while True:
                if page_token == "":
                    request = ListTestRunsRequest(project_id=self._project_id,)
                else:
                    request = ListTestRunsRequest(page_token=page_token)
                res: ListTestRunsResponse = test_run_results.ListTestRuns(request)
                for test_run in res.test_runs:
                    yield TestRun(self._backend, test_run.test_run_id)
                # Advance to the next page of test cases.
                page_token = res.next_page_token
                # we've reached the last page of test cases.
                if not res.has_more:
                    break

    def create_firewall(
        self,
        name: str,
        bin_size: str,
        test_run_id: str,
        run_ct_schedule: bool = False,
        location_type: Optional[str] = None,
    ) -> Firewall:
        """Create a Firewall for a given project.

        Args:
            name: str
                FW name.
            bin_size: str
                Bin size. Can be `year`, `month`, `week`, `day`, `hour`.
            test_run_id: str
                ID of the stress test run that firewall will be based on.
            run_ct_schedule: bool
                Whether to run the CT on a schedule or not.
            location_type: Optional[str]
                The location type of the data. Can be None or "data_collector"

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the provided values are invalid.
                If the request to the Firewall service failed.

        Example:

        .. code-block:: python

            # Create FW based on foo stress test in project.
            firewall = project.create_firewall(
                "firewall name", "day", "foo")
        """
        bin_size_proto = get_bin_size_proto(bin_size_str=bin_size)
        req = CreateFirewallRequest(
            name=name,
            project_id=self._project_id,
            bin_size=bin_size_proto,
            run_ct_schedule=run_ct_schedule,
            stress_test_run_id=test_run_id,
        )

        if location_type is not None:
            location_info = location_args_to_data_location(location_type)
            req.data_location_info.CopyFrom(location_info)
        try:
            with self._backend.get_firewall_stub() as firewall_tester:
                res = firewall_tester.CreateFirewallFromTestRunID(req)
                res = cast(CreateFirewallResponse, res)
                return Firewall(self._backend, res.firewall_id)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                raise ValueError(
                    f"a test run with this id (`{test_run_id}`)  does not exist"
                )
            raise ValueError(rpc_error.details()) from None

    def create_firewall_from_components(
        self,
        name: str,
        bin_size: str,
        stress_test_config: Dict[str, Any],
        firewall_rules: List[Dict[str, Any]],
        threshold_infos: List[dict],
        run_ct_schedule: bool = False,
        location_type: Optional[str] = None,
    ) -> Firewall:
        """Create a Firewall for a given project.

        Args:
            name: str
                FW name.
            bin_size: str Can be `year`, `month`, `week`, `day`, `hour`.
            stress_test_config: RIME Config that indicates the testing, model, and
                data configurations
            firewall_rules: Firewall Rules to update the firewall with.
            threshold_infos: Threshold info for each summary metric.
            run_ct_schedule: bool
                Whether to run the CT on a schedule or not.
            location_type: Optional[str]
                The location type of the data. Can be None or "data_collector"

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the provided values are invalid.
                If the request to the Firewall service failed.

        Example:

        .. code-block:: python

            # Create FW manually from components.
           stress_test_config = {
                "data_info": {
                    "pred_col": "preds",
                    "label_col": "label",
                    "ref_path": "s3://my-bucket/my-data.csv",
                },
                "model_info": {"path": "s3://model-test-bucket/model.py",},
                "model_task": "Binary Classification",
            }
            firewall_rules = [
                {
                    "test_name": "Unseen Categorical",
                    "description": "Value must be in a required set of values",
                    "is_transformation": False,
                    "firewall_configs": [
                        {
                            "rule_info": {
                                "feature_names": ["city"],
                                "flagged_action": "FLAG",
                            }
                        }
                    ],
                }
            ]
            metric_thresholds = [
                {
                    "direction": "below",
                    "low": 0.999,
                    "medium": 0.99,
                    "high": 0.9,
                    "metric_name": "accuracy",
                }
            ]
            firewall = project.create_firewall_from_components(
                "firewall name",
                "day",
                stress_test_config,
                firewall_rules,
                metric_thresholds,
            )
        """
        bin_size_proto = get_bin_size_proto(bin_size_str=bin_size)
        cli_config_pb = CLIConfig(data=json.dumps(stress_test_config).encode("utf-8"))
        firewall_rules_pb = FirewallRules(
            data=json.dumps(firewall_rules).encode("utf-8")
        )
        metric_thresholds = [
            get_threshold_info_proto(threshold_dict)
            for threshold_dict in threshold_infos
        ]
        req = CreateFirewallFromComponentsRequest(
            name=name,
            project_id=self._project_id,
            bin_size=bin_size_proto,
            run_ct_schedule=run_ct_schedule,
            components=FirewallComponents(
                cli_config=cli_config_pb,
                firewall_rules=firewall_rules_pb,
                threshold_infos=metric_thresholds,
            ),
        )
        if location_type is not None:
            location_info = location_args_to_data_location(location_type)
            req.data_location_info.CopyFrom(location_info)
        with self._backend.GRPCErrorHandler():
            with self._backend.get_firewall_stub() as firewall_tester:
                res = firewall_tester.CreateFirewallFromComponents(req)
                res = cast(CreateFirewallResponse, res)
                return Firewall(self._backend, res.firewall_id)

    def _get_firewall_id(self) -> Optional[str]:
        src_type = FirewallConvIDType.FIREWALL_CONV_ID_TYPE_PROJECT_ID
        dst_type = FirewallConvIDType.FIREWALL_CONV_ID_TYPE_FIREWALL_ID
        req = ConvertIDsRequest(
            src_type=src_type, dst_type=dst_type, src_ids=[self._project_id]
        )
        with self._backend.GRPCErrorHandler():
            with self._backend.get_firewall_stub() as firewall_tester:
                res: ConvertIDsResponse = firewall_tester.ConvertIDs(req)
        src_dst_id_mapping = res.src_dst_id_mapping
        if self._project_id not in src_dst_id_mapping:
            return None
        # Current backend functionality is to return mapping for everything,
        # but with empty string if no firewall exists.
        firewall_id = src_dst_id_mapping.get(self._project_id, "")
        if firewall_id == "":
            return None
        return firewall_id

    def get_firewall(self) -> Firewall:
        """Get the active Firewall for a project if it exists.

        Query the backend for an active `Firewall` in this project which
        can be used to perform Firewall operations. If there is no active
        Firewall for the project, this call will error.

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the Firewall does not exist.

        Example:

        .. code-block:: python

            # Get FW if it exists.
            firewall = project.get_firewall()
        """
        firewall_id = self._get_firewall_id()
        if firewall_id is None:
            raise ValueError("No firewall found for given project.")
        return Firewall(self._backend, firewall_id)

    def has_firewall(self) -> bool:
        """Check whether a project has a firewall or not."""
        firewall_id = self._get_firewall_id()
        return firewall_id is not None

    def delete_firewall(self) -> None:
        """Delete firewall for this project if exists."""
        firewall = self.get_firewall()
        firewall.delete_firewall()
