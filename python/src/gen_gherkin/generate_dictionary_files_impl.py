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

    definitions_dictionary = parse(architecture_file)

    results = get_template_properties(definitions_dictionary)
    yaml_list = []
    for model in results:
        for acceptance in model["acceptance"]:
            yaml_list.append([{"acceptance": acceptance}])

    new_file = ""
    for yaml_object in yaml_list:
        new_file = new_file + yaml.safe_dump_all(yaml_object, default_flow_style=False, sort_keys=False, explicit_start=True)

    if len(results) < 1:
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

    return results, ExecutionResult(plugin_name, "gen-dictionary-file", status, messages)


def after_gen_dictionary_file(architecture_file: str, output_directory: str, run_generate: Callable) -> ExecutionResult:
    """
    Runs Generate on the output of the gen_dictionary_file plugin command.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate a Dictionary File.
        output_directory (str): The directory into which the generated dictionary files will be written.
        run_generate (Callable): The Generation function which generates a dictionary file

    Returns:
        The results of the execution of the generate command.

    """
    new_file, execution_status = gen_dictionary_file(architecture_file, output_directory)
    for model in new_file:
        for acceptance in model["acceptance"]:
            for feature in acceptance["feature"]:
                filepath = f"{output_directory}/{acceptance['name']}_{feature['name']}.json"
                filepath = "_".join( filepath.split() )
                makedirs(path.dirname(filepath), exist_ok=True)
                f = open(filepath, "w")
                f.write(json.dumps(feature["scenario"], indent=4))

    return ExecutionResult(
        plugin_name,
        "gen-dictionary-file",
        ExecutionStatus.SUCCESS,
        [ExecutionMessage(f"Successfully generated dictionary file(s) to directory: {output_directory}", MessageLevel.INFO, None, None)]
    )

    # generator_file = path.abspath(path.join(path.dirname(__file__), "./dictionary_generator.aac"))

    # return run_generate(
    #     aac_plugin_file=new_file,
    #     generator_file=generator_file,
    #     code_output=output_directory,
    #     test_output="",
    #     doc_output="",
    #     no_prompt=True,
    #     force_overwrite=True,
    #     evaluate=False,
    # )
