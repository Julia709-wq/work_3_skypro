import json
from src.views import generate_json_response
from src.utils import read_data_from_file


data = read_data_from_file()

date_str = "2019-02-19 17:00:00"

json_response = json.dumps(generate_json_response(date_str, data), indent=4, ensure_ascii=False)

# print(json_response)
