import traceback
import sys

class clientTraceback:

    def getClientTraceback(e): #TODO: Take out to separeated moudle
        lines = traceback.format_exception(type(e), e, e.__traceback__)
        return ''.join(lines)

    def is_debug(self):
        gettrace = getattr(sys, 'gettrace', None)

        if gettrace is None:
            return False
        else:
            v = gettrace()
            if v is None:
                return False
            else:
                return True
