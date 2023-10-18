import requests
from deepdiff import DeepDiff
import json

with open("event.json", "rt", encoding="utf-8") as f_in:
    event = json.load(f_in)

with open("event_response.json", "rt", encoding="utf-8") as f_in:
    expected_response = json.load(f_in)


url = "http://localhost:8080/2015-03-31/functions/function/invocations"

actual_response = requests.post(url, json=event).json()
print(actual_response)
diff = DeepDiff(actual_response, expected_response)
str_different = "diff = {}".format(diff)
print(str_different)
assert "type_changes" not in diff
