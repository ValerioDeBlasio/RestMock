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
    path_params: Optional[Dict[str, str]]
    query_params: Optional[Dict[str, Union[str, List[str]]]]
    body: Optional[Dict]
    response: Dict
    response_code: Optional[int]
