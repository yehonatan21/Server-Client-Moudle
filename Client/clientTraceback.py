import traceback
import sys

class clientTraceback:

    def getClientTraceback(e):
        """Gives the specific loction of the exeption"""
        lines = traceback.format_exception(type(e), e, e.__traceback__)
        return ''.join(lines)

    def is_debug(self):
        """Checking if this run is debug to print the right logging"""
        gettrace = getattr(sys, 'gettrace', None)

        if gettrace is None:
            return False
        else:
            v = gettrace()
            if v is None:
                return False
            else:
                return True
