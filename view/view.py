from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings


tickers_grouped = [
    ["AAPL", "MSFT", "ASML.AS", "NVDA", "TSLA"],
    ["JPM", "XOM", "UNH", "PG", "KO"],
    ["V", "MA", "META", "GOOGL", "AMZN"],
    ["SHEL.AS", "ADYEN.AS", "SAP.DE", "NESN.SW", "NOVO-B.CO"],
    ["AGG", "BND", "VOO", "SPY", "QQQ"],
    ["BTC-USD", "ETH-USD", "GLD", "SLV", "CASH"],
]

tickers = [t for row in tickers_grouped for t in row]

CELL_WIDTH = 12  # " TICKER     " — 10 chars padded + 2 spaces

selected_index = 0
last_ncols = 1  # refreshed on every render; used by arrow keys


def compute_ncols():
    term_cols = get_app().output.get_size().columns
    # subtract a few chars for the Frame border + padding
    usable = max(CELL_WIDTH, term_cols - 4)
    return max(1, usable // CELL_WIDTH)


def get_grid_text():
    global last_ncols
    last_ncols = compute_ncols()

    result = []
    for i, ticker in enumerate(tickers):
        style = "reverse" if i == selected_index else ""
        result.append((style, f" {ticker:<10} "))
        if (i + 1) % last_ncols == 0 and i != len(tickers) - 1:
            result.append(("", "\n"))
    return result


ticker_input = TextArea(
    height=1,
    prompt="Type ticker: ",
    multiline=False,
)

status = TextArea(
    height=1,
    text="Arrow keys to move. Enter to select. Ctrl+C to cancel.",
    multiline=False,
    focusable=False,
)


grid_control = FormattedTextControl(get_grid_text)
grid_window = Window(content=grid_control, wrap_lines=False)


kb = KeyBindings()


def _reset_input():
    ticker_input.text = ""
    status.text = "Arrow keys to move. Enter to select. Ctrl+C to cancel."


@kb.add("up")
def move_up(event):
    global selected_index
    new = selected_index - last_ncols
    if new >= 0:
        selected_index = new
    _reset_input()


@kb.add("down")
def move_down(event):
    global selected_index
    new = selected_index + last_ncols
    if new < len(tickers):
        selected_index = new
    _reset_input()


@kb.add("left")
def move_left(event):
    global selected_index
    selected_index = max(0, selected_index - 1)
    _reset_input()


@kb.add("right")
def move_right(event):
    global selected_index
    selected_index = min(len(tickers) - 1, selected_index + 1)
    _reset_input()


@kb.add("enter")
def select_ticker(event):
    typed = ticker_input.text.strip().upper()
    if not typed:
        event.app.exit(result=tickers[selected_index])
    elif typed in tickers:
        event.app.exit(result=typed)
    else:
        status.text = f"'{typed}' is not in the ticker list."


@kb.add("c-c")
def quit_app_c(event):
    event.app.exit(result=None)


layout = Layout(
    HSplit(
        [
            Frame(ticker_input, title="Manual ticker input"),
            Frame(grid_window, title="Ticker grid"),
            status,
        ]
    )
)

app = Application(
    layout=layout,
    key_bindings=kb,
    full_screen=True,
    mouse_support=True,
)

result = app.run()

print(f"You selected: {result}")
