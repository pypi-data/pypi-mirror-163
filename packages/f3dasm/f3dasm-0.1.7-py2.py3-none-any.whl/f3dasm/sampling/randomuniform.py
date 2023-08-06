import numpy as np

from f3dasm.src.designofexperiments import DesignSpace

from ..src.samplingmethod import SamplingMethod


class RandomUniform(SamplingMethod):
    """Sampling via random uniform sampling"""

    def sample_continuous(self, numsamples: int, doe: DesignSpace) -> np.ndarray:
        continuous = doe.get_continuous_parameters()
        dimensions = len(continuous)

        samples = np.random.uniform(size=(numsamples, dimensions))

        # stretch samples
        samples = self.stretch_samples(doe, samples)
        return samples
