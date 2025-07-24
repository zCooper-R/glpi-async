from collections import Counter
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
        # Закрытые заявки (12 - статус, 6 - закрыто)
        closed = await glpi.tickets.query() \
            .created_after(seven_days_ago) \
            .where(12, 6).show("22").get()

        # Открытые заявки (12 - статус, 2 - открыто)
        opened = await glpi.tickets.query() \
            .created_after(seven_days_ago) \
            .where(12, 2).get()
        assigned = [
            row.get("Ticket.users_id_recipient.User.name")
            for row in closed.get("data", [])
            if row.get("Ticket.users_id_recipient.User.name")
        ]
        counter = Counter(assigned)

        top_technician = counter.most_common(1)[0][0] if counter else "—"
        tech_stats = "\n".join(
            [f"• {name} — {count}" for name, count in counter.most_common()]
        ) if counter else "—"

        text = (
            f"📊 <b>За неделю:</b>\n"
            f"✅ <b>Закрыто:</b> {closed.get('totalcount', 0)} заявок\n"
            f"🚨 <b>Открыто:</b> {opened.get('totalcount', 0)} новых\n"
            f"👤 <b>Самый активный техник:</b> {top_technician}\n"
            f"📋 <b>Рейтинг техников:</b>\n{tech_stats}"
        )

        return text


async def main():
    a = await weekly_summary()
    print(a)


if __name__ == '__main__':
    asyncio.run(main())
