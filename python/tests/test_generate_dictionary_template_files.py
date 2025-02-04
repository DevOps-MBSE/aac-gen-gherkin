from click.testing import CliRunner
from os import listdir, path
from tempfile import TemporaryDirectory
from typing import Tuple
from unittest import TestCase

from aac.execute.aac_execution_result import ExecutionStatus
from aac.execute.command_line import cli, initialize_cli

from gen_gherkin.generate_dictionary_files_impl import (
    plugin_name,
    gen_dictionary_file,
)


class TestGenerateDictionaryFiles(TestCase):

    def test_gen_dictionary_file(self):

        # Like in core going to rely on the CLI testing for this, have not determined what we would like to test here
        pass

    def run_gen_dictionary_file_cli_command_with_args(
        self, args: list[str]
    ) -> Tuple[int, str]:
        """Utility function to invoke the CLI command with the given arguments."""
        initialize_cli()
        runner = CliRunner()
        result = runner.invoke(cli, ["gen-dictionary-file"] + args)
        exit_code = result.exit_code
        std_out = str(result.stdout)
        output_message = std_out.strip().replace("\x1b[0m", "")
        return exit_code, output_message

    def test_cli_gen_dictionary_file(self):
        with TemporaryDirectory() as temp_dir:
            aac_file_path = path.join(path.dirname(__file__), "dictionary/dictionary_step.aac")
            args = [aac_file_path, temp_dir]
            exit_code, output_message = (self.run_gen_dictionary_file_cli_command_with_args(args))
            self.assertEqual(0, exit_code)
            self.assertIn("Successfully generated dictionary file(s) to directory", output_message)

            temp_dir_files = listdir(temp_dir)
            self.assertNotEqual(0, len(temp_dir_files))
            for temp_file in temp_dir_files:
                self.assertTrue(temp_file.find(".json"))
                temp_file_content = open(path.join(temp_dir, temp_file), "r")
                temp_content = temp_file_content.read()
                self.assertIn('"functions":', temp_content)
                self.assertIn('"statements":', temp_content)
                temp_file_content.close()


    def test_cli_gen_gherkin_behaviors_failure(self):
        with TemporaryDirectory() as temp_dir:
            aac_file_path = path.join(path.dirname(__file__), "calc/spec/Add_SRS.yaml")
            args = [aac_file_path, temp_dir]
            exit_code, output_message = (self.run_gen_dictionary_file_cli_command_with_args(args))
            self.assertNotEqual(0, exit_code)
            self.assertIn("No applicable acceptance feature to generate a dictionary file", output_message)
