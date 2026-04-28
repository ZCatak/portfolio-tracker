from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings


_TICKERS_GROUPED = [
    ["AAPL", "MSFT", "ASML.AS", "NVDA", "TSLA"],
    ["JPM", "XOM", "UNH", "PG", "KO"],
    ["V", "MA", "META", "GOOGL", "AMZN"],
    ["SHEL.AS", "ADYEN.AS", "SAP.DE", "NESN.SW", "NOVO-B.CO"],
    ["AGG", "BND", "VOO", "SPY", "QQQ"],
    ["BTC-USD", "ETH-USD", "GLD", "SLV", "CASH"],
]
TICKERS = [t for row in _TICKERS_GROUPED for t in row]

ASSET_CLASSES = ["Equity", "Crypto", "Fixed Income", "Cash", "Commodity", "ETF"]

SECTORS_BY_CLASS = {
    "Equity": [
        "Technology", "Healthcare", "Financials", "Consumer Discretionary",
        "Consumer Staples", "Energy", "Industrials", "Materials",
        "Utilities", "Real Estate", "Communication Services",
    ],
    "Crypto": [
        "DeFi", "NFT", "Layer 1", "Layer 2", "Stablecoin",
        "Meme", "Privacy", "Gaming/Metaverse", "Infrastructure",
    ],
    "Fixed Income": [
        "Government", "Corporate IG", "Corporate HY",
        "Municipal", "Emerging Market", "Inflation-Linked", "Mortgage-Backed",
    ],
    "Cash": ["Cash", "Money Market"],
    "Commodity": [
        "Precious Metals", "Energy", "Agriculture",
        "Industrial Metals", "Livestock",
    ],
    "ETF": ["Equity ETF", "Bond ETF", "Sector ETF", "International", "Thematic"],
}

STATUS_HINT = "Arrow keys to move. Enter to select. Ctrl+C to cancel."


def pick_from_list(
    items: list[str],
    title: str,
    input_label: str,
    transform=None,
) -> str | None:
    selected = 0
    ncols = 1
    cell_width = max(len(s) for s in items) + 2

    text_input = TextArea(height=1, prompt=input_label, multiline=False)
    status = TextArea(height=1, text=STATUS_HINT, multiline=False, focusable=False)

    def reset_input():
        text_input.text = ""
        status.text = STATUS_HINT

    def compute_ncols():
        term_cols = get_app().output.get_size().columns
        usable = max(cell_width, term_cols - 4)
        return max(1, usable // cell_width)

    def get_grid_text():
        nonlocal ncols
        ncols = compute_ncols()
        result = []
        for i, item in enumerate(items):
            style = "reverse" if i == selected else ""
            result.append((style, f" {item:<{cell_width - 2}} "))
            if (i + 1) % ncols == 0 and i != len(items) - 1:
                result.append(("", "\n"))
        return result

    kb = KeyBindings()

    @kb.add("up")
    def move_up(event):
        nonlocal selected
        new = selected - ncols
        if new >= 0:
            selected = new
        reset_input()

    @kb.add("down")
    def move_down(event):
        nonlocal selected
        new = selected + ncols
        if new < len(items):
            selected = new
        reset_input()

    @kb.add("left")
    def move_left(event):
        nonlocal selected
        selected = max(0, selected - 1)
        reset_input()

    @kb.add("right")
    def move_right(event):
        nonlocal selected
        selected = min(len(items) - 1, selected + 1)
        reset_input()

    @kb.add("enter")
    def select(event):
        typed = text_input.text.strip()
        if typed:
            event.app.exit(result=transform(typed) if transform else typed)
        else:
            event.app.exit(result=items[selected])

    @kb.add("c-c")
    def cancel(event):
        event.app.exit(result=None)

    layout = Layout(
        HSplit(
            [
                Frame(text_input, title=f"Manual {title.lower()} input"),
                Frame(
                    Window(content=FormattedTextControl(get_grid_text), wrap_lines=False),
                    title=title,
                ),
                status,
            ]
        )
    )

    return Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True,
        mouse_support=True,
    ).run()


def pick_ticker() -> str | None:
    return pick_from_list(
        TICKERS,
        title="Ticker grid",
        input_label="Type ticker: ",
        transform=str.upper,
    )


def pick_asset_class() -> str | None:
    return pick_from_list(
        ASSET_CLASSES,
        title="Asset class",
        input_label="Type asset class: ",
        transform=str.title,
    )


def pick_sector(asset_class: str) -> str | None:
    sectors = SECTORS_BY_CLASS.get(asset_class, ["Other"])
    return pick_from_list(
        sectors,
        title=f"Sector ({asset_class})",
        input_label="Type sector: ",
        transform=str.title,
    )
