from pydispatch import dispatcher


class BaseProcedure(object):

    def connect(self, sender, signal, slot=None):
        # Syntactic sugar: avoids to supply self as sender.
        # connect(signal, slot)
        if slot is None:
            if isinstance(sender, MXSignal):
                slot = signal
                signal = sender
                sender = self
            else:
                raise ValueError("Invalid slot")

        signal = str(signal.name)
        dispatcher.connect(slot, signal, sender)

        # self.connect_dict[sender] = {'signal': signal, 'slot': slot}

    def disconnect(self, sender, signal, slot=None):
        # Syntactic sugar: avoids to supply self as sender.
        # connect(signal, slot)
        if slot is None:
            if isinstance(sender, MXSignal):
                slot = signal
                signal = sender
                sender = self
            else:
                raise ValueError("Invalid slot")

        signal = str(signal.name)

        dispatcher.disconnect(slot, signal, sender)

    def emit(self, signal, *args):
        # Slot expects no arguments and 0 args are passed
        if len(args) < 1 and not signal.arg_types:
            _passed = True
        # If some arguments are expected for this signal
        elif signal.arg_types:
            _passed = all([isinstance(b, a) for a,b in list(zip(signal.arg_types, args))])
        # No matching between arguments types passed and expected for signal
        else:
            _passed = False
        if not _passed:
            msg = "Argument type does not match signal signature"
            print(msg)
            #raise ValueError(msg)
        else:
            dispatcher.send(signal.name, self, *args)


class MXSignal(object):
    def __init__(self, name, arg_types=None):
        self.name = name
        if arg_types:
            self.arg_types = arg_types
        else:
            self.arg_types = None


if __name__ == "__main__":

    SIG_start_proc0 = MXSignal('startProc0')
    SIG_start_proc1 = MXSignal('startProc1', [int])
    SIG_start_proc2 = MXSignal('startProc2', [int, float])

    def start_proc_cb(*args):
        print("Starting procedure with {}".format([a for a in args]))

    def start_proc_cb2(*args):
        print("Starting procedure with {}".format([a for a in args]))

    emitter = BaseProcedure()
    receiver = BaseProcedure()

    emitter.connect(SIG_start_proc0, start_proc_cb2)
    receiver.connect(emitter, SIG_start_proc0, start_proc_cb)
    emitter.emit(SIG_start_proc0)
    emitter.emit(SIG_start_proc0, 1)  # Will fail due to invalid signature

    # receiver.connect(emitter, SIG_start_proc1, start_proc_cb)
    # emitter.emit(SIG_start_proc1, 78)
    # emitter.emit(SIG_start_proc1, 'a')  # Will fail due to invalid signature
    #
    # receiver.connect(emitter, SIG_start_proc2, start_proc_cb)
    # emitter.emit(SIG_start_proc2, 42, 82.)
    # emitter.emit(SIG_start_proc2, 42, 82)  # Will fail due to invalid signature

