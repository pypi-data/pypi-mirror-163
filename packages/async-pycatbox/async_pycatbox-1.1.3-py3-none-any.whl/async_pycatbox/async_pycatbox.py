import sys
import aiohttp


class Uploader:
    """
    Simple class, just for ease of repeatedly uploading files.
    """

    def __init__(self, token: str = ""):
        """
        Initializes the uploader.

        Parameters
        ----------
        token : str, optional
            The token to use when uploading a file to catbox, by default ""
        """
        self.token = token
        self.apiUrl = "https://catbox.moe/user/api.php"

    async def upload(
        self, file_type: str = None, file_raw: bytes = None, quiet: bool = False
    ) -> str:
        """
        For uploading a file to catbox.

        Parameters
        ----------
        file_type : str, optional
            The type of file, should just be its extension most of the time, by default
            None
        file_raw : bytes, optional
            The raw bytes of the file (for example by using open with the 'rb' flag), by
            default None
        quiet : bool, optional
            Whether or not it should output an error upon an issue.

        Returns
        -------
        str
            Returns the url of the newly uploaded post.
        """
        data = aiohttp.FormData()
        data.add_field("reqtype", "fileupload")
        data.add_field("userhash", self.token)
        data.add_field("fileToUpload", file_raw, filename="file.{}".format(file_type))
        async with aiohttp.ClientSession() as session:

            async def post(data) -> str:
                async with session.post(self.apiUrl, data=data) as response:
                    resp = response
                    text = await resp.text()
                    if not response.ok:
                        if not quiet:
                            print(
                                "Error with uploading to catbox, status {} with text"
                                " '{}' and headers {}".format(response.status, text, response.headers),
                                file=sys.stderr,
                            )
                        return None
                    return text

            return await post(data)
