# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset


class ActionResetAllSlots(Action):
    """Reset all slots"""

    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]


class ActionSetOperation(Action):
    """Set the math operation to perform"""

    def name(self) -> Text:
        return "action_set_operation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the operation slot value
        operation = tracker.get_slot("operation")

        # Set the operation slot with the corresponding value
        return [SlotSet("operation", operation)]


class ActionMathOperation(Action):
    """Perform the math operation"""

    def name(self) -> Text:
        return "action_perform_operation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the operand1, operand2 and operation slot values
        operand1 = tracker.get_slot("operand1")
        operand2 = tracker.get_slot("operand2")
        operation = tracker.get_slot("operation")

        # Initialize the result variable
        result = None

        # Perform the corresponding operation
        if operation == "addition":
            result = operand1 + operand2
        elif operation == "subtraction":
            result = operand1 - operand2
        elif operation == "multiplication":
            result = operand1 * operand2
        elif operation == "division":
            result = operand1 / operand2

        # Set the result slot with the corresponding value
        return [SlotSet("result", result)]


class ActionDefaultFallback(Action):
    """Default fallback action"""

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Send a message to the user
        dispatcher.utter_message("I didn't understand, please try again.")

        # Reset all slots
        return [AllSlotsReset()]


class ActionValidateOperation(Action):
    """Validate the math operation"""

    def name(self) -> Text:
        return "action_validate_operation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the operation slot value
        operation = tracker.get_slot("operation")

        # Check if the operation is valid
        if operation not in ["addition", "subtraction", "multiplication", "division"]:
            # Send a message to the user
            dispatcher.utter_message("Invalid operation, please try again.")

            # Reset the operation slot
            return [SlotSet("operation", None)]

        # Set the operation slot with the corresponding value
        return [SlotSet("operation", operation)]


class ActionValidateOperand(Action):
    """Validate the math operand"""

    def name(self) -> Text:
        return "action_validate_operand"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        operand = tracker.get_slot('operand')
    
    if operand is not None and operand.isdigit():
        # Valid operand
        return [SlotSet('operand', int(operand))]
    else:
        # Invalid operand
        dispatcher.utter_message(template="utter_invalid_operand")
        return [SlotSet('operand', None)]

