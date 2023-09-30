class Item:
    def __init__(
        self, identifier, tags=[], content={}
    ):  # use to refer to its tracker data
        self.identifier = identifier
        self.tags = set(tags)
        self.content = content

    def has_tag(self, tag):
        return tag in self.tags

    def to_dictionary(self):
        return {
            "identifier": self.identifier,
            "tags": list(self.tags),
            "content": content,
        }

    @staticmethod
    def load_from_dictionary(data_dict):
        item = Item("dummy_identifier")
        item.identifier = data_dict["identifier"]
        item.tags = set(data_dict["tags"])
        item.content = data_dict["content"]
        return item
