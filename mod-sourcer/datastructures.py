from typing import Dict, List, Set


class TagSource:
    """
    Describes a potential source for tags, which is almost always a Mod or Vanilla Minecraft.
    """
    mod_id: str
    mod_name: str
    mod_version: str
    mod_url: str

    def __init__(self, mod_id, mod_name, mod_version, mod_url):
        self.mod_id = mod_id
        self.mod_name = mod_name
        self.mod_version = mod_version
        self.mod_url = mod_url

    def to_json(self):
        return {
            'id': self.mod_id,
            'name': self.mod_name,
            'version': self.mod_version,
            'url': self.mod_url
        }

    @classmethod
    def from_json(cls, json):
        return TagSource(json['id'], json['name'], json['version'], json['url'])


class TagEntry:
    value: str
    sources: Set[TagSource]

    def __init__(self, value: str, sources: Set[TagSource]) -> None:
        super().__init__()
        self.value = value
        self.sources = sources

    def add_source(self, source: TagSource):
        self.sources.add(source)

    def to_json(self):
        return {
            'value': self.value,
            'sources': [s.mod_id for s in self.sources]
        }

    @classmethod
    def from_json(cls, json, sources):
        resolved_sources = {sources[x] for x in json['sources']}
        return TagEntry(json['value'], resolved_sources)


class Tag:
    id: str
    # Tag sources that will replace this tag fully
    replaced_by: Set[TagSource]
    content: List[TagEntry]
    sources: Set[TagSource]

    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id
        self.replaced_by = set()
        self.content = []
        self.sources = set()

    def add_source(self, source: TagSource, tag_json: Dict):
        if tag_json.get("replace", False):
            self.replaced_by.add(source)

        # Merge values from the mod and add the mod as a source for each entry
        entries = tag_json.get("values", [])
        for entry in entries:
            found = False
            for existing_entry in self.content:
                if existing_entry.value == entry:
                    existing_entry.add_source(source)
                    found = True
            if not found:
                self.content.append(TagEntry(entry, {source}))

    def to_json(self):
        return {
            'id': self.id,
            'replaced_by': [s.mod_id for s in self.replaced_by],
            'sources': [s.mod_id for s in self.replaced_by],
            'content': [c.to_json() for c in self.content]
        }

    @classmethod
    def from_json(cls, json, sources: Dict):
        tag = Tag(json['id'])
        tag.sources = {sources[x] for x in json['sources']}
        tag.replaced_by = {sources[x] for x in json['replaced_by']}
        return tag


class TagContainer:
    sources: Set[TagSource]
    items: Dict[str, Tag]
    blocks: Dict[str, Tag]
    fluids: Dict[str, Tag]

    def __init__(self) -> None:
        super().__init__()
        self.sources = set()
        self.items = {}
        self.blocks = {}
        self.fluids = {}

    def add_tag(self, tag_type: str, source: TagSource, tag_id: str, tag_json: Dict):
        self.sources.add(source)

        tag_dict: Dict[str, Tag] = self.__getattribute__(tag_type)

        if tag_id not in tag_dict:
            tag_dict[tag_id] = Tag(tag_id)

        tag_dict[tag_id].add_source(source, tag_json)

    def to_json(self) -> Dict:
        return {
            'sources': {source.mod_id: source.to_json() for source in self.sources},
            'items': [x.to_json() for x in self.items.values()],
            'blocks': [x.to_json() for x in self.blocks.values()],
            'fluids': [x.to_json() for x in self.fluids.values()]
        }

    @classmethod
    def from_json(cls, json):
        tags = TagContainer()
        tags.sources = {TagSource.from_json(x) for x in json['sources'].values()}
        sources = {s.mod_id: s for s in tags.sources}

        def load_tags(key):
            tag_list = [Tag.from_json(x, sources) for x in json[key]]
            return {t.id: t for t in tag_list}

        tags.items = load_tags('items')
        tags.blocks = load_tags('blocks')
        tags.fluids = load_tags('fluids')
        return tags
