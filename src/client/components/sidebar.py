from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, Collapsible, RadioSet, RadioButton, Rule


class Sidebar(Vertical):
    """A sidebar with conversation list and account summary."""

    def compose(self) -> ComposeResult:
        yield Label("Terminal Chat", classes="app-title")
        with Collapsible(title="Workspaces", collapsed=False, classes="section-label"):
            with RadioSet(classes="workspace-list"):
                yield RadioButton("General", classes="channel", value=True)
                yield RadioButton("Product team", classes="channel")
                yield RadioButton("Random", classes="channel")
        with Collapsible(title="Direct Messages", collapsed=False, classes="section-label"):
            with RadioSet():
                yield RadioButton("Alex Morgan  2m", classes="channel")
                yield RadioButton("Priya Shah   18m", classes="channel")
                yield RadioButton("Jordan Lee   offline", classes="channel")
        yield Rule(classes="sidebar-rule")
        yield Label("⌘  You\n    online", classes="profile")