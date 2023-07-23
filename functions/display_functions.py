from IPython.display import Markdown, display
from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def sized_markdown(text: str, font_size: int = 14):
    display(Markdown(f"<span style='font-size:{font_size}px;'>" + text))


def axis_titles(
    ax: plt.Axes,
    xtitle: Optional[str] = None,
    ytitle: Optional[str] = None,
    title: Optional[str] = None,
):
    """
    Sets the labels of the x and y axes, as well as the title of a graph.

    Parameters:
        ax (plt.Axes): The matplotlib Axes object representing the graph.
        xtitle (Optional[str]): The label for the x-axis. Defaults to None.
        ytitle (Optional[str]): The label for the y-axis. Defaults to None.
        title (Optional[str]): The title of the graph. Defaults to None.

    Returns:
        None

    This function sets the labels of the x and y axes, as well as the title of a graph
    represented by the provided Axes object. It allows you to specify custom labels for
    the x and y axes, as well as a title for the graph. If any of the parameters are not
    provided (i.e., set to None), the corresponding axis or title will not be modified.

    Example usage:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        axis_titles(ax, xtitle='Time (s)', ytitle='Value', title='My Graph')
        plt.show()
    """
    ax.set_ylabel(ytitle)
    ax.set_xlabel(xtitle)
    ax.set_title(title)


def get_correlation_pairs(
    data: pd.DataFrame,
    positive_cut_off: Optional[float] = 0,
    negative_cut_off: Optional[float] = 0,
    leave_center: bool = False,
) -> pd.DataFrame:
    """
    Produces a data frame that contains pairs of features
    and their r-values based on selected cut-offs
    """
    if positive_cut_off is not None and not 0 <= positive_cut_off <= 1:
        raise ValueError("Positive cut-offs must be between 0 and 1")

    if negative_cut_off is not None and not -1 <= negative_cut_off <= 0:
        raise ValueError("Negative cut-offs must be between -1 and 0")

    corr_matrix = data.corr(numeric_only=True)

    if not leave_center:
        np.fill_diagonal(corr_matrix.values, None)

        cut_correlation_matrix = corr_matrix.mask(
            (corr_matrix >= negative_cut_off) & (corr_matrix <= positive_cut_off)
        )

    else:
        # Masking extreme negative values
        cut_correlation_matrix = corr_matrix.mask(corr_matrix <= negative_cut_off)

        # Masking extreme positive values
        cut_correlation_matrix = cut_correlation_matrix.mask(
            corr_matrix >= positive_cut_off
        )

    # stacking the remaining values
    cut_correlation_matrix = cut_correlation_matrix.stack().reset_index()

    # combining levels after stacking into a single pair frozenset
    cut_correlation_matrix["feature_pair"] = cut_correlation_matrix[
        ["level_0", "level_1"]
    ].apply(frozenset, axis=1)

    # dropping previous level columns
    cut_correlation_matrix = cut_correlation_matrix.drop(columns=["level_0", "level_1"])

    # removing duplicate pairs
    cut_correlation_matrix = cut_correlation_matrix.drop_duplicates(
        subset="feature_pair"
    )

    cut_correlation_matrix = cut_correlation_matrix.rename(columns={0: "r-value"})
    return cut_correlation_matrix


def rb_cell_highlight(value: float, threshold: float, higher: bool = True) -> str:
    """Sets the cell background color of a pandas DataFrame,
    based on whether the cell's float value is greater than the threshold.
    """
    color = ""
    if higher:
        if value > threshold:
            color = "background-color: rgba(0, 0, 255, 0.25)"
        else:
            color = "background-color: rgba(255, 0, 0, 0.25)"
    else:
        if value < threshold:
            color = "background-color: rgba(0, 0, 255, 0.25)"
        else:
            color = "background-color: rgba(255, 0, 0, 0.25)"
    return color
