from datetime import date


# Datas sem sessão de negociação nos calendários oficiais da B3.
B3_CLOSED_DATES = {
    # 2025
    date(2025, 1, 1),
    date(2025, 3, 3),
    date(2025, 3, 4),
    date(2025, 4, 18),
    date(2025, 4, 21),
    date(2025, 5, 1),
    date(2025, 6, 19),
    date(2025, 11, 20),
    date(2025, 12, 24),
    date(2025, 12, 25),
    date(2025, 12, 31),
    # 2026
    date(2026, 1, 1),
    date(2026, 2, 16),
    date(2026, 2, 17),
    date(2026, 4, 3),
    date(2026, 4, 21),
    date(2026, 5, 1),
    date(2026, 6, 4),
    date(2026, 9, 7),
    date(2026, 10, 12),
    date(2026, 11, 2),
    date(2026, 11, 20),
    date(2026, 12, 24),
    date(2026, 12, 25),
    date(2026, 12, 31),
}


def is_b3_trading_day(value: date) -> bool:
    return value.weekday() < 5 and value not in B3_CLOSED_DATES
