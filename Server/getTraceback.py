import traceback

class getTracbace:
    def get_traceback(e): #TODO: Take out to separeated moudle
        lines = traceback.format_exception(type(e), e, e.__traceback__)
        return ''.join(lines)