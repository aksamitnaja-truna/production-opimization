import json
from dataclasses import dataclass
from pydantic import BaseModel


class TableShema(BaseModel):
    table: list[list[str]]
    trend: dict[str, str]

class TableShemaModel(BaseModel): ...
class TrendShemaModel(BaseModel): ...

# if __name__ == "__main__":
#     with open("../data/data.json", 'r') as json_file:
#         json_data = json.load(json_file)
#         data = TableShema(**json_data)
#     print(data)