"""The implementation module for the gen-dictionary-helpers command in the AaC Generate Gherkin Feature Files plugin."""
import yaml
import json
from os import path, makedirs
from typing import Callable

from aac.execute.aac_execution_result import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionMessage,
    MessageLevel,
)
from aac.in_out.parser._parse_source import parse

from .gen_dictionary_file_helpers import get_template_properties

plugin_name = "Generate Gherkin Feature Files"


def before_gen_dictionary_file(architecture_file: str, run_check: Callable) -> ExecutionResult:
    """
    Run the Check AaC command before the gen-dictionary_file command.

    Args:
        architecture_file (str): A path to a YAML file containing an AaC-defined use model
        run_check (Callable): Callback reference to the run_check method from the Check plugin.

    Returns:
        The results of the execution of the check command.
    """
    return run_check(architecture_file, False, False)


def gen_dictionary_file(architecture_file: str, output_directory: str) -> tuple[str, ExecutionResult]:
    """
    Business logic for allowing gen-dictionary-file command to generate dictionary step files.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate dictionary files.
        output_directory (str): The directory into which the generated dictionary files will be written.

    Returns:
        The results of the execution of the gen-dictionary-file command.
    """
    status = ExecutionStatus.GENERAL_FAILURE
    messages: list[ExecutionMessage] = []

    dictionary_steps = parse(architecture_file)
    # for d in dictionary_steps:
    #     print(d.structure)
    # results = get_template_properties(definitions_dictionary)
    # yaml_list = []
    # for model in results:
    #     for acceptance in model["acceptance"]:
    #         yaml_list.append([{"acceptance": acceptance}])

    # new_file = ""
    # for yaml_object in yaml_list:
    #     new_file = new_file + yaml.safe_dump_all(yaml_object, default_flow_style=False, sort_keys=False, explicit_start=True)
    # dictionary_steps = definitions_dictionary.structure
    files = {}
    for dictionary_step_definition in dictionary_steps:
        # print(dictionary_step_definition)
        dictionary_step = dictionary_step_definition.structure["dictionary_step"]
        # print(dictionary_step)
        if dictionary_step["feature_name"] in files.keys():
            files[dictionary_step["feature_name"]][dictionary_step["name"]] = {
                "statements": dictionary_step["statements"],
                "functions": dictionary_step["functions"]
            }
            # print(files[dictionary_step["feature_name"]])
        else:
            files[dictionary_step["feature_name"]] = {
                dictionary_step["name"]: {
                    "statements": dictionary_step["statements"],
                    "functions": dictionary_step["functions"]
                }
            }
            # print(files[dictionary_step["feature_name"]])
    # print(files)

    if len(files.keys()) < 1:
        msg = ExecutionMessage(
            "No applicable acceptance feature to generate a dictionary file",
            MessageLevel.ERROR,
            None,
            None,
        )
        messages.append(msg)
        return None, ExecutionResult(plugin_name, "gen-dictionary-file", ExecutionStatus.GENERAL_FAILURE, messages)
    messages.append(ExecutionMessage(f"Successfully generated dictionary file(s) to directory: {output_directory}", MessageLevel.INFO, None, None))
    status = ExecutionStatus.SUCCESS

    return files, ExecutionResult(plugin_name, "gen-dictionary-file", status, messages)


def after_gen_dictionary_file(architecture_file: str, output_directory: str) -> ExecutionResult:
    """
    Runs Generate on the output of the gen_dictionary_file plugin command.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate a Dictionary File.
        output_directory (str): The directory into which the generated dictionary files will be written.

    Returns:
        The results of the execution of the generate command.

    """
    files, execution_status = gen_dictionary_file(architecture_file, output_directory)
    for key in files.keys():

            # print("======")
        filepath = f"{output_directory}/{key}.json"
        filepath = "_".join(filepath.split())
        makedirs(path.dirname(filepath), exist_ok=True)
        f = open(filepath, "w")
        f.write(json.dumps(files[key], indent=4))
        f.close

    return ExecutionResult(
        plugin_name,
        "gen-dictionary-file",
        ExecutionStatus.SUCCESS,
        [ExecutionMessage(f"Successfully generated dictionary file(s) to directory: {output_directory}", MessageLevel.INFO, None, None)]
    )
