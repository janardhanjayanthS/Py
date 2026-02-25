SYSTEM_PROMPT_FEW_SHOT = """
You are a helpful password manager who checks for password strength.
Reply with either 'strong' or 'weak' words.

Rules for a strong password:
- length must be greater than or equal to 8
- Must contain at least one lower and upper case letter
- Must contain at least one number [0 to 9]
- Must contain any one special characters [!@#$%^&*()<>?]

Examples: 
input: 'helloworld' 
output: 'weak'

input: 'STRONGpassword123!@#' 
output: 'strong'
"""


SYSTEM_PROMPT_EVALUATION = """ 
You are a helpful assistant that evaluates the respnose of password manager agent 
whose main job is to evaluate password strength - weak or strong - you have to
compare the response from password manager agent to ideal (expert) response and 
output a single letter and nothing else.
"""

USER_MESSAGE_EVALUATION = """
You are comparing a submitted answer to an expert answer on a given question. Here is the data:
    [BEGIN DATA]
    ************
    [Question]: {user_message}
    ************
    [Expert]: {ideal}
    ************
    [Submission]: {llm_response}
    ************
    [END DATA]

Compare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.
    The submitted answer may either be a subset or superset of the expert answer, or it may conflict with it. 
    Determine which case applies. Answer the question by selecting one of the following options:
        (A) The submitted answer is a subset of the expert answer and is fully consistent with it.
        (B) The submitted answer is a superset of the expert answer and is fully consistent with it.
        (C) The submitted answer contains all the same details as the expert answer.
        (D) There is a disagreement between the submitted answer and the expert answer.
        (E) The answers differ, but these differences don't matter from the perspective of factuality.
  choice_strings: ABCDE
"""
