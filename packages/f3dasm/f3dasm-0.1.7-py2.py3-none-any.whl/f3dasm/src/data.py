from dataclasses import dataclass, field
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt

from f3dasm.src.designofexperiments import DesignSpace


@dataclass
class Data:
    """Class that contains data

    Args:
        data (DataFrame): data stored in a DataFrame
    """

    # data: pd.DataFrame
    doe: DesignSpace
    data: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.data = self.doe.get_empty_dataframe()

    def show(self) -> None:
        print(self.data)
        return

    def add(self, data: pd.DataFrame) -> None:
        """Add data

        Args:
            data (pd.DataFrame): data to append
        """
        self.data = pd.concat([self.data, data])

    def add_output(self, output: np.ndarray, label: str) -> None:
        self.data[("output", label)] = output

    def get_input_data(self) -> pd.DataFrame:
        return self.data["input"]

    def get_output_data(self) -> pd.DataFrame:
        return self.data["output"]

    def plot(
        self, input_par1: str, input_par2: str = None, output_par: str = None
    ) -> None:
        """Plot the data of two parameters in a figure

        Args:
            input_par1 (str): name of first parameter (x-axis)
            input_par2 (str): name of second parameter (x-axis)
            output_par (str): name of output parameter (y-axis)
        """
        fig, ax = plt.figure(), plt.axes()

        ax.scatter(
            self.data[("input", input_par1)], self.data[("input", input_par2)], s=3
        )

        ax.set_xlabel(input_par1)
        ax.set_ylabel(input_par2)

        fig.show()

    def plot_pairs(self):
        import seaborn as sb

        sb.pairplot(data=self.get_input_data())
