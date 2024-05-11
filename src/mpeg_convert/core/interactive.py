from typing import Any, Dict

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Button, Input, Static, Label, Switch
from textual.widgets import TabbedContent, TabPane


class FileTab(Static):

    def compose(self) -> ComposeResult:
        yield Static('[bold] • Media')
        with Horizontal():
            with Vertical():
                yield Static('[grey70]Input the input file path below, or select a file from the menu', id='FileInputLabel')
                yield Input(placeholder='Path to the input file', id='FileInput')
            with Vertical():
                yield Static('[grey70]Input the output file path below, or select a file from the menu', id='FileOutputLabel')
                yield Input(placeholder='Path to the output file', id='FileOutput')
        yield Static('[bold] • Options')


class VideoTab(Static):

    def compose(self) -> ComposeResult:
        yield Label()


class AudioTab(Static):

    def compose(self) -> ComposeResult:
        yield Label()


class FilterTab(Static):

    def compose(self) -> ComposeResult:
        yield Label()


class PresetTab(Static):

    def compose(self) -> ComposeResult:
        yield Label()


class InteractiveApp(App):

    CSS_PATH = 'css/program.tcss'

    def compose(self) -> ComposeResult:
        with TabbedContent('File', 'Video', 'Audio', 'Filter', 'Preset', id='MainView'):
            yield ScrollableContainer(TabPane('File', FileTab(), id='FileTab'))
            yield ScrollableContainer(TabPane('Video', VideoTab(), id='VideoTab'))
            yield ScrollableContainer(TabPane('Audio', AudioTab(), id='AudioTab'))
            yield ScrollableContainer(TabPane('Filter', FilterTab(), id='FilterTab'))
            yield ScrollableContainer(TabPane('Preset', PresetTab(), id='PresetTab'))
        yield Horizontal(
            Static(),
            Button('Settings', variant='default', id='SettingsFooter'),
            Button('Convert', variant='success', id='ConvertFooter'),
            id='MainFooter'
        )


def run_module(argv: Dict[Any, Any]) -> int:
    instance = InteractiveApp()
    instance.run()
    return 0
