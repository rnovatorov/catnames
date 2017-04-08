Feature: Greeting users


    Scenario: Non authorized user at the index page
       Given non authorized user
        When user visits Sovyak index page
        Then "Welcome to Sovyak!" is seen in "h2"


    Scenario Outline: Authorized user at the index page
       Given authorized user "<username>"
        When user visits Sovyak index page
        Then "<greeting>" is seen in "h2"

    Examples: Known users
        | username | greeting              |
        | Sovyak   | Welcome back, Sovyak! |
