from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll, HorizontalGroup
from textual.reactive import reactive
from textual.widgets import Input, Label, Markdown, Button

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

class MessageComposer(HorizontalGroup):
    """A message composer for the active conversation."""

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Message #general", id="message-input")
        yield Button("Send", id="send-button")

class ChatView(Vertical):
    """Active conversation and message composer."""

    chatlogs = reactive([
        {"author": "Alex Morgan", "text": "Morning team! I pushed the first terminal UI mockup. Let me know what you think.", "timestamp": "09:41"},
        {"author": "Priya Shah", "text": "This is looking great. The keyboard-first layout feels right for a terminal app.", "timestamp": "09:43"},
        {"author": "You", "text": "Agreed — I'm keeping the sidebar compact so the conversation stays the focus.", "timestamp": "09:46"},
        {"author": "Alex Morgan", "text": "Nice. Let's add notifications and a quick way to switch channels next.", "timestamp": "10:02"}
    ])
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the send button being pressed."""
        if event.button.id == "send-button":
            input_widget = self.query_one("#message-input", Input)
            message_text = input_widget.value.strip()
            if message_text:
                # Add the new message to the chatlogs
                self.chatlogs = [
                    *self.chatlogs,
                    {"author": "You", "text": message_text, "timestamp": "now"},
                ]
                # Clear the input field
                input_widget.value = ""
                
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle the enter key being pressed in the input field."""
        if event.input.id == "message-input":
            message_text = event.value.strip()
            if message_text:
                # Add the new message to the chatlogs
                self.chatlogs = [
                    *self.chatlogs,
                    {"author": "You", "text": message_text, "timestamp": "now"},
                ]
                # Clear the input field
                event.input.value = ""

    async def watch_chatlogs(self, chatlogs: list[dict[str, str]]) -> None:
        """Rebuild the messages whenever the chat log changes."""
        messages = self.query_one("#messages", VerticalScroll)
        await messages.remove_children()
        await messages.mount(*(
            Message(message["author"], message["text"], message["timestamp"])
            for message in chatlogs
        ))

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("# general", classes="conversation-title"),
            Label("12 members  •  team workspace", classes="conversation-subtitle"),
            classes="conversation-header",
        )
        with VerticalScroll(id="messages"):
            for message in self.chatlogs:
                yield Message(message["author"], message["text"], message["timestamp"])
        yield MessageComposer(
            classes="composer",
        )
        
