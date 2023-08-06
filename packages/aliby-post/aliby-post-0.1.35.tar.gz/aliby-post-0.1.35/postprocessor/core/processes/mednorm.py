#!/usr/bin/env python3


import pandas as pd

from agora.abc import ParametersABC
from postprocessor.core.abc import PostProcessABC


class mednormParameters(ParametersABC):
    """:window: Number of timepoints to consider for signal."""

    _defaults = {"window": 3}


class mednorm(PostProcessABC):
    """Normalise a channel by the median."""

    def __init__(self, parameters: mednormParameters):
        super().__init__(parameters)

    def run(self, signal: pd.DataFrame):
        return (
            signal.rolling(window=self.parameters.window, axis=1)
            .mean()
            .diff(axis=1)
        )
