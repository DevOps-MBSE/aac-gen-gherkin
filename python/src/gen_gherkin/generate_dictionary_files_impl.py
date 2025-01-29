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

from .gen_dictionary_file_helpers import get_template_properties

plugin_name = "Generate Gherkin Feature Files"


def dictionary_file_generation(architecture_file: str, output_directory: str) -> tuple[str, ExecutionResult]:
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
    messages.append(ExecutionMessage(f"Successfully generated feature file(s) to directory: {output_directory}", MessageLevel.INFO, None, None))
    status = ExecutionStatus.SUCCESS

    return (results, ExecutionResult(plugin_name, "gen-dictionary-file", status, messages))

