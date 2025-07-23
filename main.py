from datetime import datetime, timedelta
from pprint import pprint

from glpi_async.client import GLPIClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def weekly_summary():
    seven_days_ago = (datetime.now() - timedelta(days=7))
    async with GLPIClient(
            app_token=os.getenv("GLPI_APP_TOKEN"),
            user_token=os.getenv("GLPI_USER_TOKEN"),
            base_url=os.getenv("GLPI_API_URL")
    ) as glpi:
        closed = await glpi.tickets.query().show('22').created_after(seven_days_ago).where(12, 6).get()
        opened = await glpi.tickets.query().created_after(seven_days_ago).where(12, 2).get()
        from collections import Counter
        assigned_ids = [row.get("Ticket.users_id_recipient.User.name") for row in closed.get('data')]
        most_common_username = Counter(assigned_ids).most_common(1)
        # Формируем сообщение
        text = (
            f"📊 За неделю:\n"
            f"✅ Закрыто: {closed.get('totalcount')} заявок\n"
            f"🚨 Открыто: {opened.get('totalcount')} новых\n"
            f"👤 Самый активный техник: {most_common_username[0][0]}"
        )

        return text


async def main():
    a = await weekly_summary()
    print(a)


if __name__ == '__main__':
    asyncio.run(main())
