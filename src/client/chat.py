from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header
from src.client.components.sidebar import Sidebar
from src.client.components.chatview import ChatView, Message
import requests

class TerminalChat(App):
    """A Textual chatting app."""

    CSS_PATH = "style.tcss"
    
    TITLE = "Terminal Chat"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header(show_clock=False)
        yield Horizontal(
            Sidebar(id="sidebar"),
            ChatView(id="chat-view"),
            id="app-body",
        )
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )