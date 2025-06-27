from pydantic import BaseModel
from typing import List, Optional

class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: int
    aud: List[str]
    azp: str
    scope: Optional[str]
    # Ajoute les champs dont tu as besoin
