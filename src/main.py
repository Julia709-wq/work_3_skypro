import os
import pandas as pd
import json
from src.views import generate_json_response


current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, '..', 'data')

file_excel_path = os.path.join(data_dir, 'operations.xlsx')
file_excel_path = os.path.normpath(file_excel_path)

data = pd.read_excel(file_excel_path)
result_dict = data.to_dict('records')


date_str = "2019-02-19 00:00:00"

json_response = generate_json_response(date_str, result_dict)

print(json.dumps(json_response, indent=4, ensure_ascii=False))
