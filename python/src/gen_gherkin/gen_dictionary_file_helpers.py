from re import sub

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

    if "acceptance" in behavior_entry:
        for acceptance in behavior_entry["acceptance"]:
            for scenario in acceptance["scenarios"]:
                scenario_lists.append(collect_and_sanitize_scenario_steps(scenario))
    return [
        {
            "name": (name + "_" + feature_name),
            "scenarios": [scenario for scenario_list in scenario_lists for scenario in scenario_list],
        }
    ]


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
        "acceptance": [acceptance for acceptance_list in acceptance_lists for acceptance in acceptance_list],
    }

    return returning_list

def get_template_properties(parsed_models: dict) -> list[dict]:
    """
    Generate a list of template property dictionaries for each dictionary steps file to generate.

    Args:
        parsed_models (dict): a dict of models where the key is the model name and the value is the model dict.

    Returns:
        a list of template property dictionaries
    """

    return [collect_model_acceptance_properties(model) for model in collect_models(parsed_models)]
