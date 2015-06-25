from raw_condition import RawCondition

class InteractiveCondition(RawCondition):
    def question(self):
        return "Is it true?"
