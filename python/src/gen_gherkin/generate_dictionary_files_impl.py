"""The implementation module for the gen-dictionary-file command in the AaC Generate Gherkin plugin."""
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

plugin_name = "Generate Dictionary Step Files"


def before_gen_dictionary_file(architecture_file: str, run_check: Callable) -> ExecutionResult:
    """
    Run the Check AaC command before the gen-dictionary-file command.

    Args:
        architecture_file (str): A path to a YAML file containing an AaC-defined model.
        run_check (Callable): Callback reference to the run_check method from the Check plugin.

    Returns:
        ExecutionResult: The results of the execution of the check command.
    """
    return run_check(architecture_file, False, False)


def gen_dictionary_file(architecture_file: str, output_directory: str) -> tuple[str, ExecutionResult]:
    """
    Business logic for allowing gen-dictionary-file command to generate dictionary step files.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate dictionary files.
        output_directory (str): The directory into which the generated dictionary files will be written.

    Returns:
        tuple[str, ExecutionResult]: The results of the execution of the gen-dictionary-file command.
    """
    status = ExecutionStatus.GENERAL_FAILURE
    messages: list[ExecutionMessage] = []

    dictionary_steps = parse(architecture_file)
    files = {}

    for dictionary_step_definition in dictionary_steps:
        if "dictionary_step" in dictionary_step_definition.content:
            dictionary_step = dictionary_step_definition.structure["dictionary_step"]
            if dictionary_step["feature_name"] in files.keys():
                files[dictionary_step["feature_name"]]["steps"].append({
                    "name": dictionary_step["name"],
                    "statements": dictionary_step["statements"],
                    "functions": dictionary_step["functions"]
                })
            else:
                files[dictionary_step["feature_name"]] = {
                    "name": dictionary_step["feature_name"],
                    "steps": [{
                        "name": dictionary_step["name"],
                        "statements": dictionary_step["statements"],
                        "functions": dictionary_step["functions"]
                    }]
                }
    file_list = []
    for key in files.keys():
        file_list.append({"dictionary": files[key]})

    yaml_list = ""
    for key in files.keys():
        print(files[key])
        yaml_list = yaml_list + yaml.safe_dump_all(file_list, default_flow_style=False, sort_keys=False, explicit_start=True)

    if len(files.keys()) < 1:
        msg = ExecutionMessage(
            "No step definitions to generate a dictionary steps file.",
            MessageLevel.ERROR,
            None,
            None,
        )
        messages.append(msg)
        return None, ExecutionResult(plugin_name, "gen-dictionary-file", status, messages)
    messages.append(ExecutionMessage(f"Successfully generated dictionary file(s) to directory: {output_directory}", MessageLevel.INFO, None, None))
    status = ExecutionStatus.SUCCESS

    return yaml_list, ExecutionResult(plugin_name, "gen-dictionary-file", status, messages)


def after_gen_dictionary_file(architecture_file: str, output_directory: str, run_generate: Callable) -> ExecutionResult:
    """
    Runs Generate on the output of the gen_dictionary_file plugin command.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate a Dictionary File.
        output_directory (str): The directory into which the generated dictionary files will be written.
        run_generate (Callable): The Generation function which generates a feature file

    Returns:
        The results of the execution of the generate command.

    """
    new_file, execution_status = gen_dictionary_file(architecture_file, output_directory)

    generator_file = path.abspath(path.join(path.dirname(__file__), "./dictionary_generator.aac"))

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
