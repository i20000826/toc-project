from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    """
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model = self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "go to menu"

    def on_enter_menu(self, event):
        print("I'm entering menu")

        send_text_message(event.reply_token, "menu")
        # self.go_back()

    def is_going_to_forbidden_forest(self, event):
        text = event.message.text
        return text.lower() == "go to forbidden_forest"

    def on_enter_forbidden_forest(self, event):
        print("I'm entering forbidden_forest")

        send_text_message(event.reply_token, "forbidden_forest")
        # self.go_back()
    """

    """
    def on_exit_state1(self):
        print("Leaving menu")

    def on_exit_forbidden_forest(self):
        print("Leaving forbidden_forest")
    """
