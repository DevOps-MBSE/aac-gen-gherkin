"""The AaC Generate Gherkin Feature Files plugin implementation module."""

# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-plugin, and it won't be overwritten if the file already exists.

# There may be some unused imports depending on the definition of the plugin, be sure to remove unused imports.
import yaml

from os import path
from typing import Callable

from aac.execute.aac_execution_result import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionMessage,
    MessageLevel,
)
from aac.in_out.parser._parse_source import parse

from .gen_gherkin_helpers import get_template_properties

plugin_name = "Generate Gherkin Feature Files"


def before_gen_gherkin_behaviors(architecture_file: str, run_check: Callable) -> ExecutionResult:
    """
    Run the Check AaC command before the gen-gherkin-behaviors command.

    Args:
        architecture_file (str): A path to a YAML file containing an AaC-defined use model
        run_check (Callable): Callback reference to the run_check method from the Check plugin.

    Returns:
        The results of the execution of the check command.
    """
    return run_check(architecture_file, False, False)


def gen_gherkin_behaviors(
    architecture_file: str, output_directory: str
) -> tuple[str, ExecutionResult]:
    """
    Business logic for allowing gen-gherkin-behaviors command to perform Generate Gherkin feature files from AaC model behavior scenarios.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate Gherkin feature files.
        output_directory (str): The directory into which the generated Gherkin feature files will be written.

    Returns:
        The results of the execution of the gen-gherkin-behaviors command.
    """
    status = ExecutionStatus.GENERAL_FAILURE
    messages: list[ExecutionMessage] = []

    definitions_dictionary = parse(architecture_file)

    results = get_template_properties(definitions_dictionary)

    yaml_list = []
    for model in results:
        behavior_list = []
        for behavior in model["behaviors"]:
            yaml_list.append([{"behavior": behavior}])


    new_file = ""
    for yaml_object in yaml_list:
        new_file = new_file + yaml.safe_dump_all(yaml_object, default_flow_style=False, sort_keys=False, explicit_start=True)

    if len(yaml_list) < 1:
        msg = ExecutionMessage(
            "No applicable behavior to generate a feature file",
            MessageLevel.ERROR,
            None,
            None,
        )
        messages.append(msg)
        return None, ExecutionResult(plugin_name, "gen-gherkin-behaviors", ExecutionStatus.GENERAL_FAILURE, messages)

    messages.append(ExecutionMessage(f"Successfully generated feature file(s) to directory: {output_directory}", MessageLevel.INFO, None, None))
    status = ExecutionStatus.SUCCESS

    return new_file, ExecutionResult(plugin_name, "gen-gherkin-behaviors", status, messages)


def after_gen_gherkin_behaviors(architecture_file: str, output_directory: str, run_generate: Callable) -> ExecutionResult:
    """
    Runs Generate on the output of the gen_gherkin_behaviors plugin.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate Gherkin feature files.
        output_directory (str): The directory into which the generated Gherkin feature files will be written.
        run_generate (Callable): The Generation function which generates a feature file

    Returns:
        The results of the execution of the generate command.

    """
    new_file, execution_status = gen_gherkin_behaviors(architecture_file, output_directory)

    generator_file = path.abspath(path.join(path.dirname(__file__), "./behavior_generator.aac"))

    return run_generate(
        aac_plugin_file=new_file,
        generator_file=generator_file,
        code_output=output_directory,
        test_output="",
        doc_output="",
        no_prompt=True,
        force_overwrite=True,
        evaluate=False,
    )
