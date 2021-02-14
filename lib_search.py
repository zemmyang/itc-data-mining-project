import json
import config as CFG


class LibrarySearch:
    def __init__(self, source: str, search_term: str):
        with open(CFG.LIBRARY_URLS, 'r') as f:
            self._data = json.load(f)

        _sources = [self.named_index(i, "source") for i in range(len(self._data))]
        self.search_term = search_term.replace(" ", "%20")

        _index = _sources.index(source)
        self.search_url = self.named_index(_index, "search_prefix") + self.search_term + self.named_index(_index, "search_suffix")

    def index(self, row: int, column: int):
        _header_labels = list(self._data[0].keys())
        return self._data[row][_header_labels[column]]

    def named_index(self, row: int, column: str):
        return self._data[row][column]

    @classmethod
    def get_search_url(cls, source: str, search_term: str):
        _obj = LibrarySearch(source, search_term)
        return _obj.search_url


def test():
    print(LibrarySearch.get_search_url("HUJI", "amos oz"))


if __name__ == "__main__":
    test()
