class Element():
    def __init__(self, ctype):
        self.ctype = ctype
        self.in_name = 'is_in_allowed'
        self.out_name = 'is_out_allowed'

    def init(self):
        if self.ctype == 'in_out':
            setattr(self, self.in_name, self._allowed_act0)
            setattr(self, self.out_name, self._allowed_act1)

    def _allowed_act0(self):
        print 'act0'

    def _allowed_act1(self):
        print 'act1'

A = Element('in_out')

A.is_in_allowed()
A.is_out_allowed()

class Specific(Element):
    def __init__(self, *args):
        super(Specific, self).__init(*args)

    def _allowed_act0(self):
        print 'REact0'

    def _allowed_act1(self):
        print 'REact1'


