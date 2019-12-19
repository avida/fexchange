from utils import logger
from io import BytesIO
from asyncio import StreamReader
from collections import defaultdict
from zipfile import ZipFile, ZIP_DEFLATED
import random
import string

class StorageController:
    def __init__(self):
        self.directories = defaultdict(dict)
        logger.info("Create storage controler")

    async def save_file(self, filename, file_content: StreamReader, directory):
        logger.info("Saving file")
        content = BytesIO()
        while True:
            chunk = await file_content.read(1024)
            if not chunk:
                break
            content.write(chunk)
        content = content.getvalue()
        logger.info(f"Saving file {len(content)}")
        self.directories[directory][filename] = content

    def get_file(self, directory, filename) -> bytes:
        logger.info(f"Getting file {filename} from {directory}")
        if directory not in self.directories or \
            filename not in self.directories[directory]:
            return None
        return self.directories[directory][filename]

    def get_directory(self, directory) -> bytes:
        logger.info(f"Getting {directory} content")
        if directory not in self.directories:
            return None
        response = BytesIO()
        with ZipFile(response, mode="w", compression=ZIP_DEFLATED) as zipfile:
            for filename, content in self.directories[directory].items():
                with zipfile.open(filename, "w") as fl:
                    fl.write(content)
        return response.getvalue()

    def new_directory(self):
        for _ in range(0,10):
            random_name = "".join(random.choices(string.ascii_lowercase+string.digits, k=3))
            if random_name not in self.directories:
                return random_name
        return None
