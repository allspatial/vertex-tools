__author__ = 'michael'


class VertexToolsError(Exception):

    def __init__(self, title, message):

        self.__title = title
        self.__message = message

    def message(self):

        return self.__message

    def title(self):

        return self.__title
