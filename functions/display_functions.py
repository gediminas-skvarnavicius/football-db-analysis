from IPython.display import Markdown, display
from typing import Optional
import matplotlib.pyplot as plt


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
