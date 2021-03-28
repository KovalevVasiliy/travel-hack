# NOTE: in the future, all files at this level should be moved to separate library

from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    ok: bool = False
    error: Optional[Union[str, Dict, List]] = 'Unknown error'
    error_code: str = 'ERROR'
