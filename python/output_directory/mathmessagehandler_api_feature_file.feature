# ATTENTION - This generated file is safe to modify. It will not be overwritten.

@ADD-1
@SUB-1
@MULT-1
@DIV-1
@POW-1
@SQRT-1

Feature: TODO: Fill out this feature description.
    
    Scenario: Request handler responds with a calculated value
        
        Given The MathMessageHandler is running
        When The user makes a request with MathRequest
        Then The MathRequest function is executed against the values and a result is calculated
        And The user gets a MathResponse response with the calculated value
        
    @SQRT-2
    Scenario: Request handler issues error for square root command with negative value
        
        Given The MathMessageHandler is running
        When The user makes a square root request with MathRequest
        Then The user gets a MathResponse response with the error
        