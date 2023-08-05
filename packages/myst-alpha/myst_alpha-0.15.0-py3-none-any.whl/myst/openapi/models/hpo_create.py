from typing import Dict, Optional, Union

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.absolute_timing_create import AbsoluteTimingCreate
from myst.openapi.models.choice import Choice
from myst.openapi.models.constant import Constant
from myst.openapi.models.cron_timing_create import CronTimingCreate
from myst.openapi.models.hyperopt_create import HyperoptCreate
from myst.openapi.models.log_uniform import LogUniform
from myst.openapi.models.q_log_uniform import QLogUniform
from myst.openapi.models.q_uniform import QUniform
from myst.openapi.models.relative_timing_create import RelativeTimingCreate
from myst.openapi.models.uniform import Uniform


class HPOCreate(base_model.BaseModel):
    """HPO schema for create input."""

    object_: Literal["HPO"] = Field(..., alias="object")
    title: str
    model: str
    search_algorithm: HyperoptCreate
    fit_start_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    fit_end_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    predict_start_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    predict_end_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    description: Optional[str] = None
    search_space: Optional[
        Dict[str, Optional[Union[Uniform, QUniform, LogUniform, QLogUniform, Choice, Constant]]]
    ] = None
    test_start_time: Optional[str] = None
    test_end_time: Optional[str] = None
    fit_reference_timing: Optional[Union[AbsoluteTimingCreate, CronTimingCreate]] = None
    predict_reference_timing: Optional[CronTimingCreate] = None
