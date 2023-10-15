from lethal import System, SideEffect


class MsgSideEffect(SideEffect):
    """Send a log msg to the ui"""

    text: str


class DungeonSystem(System):
    """Extended ECS system adds helpers for our particular game setup"""

    def _message(self, text) -> SideEffect:
        return self.add_side_effect(MsgSideEffect(text=text))
