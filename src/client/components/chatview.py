from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll, HorizontalGroup
from textual.widgets import Input, Label, Markdown, Button

chatlogs = [
    {"author": "Alex Morgan", "text": "Morning team! I pushed the first terminal UI mockup. Let me know what you think.", "timestamp": "09:41"},
    {"author": "Priya Shah", "text": "This is looking great. The keyboard-first layout feels right for a terminal app.", "timestamp": "09:43"},
    {"author": "You", "text": "Agreed — I'm keeping the sidebar compact so the conversation stays the focus.", "timestamp": "09:46"},
    {"author": "Alex Morgan", "text": "Nice. Let's add notifications and a quick way to switch channels next.", "timestamp": "10:02"}
]

class Message(HorizontalGroup):
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
        with VerticalScroll(id="messages"):
            for message in chatlogs:
                yield Message(message["author"], message["text"], message["timestamp"])
        yield HorizontalGroup(
            Input(placeholder="Message #general", id="message-input"),
            Button("Send", id="send-button"),
            classes="composer",
        )
