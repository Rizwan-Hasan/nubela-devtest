import json
from typing import Optional


def response_for_problem_1_and_2(text: str) -> Optional[bytes]:
    """ Handling Message - Problem 1 and 2 """

    if '"message":' not in text:
        return None

    text: dict = json.loads(text)

    msg = {
        'id': text['id'],
        'result': {
            'message': text['params']['message']
        }
    }
    msg = json.dumps(msg).encode("utf-8")
    msg = msg + b'\n'
    return msg
