class Situation:
    """Contain Situation to store

    variables:
        self.type: str, can be 'CANCEL' or 'ALERT'
        self.msg: str, that contains the message of alert or cancel
    """

    def __init__(self, types, msg):
        self.type = types
        self.msg = msg


class Device:
    """Module of the devices

    functions:
        add_situation: adding Situation to device log
        show_id: returns device ID
        handle_cancel: receive the message of alert to be canceled and delete that from log
    """

    def __init__(self, id1):
        self._ID = int(id1)
        self.situation = []

    def add_situation(self, sit):
        """
        Add cancel or alert to device
        """
        if self.situation:
            for i in self.situation:
                if i.msg == sit.msg:
                    if i.type == 'ALERT' and sit.type == 'CANCEL':
                        self.situation.remove(i)
                        return
                    elif i.type == 'CANCEL' and sit.type == 'ALERT':
                        self.situation.remove(i)
                        return
                    else:
                        raise Exception('Duplicate Alerts with same message')
        self.situation.append(sit)

    def show_id(self):
        """
        Returns the ID of the device
        """
        return self._ID

    def handle_cancel(self, msg):
        """
        Take in the message to be canceled and delete that in the device.
        """
        flag = False
        for i in self.situation:
            if i.msg == msg:
                self.situation.remove(i)
                flag = True
        if not flag:
            print(1)
            si = Situation('CANCEL', msg)
            self.add_situation(si)


class Propagate:
    """An module that contains the propagation

    variables:
        self.type: contains if the information is cancellation or alert
        self.time: int that contains the time to receive the message
        self.from_ID: int that contains the ID of the sending device
        self.to_ID: int that contains the ID of receiving device
    """

    def __init__(self, time, types, from_id, to_id):
        self.type = types
        self.time = time
        self.from_ID = from_id
        self.to_ID = to_id
