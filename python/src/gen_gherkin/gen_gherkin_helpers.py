"""Helper methods for extracting and sorting pertinent data for use in generating feature files."""
from aac.context.definition import Definition


def collect_models(parsed_models: list[dict]) -> list:
    """
    Return a structured dict like parsed_models, but only consisting of model definitions.

    Args:
        parsed_models (list(dict)): A list of parsed definitions

    Returns:
        A list containing only model definitions
    """
    collected_models = []
    for model in parsed_models:
        if model.get_root_key() == "model":
            collected_models.append(model)

    return collected_models


def sanitize_scenario_step_entry(step: str) -> str:
    """
    Remove any conflicting keyword from the scenario step.

    Args:
        step (str): A scenario step

    Returns:
        The scenario step with conflicting keywords removed
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
    scenario_steps = [
        {
            "name": scenario["name"],
            "givens": [sanitize_scenario_step_entry(given) for given in scenario["given"]],
            "whens": [sanitize_scenario_step_entry(when) for when in scenario["when"]],
            "thens": [sanitize_scenario_step_entry(then) for then in scenario["then"]],
        }
    ]
    if "requirements" in scenario:
        scenario_steps[0]["scenario_requirements"] = scenario["requirements"]
    return scenario_steps


def collect_behavior_entry_properties(name: str, behavior_entry: dict) -> list[dict]:
    """
    Produce a list of template property dictionaries from a behavior entry.

    Args:
        behavior_entry (dict): The behavior definition from a model

    Returns:
        A list of template property dictionaries.
    """
    feature_name = behavior_entry["name"]
    if "description" in behavior_entry:
        feature_description = behavior_entry["description"]
    else:
        feature_description = "TODO: Fill out this feature description."  # noqa: T101
    behavior_requirements = []
    scenario_lists = []

    for acceptance in behavior_entry["acceptance"]:
        for scenario in acceptance["scenarios"]:
            scenario_lists.append(collect_and_sanitize_scenario_steps(scenario))
    if "requirements" in behavior_entry:
        for requirement in behavior_entry["requirements"]:
            behavior_requirements.append(requirement)
    return [
        {
            "name": name,
            "feature": {"name": feature_name, "description": feature_description},
            "scenarios": [scenario for scenario_list in scenario_lists for scenario in scenario_list],
            "behavior_requirements": behavior_requirements,
        }
    ]


def collect_model_behavior_properties(model: Definition) -> dict:
    """
    Produce a template property dictionary for each behavior entry in a model.

    Args:
        model (Definition): A model containing behavior properties

    Returns:
        A dictionary containing a list of behaviors and a list of requirements
    """
    behaviors = []
    behavior_lists = []
    if "behavior" in model.content:
        for behavior in model.structure["model"]["behavior"]:
            behaviors.append(behavior)
    for behavior in behaviors:
        behavior_lists.append(collect_behavior_entry_properties(model.name, behavior))
    returning_list = {
        "name": model.name,
        "behaviors": [behavior for behavior_list in behavior_lists for behavior in behavior_list],
    }

    return returning_list


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


def get_template_properties(parsed_models: dict) -> list[dict]:
    """
    Generate a list of template property dictionaries for each gherkin feature file to generate.

    Args:
        parsed_models (dict): a dict of models where the key is the model name and the value is the model dict

    Returns:
        a list of template property dictionaries
    """

    return [collect_model_behavior_properties(model) for model in collect_models(parsed_models)]
