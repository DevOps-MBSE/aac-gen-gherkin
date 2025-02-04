"""Helper methods for extracting and sorting pertinent data for use in generating dictionary files."""
from re import sub

from aac.context.definition import Definition
from aac.context.language_context import LanguageContext


def collect_models(parsed_models: list[dict]) -> list:
    """
    Return a structured dict like parsed_models, but only consisting of model definitions.

    Args:
        parsed_models (list(dict)): A list of parsed definitions

    Returns:
        list: A list containing only model definitions.
    """
    collected_models = []
    for model in parsed_models:
        if model.get_root_key() == "model":
            collected_models.append(model)

    return collected_models


def search_for_step_in_dictionaries(step: str) -> dict:
    """
    Searches through Language Context to find the specified step.

    Args:
        step (str): A given, when, or then step used to search for dictionary steps.

    Returns:
        dict: The relevant dictionary step files.
    """
    context = LanguageContext()
    dictionary_definitions = context.get_definitions_by_root("dictionary_step")
    dictionary_statements = []
    dictionary_functions = []
    for dictionary in dictionary_definitions:
        if "statements" in dictionary.content:
            for statement in dictionary.structure["dictionary_step"]["statements"]:
                if statement in step:
                    dictionary_statements.extend(dictionary.structure["dictionary_step"]["statements"])
                    dictionary_functions.extend(dictionary.structure["dictionary_step"]["functions"])

    if len(dictionary_statements) < 1:
        dictionary_statements = ["No statements found"]
    if len(dictionary_functions) < 1:
        dictionary_functions = ["No functions found"]
    return {
        "statements": dictionary_statements,
        "functions": dictionary_functions
    }


def sanitize_scenario_step_entry(step: str) -> str:
    """
    Remove any conflicting keyword from the scenario step.

    Args:
        step (str): A scenario step.

    Returns:
        str: The scenario step with conflicting keywords removed.
    """
    if does_step_start_with_gherkin_keyword(step):
        return step.split(None, 1)[1]
    return step


def collect_and_sanitize_scenario_steps(scenario: dict) -> list[dict]:
    """
    Collect and sanitize scenario steps then return template properties for a 'scenarios' entry.

    Args:
        scenario (dict): The scenario definition from a model

    Returns:
        A list of template properties
    """
    steps = {}
    if "requirements" in scenario:
        steps["scenario_requirements"] = scenario["requirements"]
    if "given" in scenario:
        for given_step in scenario["given"]:
            steps[sanitize_scenario_step_entry(given_step)] = search_for_step_in_dictionaries(given_step)
    if "when" in scenario:
        for when_step in scenario["when"]:
            steps[sanitize_scenario_step_entry(when_step)] = search_for_step_in_dictionaries(when_step)
    if "then" in scenario:
        for then_step in scenario["then"]:
            steps[sanitize_scenario_step_entry(then_step)] = search_for_step_in_dictionaries(then_step)
    scenario_steps = {
        "name": scenario["name"],
        "scenario": {scenario["name"]: steps}
    }
    return scenario_steps


def collect_acceptance_entry_properties(name: str, acceptance_entry: dict) -> list[dict]:
    """
    Produce a list of template property dictionaries from a acceptance entry.

    Args:
        behavior_entry (dict): The acceptance definition from a model

    Returns:
        A list of template property dictionaries.
    """
    feature_name = acceptance_entry["name"]
    feature_name = sub(" ", "_", feature_name)
    feature_name = sub(r"\W+", "", feature_name)
    scenario_lists = []

    if "scenarios" in acceptance_entry:
        for scenario in acceptance_entry["scenarios"]:
            scenario_lists.append(collect_and_sanitize_scenario_steps(scenario))
    return {
        "name": feature_name,
        "feature": scenario_lists
    }


def does_step_start_with_gherkin_keyword(step: str) -> bool:
    """
    Check if a string starts with a Gherkin keyword. Gherkin keywords can be found here: https://cucumber.io/docs/gherkin/reference/#keywords.

    Args:
        step (str): The scenario step being checked

    Returns:
        A boolean value signifying whether the step begins with a gherkin keyword.
    """
    gherkin_keywords = [
        "Feature",
        "Rule",
        "Example",
        "Given",
        "When",
        "Then",
        "And",
        "But",
        "Background",
        "Example",
        "Scenario",
        "Scenario Outline",
        "Scenario Template",
    ]

    return step.startswith(tuple(gherkin_keywords))


def collect_model_acceptance_properties(model: Definition) -> dict:
    """
    Produce a template property dictionary for each acceptance entry in a model.

    Args:
        model (Definition): A model containing behavior properties

    Returns:
        A dictionary containing a list of behaviors and a list of requirements
    """
    acceptances = []
    acceptance_lists = []
    if "behavior" in model.content:
        for behavior in model.structure["model"]["behavior"]:
            if "acceptance" in behavior:
                for acceptance in behavior["acceptance"]:
                    acceptances.append(acceptance)

    for acceptance in acceptances:
        acceptance_lists.append(collect_acceptance_entry_properties(model.name, acceptance))

    returning_list = {
        "name": model.name,
        "acceptance": acceptance_lists,
    }
    return returning_list


def get_template_properties(parsed_models: dict) -> list[dict]:
    """
    Generate a list of template property dictionaries for each dictionary steps file to generate.

    Args:
        parsed_models (dict): a dict of models where the key is the model name and the value is the model dict.

    Returns:
        list[dict]: a list of template property dictionaries
    """

    return [collect_model_acceptance_properties(model) for model in collect_models(parsed_models)]


def create_json_files(dictionary_steps_definition: Definition):
    dictionary_steps = dictionary_steps_definition.structure["dictionary_step"]
    files = {}
    print(dictionary_steps)
    for dictionary_step in dictionary_steps:
        print(dictionary_step)
        if dictionary_step["feature_name"] in files.keys:
            files[dictionary_step["feature_name"]].append({
                dictionary_step.structure["name"]: {
                    "statements": dictionary_step["statements"],
                    "functions": dictionary_step["functions"]
                }
            })
        else:
            files[dictionary_step["feature_name"]] = [{
                dictionary_step.structure["name"]: {
                    "statements": dictionary_step["statements"],
                    "functions": dictionary_step["functions"]
                }
            }]
    return files

