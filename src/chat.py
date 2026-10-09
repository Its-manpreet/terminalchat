from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, Label, Static, Rule


class Sidebar(Vertical):
    """Conversation list and account summary."""

    def compose(self) -> ComposeResult:
        yield Static("TERMINAL CHAT", classes="brand")
        yield Static("WORKSPACES", classes="section-label")
        yield Static("●  General", classes="channel active")
        yield Static("◇  Product team", classes="channel")
        yield Static("◇  Random", classes="channel")
        yield Static("DIRECT MESSAGES", classes="section-label")
        yield Static("●  Alex Morgan     2m", classes="channel")
        yield Static("●  Priya Shah      18m", classes="channel")
        yield Static("○  Jordan Lee      offline", classes="channel muted")
        yield Rule(classes="sidebar-rule")
        yield Static("⌘  You\n    online", classes="profile")


class Message(Vertical):
    """A single message in the active conversation."""

    def __init__(self, author: str, timestamp: str, text: str) -> None:
        super().__init__()
        self.author = author
        self.timestamp = timestamp
        self.text = text

    def compose(self) -> ComposeResult:
        yield Label(f"{self.author}  ", classes="message-author")
        yield Static(self.timestamp, classes="message-time")
        yield Static(self.text, classes="message-text")


class ChatView(Vertical):
    """Active conversation and message composer."""

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("# general", classes="conversation-title"),
            Static("12 members  •  team workspace", classes="conversation-subtitle"),
            classes="conversation-header",
        )
        yield VerticalScroll(
            Message("Alex Morgan", "09:41", "Morning team! I pushed the first terminal UI mockup. Let me know what you think."),
            Message("Priya Shah", "09:43", "This is looking great. The keyboard-first layout feels right for a terminal app."),
            Message("You", "09:46", "Agreed — I'm keeping the sidebar compact so the conversation stays the focus."),
            Static("────  TODAY  ────", classes="date-divider"),
            Message("Alex Morgan", "10:02", "Nice. Let's add notifications and a quick way to switch channels next."),
            id="messages",
        )
        yield Vertical(
            Input(placeholder="Message #general", id="message-input"),
            Static("Enter to send   •   Ctrl+K to search   •   D to toggle theme", classes="input-hint"),
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