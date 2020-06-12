class MessageTracker(object):
    """ Attempt to create a logic that tracks messages and delete useless ones """
    startup_messages = list()
    time_change_msg = 0

    def __init__(self, *args):
        all_messages = list()
