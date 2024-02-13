import os
import tempfile

from metaflow.flowspec import FlowSpec

from dbt_metaflow.metaflow import load_module


def test_load_module():
    with tempfile.TemporaryDirectory() as tmpdirname:
        module_name = "temp_module"
        module_path = os.path.join(tmpdirname, f"{module_name}.py")

        with open(module_path, "w") as f:
            f.write("test_var = 'Hello, world!'")

        loaded_module = load_module(module_name, tmpdirname)

        assert hasattr(loaded_module, "test_var"), "Module does not have the attribute 'test_var'"
        assert loaded_module.test_var == "Hello, world!", "The value of 'test_var' is not as expected"


def test_load_flow_module():
    parent_dir = os.path.join(os.path.dirname(__file__), "test_flows")
    module_name = "minimum_flow"

    loaded_module = load_module(module_name, parent_dir)
    assert hasattr(loaded_module, "MinimumFlow"), "Module does not have the class 'MinimumFlow'"
    flow_instance = loaded_module.MinimumFlow
    assert issubclass(flow_instance, FlowSpec), "The instance is not a FlowSpec"
