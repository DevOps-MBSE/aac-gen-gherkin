from behave import *
from typing import Tuple
from os import path

from aac.execute.aac_execution_result import ExecutionStatus
from aac.execute.command_line import cli, initialize_cli
from aac.plugins.check import run_check

from gen_gherkin.generate_gherkin_feature_files_impl import (
    plugin_name,
    gen_gherkin_behaviors,
)
architecture_file = "../calc/model/calculator.yaml"


def run_gen_gherkin_behaviors_cli_command_with_args(
        self, args: list[str]
    ) -> Tuple[int, str]:
        """Utility function to invoke the CLI command with the given arguments."""
        initialize_cli()
        runner = CliRunner()
        result = runner.invoke(cli, ["gen-gherkin-behaviors"] + args)
        exit_code = result.exit_code
        std_out = str(result.stdout)
        output_message = std_out.strip().replace("\x1b[0m", "")
        return exit_code, output_message


@given(u'The "{architecture_file}" contains a valid architecture.')
def step_check(context, architecture_file):
    result = run_check(architecture_file, False, False)
    assert (result.is_success())

@when(u'The aac app is run with the gen-gherkin-behaviors command and a valid architecture file.')
def step_impl(context, architecture_file):
    run_gen_gherkin_behaviors_cli_command_with_args(args=[architecture_file])

