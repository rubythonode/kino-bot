
import arrow

from ..slack.resource import MsgResource
from ..slack.slackbot import SlackerAdapter

from ..utils.arrow import ArrowUtil
from ..utils.data_handler import DataHandler
from ..utils.state import State


class DialogManager(object):

    def __init__(self):
        self.state = State()
        self.slackbot = SlackerAdapter()
        self.data_handler = DataHandler()

    def current_state(self):
        self.state.check()
        return self.state.current

    def is_on_flow(self):
        current_state = self.current_state()
        if "step" in current_state.get(State.FLOW, {}):
            return True
        else:
            return False

    def get_flow(self, globals=None, is_raw=False):
        flow = self.current_state()[State.FLOW]
        if is_raw:
            return flow
        else:
            return self.__return_state(globals, flow, State.FLOW)

    def is_on_memory(self):
        current_state = self.current_state()
        if "step" in current_state.get(State.MEMORY, {}):
            return True
        else:
            return False

    def get_memory(self, globals=None, get_text=False):
        memory = self.current_state()[State.MEMORY]
        if get_text:
            return memory.get("text", None)
        else:
            return self.__return_state(globals, memory, State.MEMORY)

    def get_action(self):
        return self.current_state().get(State.ACTION, None)

    def __return_state(self, globals, state, kind):
        classname = state["class"]
        route_class = globals[classname]()
        behave = state["def"]
        if kind == State.FLOW:
            params = state["step"]
        elif kind == State.MEMORY:
            params = state["params"]
        return route_class, behave, params

    def is_call_repeat_skill(self, text):
        if "다시" in text:
            return True
        else:
            False

    def is_call_help(self, text):
        if ("도움말" in text) or ("help" in text):
            return True
        else:
            return False

    def is_toggl_timer(self, func_name):
        if func_name == "toggl_timer":
            return True
        else:
            return False
