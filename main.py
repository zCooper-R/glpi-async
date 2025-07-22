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
        tickets = await glpi.tickets.list_open_tickets_with_assignees()
        message_lines = ["🔔 Открытые заявки GLPI:\n"]
        for ticket in tickets.get('data'):
            # Форматируем вывод, например:
            ticket_id = ticket.get("Ticket.id", "Без названия")  # имя заявки
            ticket_name = ticket.get("Ticket.name", "Без названия")  # имя заявки
            assignee_name = ticket.get("Ticket.users_id_recipient.User.name", "Не назначен")  # id ответственного
            content = ticket.get("Ticket.content", "Не назначен")  # имя ответственного

            message_lines.append(f"#{ticket_id}: {ticket_name}\nОтветственный: {assignee_name} (Описание: {content})\n")

        message_text = "\n".join(message_lines)
        print(message_text)


if __name__ == '__main__':
    asyncio.run(main())
