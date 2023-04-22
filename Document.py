
class Document_Object():
    """
    This class is used to store documents by title, url and abstract
    """
    def __init__(self, id, title, url, abstract) -> None:
        self.id = id
        self.title = title
        self.url = url
        self.abstract = abstract

    def __str__(self) -> str:
        return f'Doc-{self.id}:{{ Title: {self.title}\nURL: {self.url}\nAbstract: {self.abstract} }}\n'