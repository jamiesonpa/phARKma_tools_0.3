import datetime
from datetime import datetime


def removeDigits(s):
    answer = []
    for char in s:
        if not char.isdigit():
            answer.append(char)
    return ''.join(answer)


def timestamp():
    dateTimeObj = datetime.now()
    timestampStr = "[" + (dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")) + "]: "
    return timestampStr
