class Property:
    internal_id: str
    provider: str
    url: str

    def __init__(self, internal_id, provider, url):
        self.internal_id = internal_id
        self.provider = provider
        self.url = url
