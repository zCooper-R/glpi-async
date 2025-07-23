from datetime import datetime
from pprint import pprint

from glpi_async.client import GLPIClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def main():
    async with GLPIClient(
            app_token=os.getenv("GLPI_APP_TOKEN"),
            user_token=os.getenv("GLPI_USER_TOKEN"),
            base_url=os.getenv("GLPI_API_URL")
    ) as glpi:
        # glpiID = await glpi.users.get_my_id()
        tickets = await glpi.categories.list()
        print(tickets)

if __name__ == '__main__':
    asyncio.run(main())
