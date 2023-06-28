from IPython.display import Markdown, display


def sized_markdown(text: str, font_size: int = 14):
    display(Markdown(f"<span style='font-size:{font_size}px;'>" + text))
