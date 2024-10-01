"""Steps for the behave gen-gherkin testing."""
from behave import given, when, then
from click.testing import CliRunner
from shutil import rmtree
from typing import Tuple
from os import listdir, path

from aac.execute.command_line import cli, initialize_cli
from aac.plugins.check import run_check

architecture_file = "../calc/model/calculator.yaml"


def run_gen_gherkin_behaviors_cli_command_with_args(
        args: list[str]
) -> Tuple[int, str]:
    """Utility function to invoke the CLI command with the given arguments."""
    initialize_cli()
    runner = CliRunner()
    result = runner.invoke(cli, ["gen-gherkin-behaviors"] + args)
    exit_code = result.exit_code
    std_out = str(result.stdout)
    output_message = std_out.strip().replace("\x1b[0m", "")
    return exit_code, output_message


@given('The "{architecture_file}" contains a valid architecture.')
def step_check(context, architecture_file: str):
    """
    Runs check on the given architecture_file.

    Args:
        context: Active behave context.
        architecture_file (str): The aac file being used for feature file generation
    """
    result = run_check(architecture_file, False, False)
    context.architecture_file = architecture_file
    assert (result.is_success())


@when('The aac app is run with the gen-gherkin-behaviors command, a valid architecture file, and an "{output_directory}".')
def step_impl(context, output_directory):
    """
    Runs the aac-gen-gherkin command.

    Args:
        context: Active behave context.
        output_directory (str): The directory that the gen-gherkin command will output to.
    """
    context.output_directory = output_directory
    exit_code, message = run_gen_gherkin_behaviors_cli_command_with_args(args=[context.architecture_file, output_directory])
    assert (0 == exit_code)


@then('Gherkin feature files are written to an output directory.')
def step_result(context):
    """
    Checks to ensure the command produced output.

    Args:
        context: Active behave context.
    """
    temp_dir_files = listdir(context.output_directory)
    assert (0 != len(temp_dir_files))
    rmtree(context.output_directory)
    assert (path.isdir(context.output_directory) is False)
