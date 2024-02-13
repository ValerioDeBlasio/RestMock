# ------- #
# Created by: valeriodeblasio with ❤
# Date: Tue 08/11/2022
# Time: 11:27
# ------- #
from typing import List, Union, Dict, Optional

from pydantic import BaseModel


class ApiMockModel(BaseModel):
    method: str
    endpoint: str
    path_params: Dict[str, str] | None = {}
    query_params: Dict[str, Union[str, List[str]]] | None = {}
    body: Dict | None = {}
    response: Dict
    response_code: int | None = 200
