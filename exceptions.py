class IllegalStateError(ValueError):
    def __init__(self, *args):
        super(IllegalStateError, self).__init__(*args)
