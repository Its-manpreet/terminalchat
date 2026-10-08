from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Footer, Header, Static, Input

class MainBody(VerticalGroup):
    """The main body of the app."""
    def compose(self) -> ComposeResult:
        yield Static("Hello from body!")
        yield ChatInput()
        
class ChatInput(HorizontalGroup):
    """A text input widget for chat messages."""
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type a message and hit enter...")

class TerminalChat(App):
    """A Textual chatting app."""

    CSS_PATH = "style.tcss"
    
    TITLE = "Terminal Chat"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header(show_clock=True)
        yield MainBody()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = TerminalChat()
    app.run()