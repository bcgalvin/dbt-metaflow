import importlib
import os
import sys
from types import ModuleType
from typing import Any, Callable, List, Optional

from metaflow import cli
from metaflow.client.core import DataArtifact, Run
from metaflow.exception import MetaflowDataMissing


def load_module(module_name: str, parent_dir: str) -> ModuleType:
    """
    Dynamically loads a module from a specified directory.

    Parameters:
    - module_name: The name of the module to load.
    - parent_dir: The directory containing the module.

    Returns:
    - The loaded module.
    """
    original_sys_path = list(sys.path)
    try:
        sys.path.append(str(parent_dir))
        mod = importlib.import_module(module_name)
    finally:
        sys.path = original_sys_path
    return mod


class FlowHandler:
    def __init__(
        self,
        flow_file_path: str,
        flow_class: str,
        module_loader: Callable[[str, str], ModuleType] = load_module,
    ):
        self.flow_file_path: str = flow_file_path
        self.flow_class: str = flow_class
        self.module_loader: Callable[[str, str], ModuleType] = module_loader

    def load_flow(self, **kwargs: Any) -> Any:
        """
        Loads a flow with given parameters + options
        """

        flow_module = load_module(self.flow_class, self.flow_file_path)
        flow_class = getattr(flow_module, self.flow_class)
        return flow_class(use_cli=False, **kwargs)

    def execute_flow(self, flow: Any, command: str, run_options: Optional[List[str]] = None) -> None:
        """
        Executes a run of a specified flow with a given command w options
        """
        run_options = run_options or []
        try:
            cli_args = [command, *run_options]
            cli.main(flow, args=cli_args, entrypoint=[sys.executable, self.flow_file_path])  # type: ignore[no-untyped-call]
        finally:
            sys.path.remove(str(os.path.dirname(self.flow_file_path)))

    def get_run_artifacts(self, run: Run, keys: List[str]) -> List[Any]:
        """
        Retrieves specified artifacts from a given run, if the run was successful.

        Parameters:
        - run: The Metaflow Run object to retrieve artifacts from.
        - keys: A list of artifact keys to retrieve.

        Returns:
        - A list of artifact data for the given keys, if available.
        """
        if run.successful and run.data is not None:
            artifacts = run.data._artifacts
            artifacts_out: List[Optional[DataArtifact]] = [artifacts.get(x) for x in keys]
            return [x.data for x in artifacts_out if x is not None]
        no_data_msg = f"No data available for run {run.id} in flow {self.flow_class}."
        raise MetaflowDataMissing(no_data_msg)  # type: ignore[no-untyped-call]
