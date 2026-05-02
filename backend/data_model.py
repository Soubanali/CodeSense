
from pydantic import BaseModel, Field
from typing import Literal
import json


class Feedback_Explain(BaseModel):                       #data format for json
    Explanation: str


class Feedback_Eli5(BaseModel):
    Eli5_Explanation:str



class Feedback_Debug(BaseModel):
    bugs_explanation:str



class Feedback_Optimize(BaseModel):
    Optimized_code:str




