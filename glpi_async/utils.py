from datetime import datetime
import re


def parse_time_to_resolve(input_str: str) -> datetime:
    """
    print(parse_time_to_resolve("14"))                 # 14 this month 00:00
    print(parse_time_to_resolve("1410 2155"))          # 14 Oct this year 21:55
    print(parse_time_to_resolve("14.10.2025 21:55"))   # exact
    print(parse_time_to_resolve("14-10-2025 2155"))    # with dash
    print(parse_time_to_resolve("141020 2155"))        # compact
    """

    input_str = input_str.strip().replace("-", ".")
    now = datetime.now()

    # Формат: 14.10.2025 21:55
    full_match = re.match(r"(\d{1,2})[.](\d{1,2})[.](\d{4})(?:\s+(\d{2})(\d{2}))?", input_str)
    if full_match:
        day, month, year, hour, minute = full_match.groups()
        return datetime(
            int(year), int(month), int(day),
            int(hour or 0), int(minute or 0)
        )

    # Формат: 141020 2155 (без точек)
    digits = re.findall(r"\d+", input_str)
    if len(digits) == 2:  # Дата + время
        date, time = digits
    elif len(digits) == 1:
        date, time = digits[0], None
    else:
        raise ValueError("Неверный формат даты")

    day = int(date[:2])
    month = int(date[2:4]) if len(date) >= 4 else now.month
    year = int("20" + date[4:6]) if len(date) == 6 else now.year

    hour = int(time[:2]) if time else 0
    minute = int(time[2:]) if time and len(time) >= 4 else 0

    return datetime(year, month, day, hour, minute)
