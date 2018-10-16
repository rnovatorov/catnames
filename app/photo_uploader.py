import asks


class Photo:

    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return self._data['id']

    @property
    def owner_id(self):
        return self._data['owner_id']

    def as_attachment(self):
        return f'photo{self.owner_id}_{self.id}'


class PhotoUploader:

    def __init__(self, api):
        self._api = api
        self._server = None
        self._upload_url = None

    async def get_server(self):
        if self._server is None:
            self._server = await self._api.photos.getMessagesUploadServer()
        return self._server

    async def get_upload_url(self):
        server = await self.get_server()
        return server['upload_url']

    async def save(self, **params):
        photos = await self._api.photos.saveMessagesPhoto(**params)
        return photos[0]

    async def upload(self, filename):
        upload_url = await self.get_upload_url()
        response = await asks.post(upload_url, files={'photo': filename})
        save_params = response.json()
        photo = await self.save(**save_params)
        return Photo(photo)
