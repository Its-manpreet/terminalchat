from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, Label, Rule, Collapsible, Markdown


class Sidebar(Vertical):
    """A sidebar with conversation list and account summary."""

    def compose(self) -> ComposeResult:
        with Collapsible(title="Workspaces", collapsed=False, classes="section-label"):
            yield Label("●  General", classes="channel active")
            yield Label("◇  Product team", classes="channel")
            yield Label("◇  Random", classes="channel")
        with Collapsible(title="Direct Messages", collapsed=False, classes="section-label"):
            yield Label("●  Alex Morgan     2m", classes="channel")
            yield Label("●  Priya Shah      18m", classes="channel")
            yield Label("○  Jordan Lee      offline", classes="channel muted")
        yield Rule(classes="sidebar-rule")
        yield Label("⌘  You\n    online", classes="profile")


class Message(Vertical):
    """A single message in the active conversation."""

    def __init__(self, author: str, text: str, timestamp: str) -> None:
        super().__init__()
        self.author = author
        self.timestamp = timestamp
        self.text = text

    def compose(self) -> ComposeResult:
        yield Label(f"{self.author}  ", classes="message-author")
        yield Markdown(self.text, classes="message-text")
        yield Label(self.timestamp, classes="message-time")

class ChatView(Vertical):
    """Active conversation and message composer."""

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("# general", classes="conversation-title"),
            Label("12 members  •  team workspace", classes="conversation-subtitle"),
            classes="conversation-header",
        )
        yield VerticalScroll(
            Message("Alex Morgan", "Morning team! I pushed the first terminal UI mockup. Let me know what you think.", "09:41"),
            Message("Priya Shah", "This is looking great. The keyboard-first layout feels right for a terminal app.", "09:43"),
            Message("You", "Agreed — I'm keeping the sidebar compact so the conversation stays the focus.", "09:46"),
            Label("────  TODAY  ────", classes="date-divider"),
            Message("Alex Morgan", "Nice. Let's add notifications and a quick way to switch channels next.", "10:02"),
            id="messages",
        )
        yield Vertical(
            Input(placeholder="Message #general", id="message-input"),
            Label("Enter to send   •   Ctrl+K to search   •   D to toggle theme", classes="input-hint"),
            classes="composer",
        )

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