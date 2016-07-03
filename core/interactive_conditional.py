from raw_condition import RawCondition

class InteractiveConditional(RawConditional):
    def description(self):
        """Describe the property in question."""
        return "description"
    
    def question(self):
        """Interact with the user to find out if the property is there."""
        print "Is it true?"
        return None
