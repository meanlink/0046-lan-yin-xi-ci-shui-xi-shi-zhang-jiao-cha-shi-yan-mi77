from pydantic import BaseModel, Field
class Strip(BaseModel):
    code: str=Field(pattern=r"^[A-Z0-9-]{2,20}$")
    short_temp: float=Field(ge=4,le=70)
    long_temp: float=Field(ge=4,le=70)
    short_density: float=Field(ge=0,le=2)
    long_density: float=Field(ge=0,le=2)
    long_fade: float=Field(ge=0,le=1)
