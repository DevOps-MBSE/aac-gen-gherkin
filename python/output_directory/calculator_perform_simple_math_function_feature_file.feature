# ATTENTION - This generated file is safe to modify. It will not be overwritten.

@CALC-1
@CALC-2
@CALC-3
@CALC-4

Feature: Add, subtract, multiply, and divide two numbers
    
    Scenario: Add two numbers
        
        Given The calculator system is running.
        When A math request is received with a function of add and values 1 and 2.
        Then The request is logged.
        And A response is provided with a result of 3 in less than 500 ms.
        And The response is logged.
        
    Scenario: Subtract two numbers
        
        Given The calculator system is running.
        When A math request is received with a function of subtract and values 2 and 1.
        Then The request is logged.
        And A math response is provided with a result of 1 in less than 500 ms.
        And The response is logged.
        
    Scenario: Multiply two numbers
        
        Given The calculator system is running.
        When A math request is received with a function of multiply and values 2 and 2.
        Then The request is logged.
        And A math response is provided with a result of 4 in less than 500 ms.
        And The response is logged.
        
    Scenario: Divide two numbers
        
        Given The calculator system is running.
        When A math request is received with a function of divide and values 8 and 2.
        Then The request is logged.
        And A math response is provided with a result of 4 in less than 500 ms.
        And The response is logged.
        