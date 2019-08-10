

class HTMLObject(object):

    def __init__(self, name):
        assert isinstance(name, str), 'You must give a string name.'
        self.name = name

    def get_html(self, *args, **kwargs):
        NotImplementedError('You must implement the get_html function')
