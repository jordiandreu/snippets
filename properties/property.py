class EnvVar(object):
    def __init__(self, key):
        print "init"
        self._key = key

    @property
    def value(self):
        """
        Function that returns the current value from the environment
        MacroServer attribute for a given key.
        :param key: Environment dictionary key requested.
        """
        print "getter"
        self._value = "/tmp/"
        return self._value

    @value.setter
    def value(self, v):
        """
        Function that sets the environment with the new value for a given key.
        A dictionary is constructed with the new key-value pairs and passed
        to the environment MacroServer attribute.
        :param key: Environment dictionary key.
        :param value: Environment dictionary value.
        """
        print "setter"
        self._value = v
