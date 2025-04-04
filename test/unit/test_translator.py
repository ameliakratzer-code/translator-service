from src import translator
from src.translator import query_llm_robust
from unittest.mock import patch

@patch.object(translator.client.chat.completions, 'create')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.choices[0].message.content = "I don't understand your request"

  # TODO assert the expected behavior
  assert (False, "__LLM_ERROR__: Hier ist dein erstes Beispiel.") == query_llm_robust("Hier ist dein erstes Beispiel.")

# Case 2: LLM returns an empty string
@patch.object(translator.client.chat.completions, 'create')
def test_llm_returns_empty_string(mocker):
    mocker.return_value.choices[0].message.content = ""
    assert (False, "__LLM_ERROR__: Manger ensemble est toujours un bon moment.") == query_llm_robust("Manger ensemble est toujours un bon moment.")

# Case 3: LLM returns a string containing an array literal
@patch.object(translator.client.chat.completions, 'create')
def test_llm_returns_array_literal(mocker):
    mocker.return_value.choices[0].message.content = "[False, 'Here is your first example.']"
    assert (False, "__LLM_ERROR__: Привет! Как дела? Сегодня отличный день для прогулки в парке.") == query_llm_robust("Привет! Как дела? Сегодня отличный день для прогулки в парке.")

# Case 4: LLM returns a string containing a tuple literal but the values are not of boolean and string type
@patch.object(translator.client.chat.completions, 'create')
def test_llm_returns_non_boolean_and_string_tuple(mocker):
  mocker.return_value.choices[0].message.content = "(50, 20)"
  assert (False, "__LLM_ERROR__: hdsakjhd123123kjasd ??? !!!") == query_llm_robust("hdsakjhd123123kjasd ??? !!!")

# Case 5: LLM returns a string containing a tuple literal but it is too long
@patch.object(translator.client.chat.completions, 'create')
def test_llm_returns_long_tuple(mocker):
  mocker.return_value.choices[0].message.content = "(False, 20, 'aiwueh aiwejfo ajsdfojas?')"
  assert (False, "__LLM_ERROR__: aiwueh aiwejfo ajsdfojas?") == query_llm_robust("aiwueh aiwejfo ajsdfojas?")