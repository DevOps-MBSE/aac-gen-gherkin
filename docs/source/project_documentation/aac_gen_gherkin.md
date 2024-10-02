# AaC Gen-Gherkin

The AaC Gen-Gherkin plugin generates gherkin feature files based on provided AaC models.

## gen-gherkin-behaviors Command

```bash
aac gen-gherkin-behaviors architecture-file.aac output/directory
```

### Arguments

#### Architecture File
The AaC file containing the `model` definition/s.

#### Output Directory
The directory in which the gherkin feature files will be generated.

## Definition Type References
The `gen-gherkin` plugin will generate feature files based on the `behavior` field of `model` definitions.
`behavior` definitions also have a field named `acceptance`.  The  `acceptance` field is where the feature files scenario steps will come from.

### Example Model Definition

```yaml
model:
    name: example_name
    description: Description of Model
    behavior:
        - name: example_behavior
          description: Does something
          acceptance:
            - name: example_acceptance
              scenarios:
                - name: example scenario
                  given:
                    - Initial state
                  when:
                    - Something happens
                  then:
                    - The model does something in response.
```

## Plugin Usage Example
The calculator model system contains three model definitions: `calculator`, `mathlogger`, and `mathmessagehandler`.
`mathlogger` and `mathmessagehandler` each contain one behavior definition, while calculator contains two.
The `example_behavior` behavior in the calculator model exists only to demonstrate the gen-gherkin plugins ability to generate multiple feature files per model.

Running the following command will generate a gherkin feature file for each behavior definition in the system.
```bash
$ aac gen-gherkin-behaviors ./tests/calc/model/calculator.yaml ./output_directory
```
It will also return the following output to the command line:
```bash
All AaC constraint checks were successful.
Successfully generated feature file(s) to directory: ./output_directory
```

After running the above command, the following four feature files will be generated in `./output_directory`.  The names of the feature files are concatenations of the model name (`calculator`) and the behavior name (`example_behavior`):

`calculator_example_behavior_feature_file.feature`:
![Calculator Example Behavior](../images/calculator_example_behavior_feature_file.png)

`calculator_perform_simple_math_function_feature_file.feature`
![Calculator Perform Simple Math Function](../images/calculator_perform_simple_math_functions_feature_file.png)

`mathlogger_api_feature_file`
![Math Logger API](../images/mathlogger_api_feature_file.png)

`mathmessagehandler_api_feature_file.feature`
![Math Message Handler API](../images/mathmessagehandler_api_feature_file.PNG)
