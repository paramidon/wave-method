# Lite solutions (low problems)

## P1. The last page is missing
User problem: with 41 products and 20 per page, page 3 is missing · feature F1
**Edit:** `shop/pagination.py:9` `pages = total // per_page` → `pages = max(1, -(-total // per_page))` (ceiling
division; an empty list still has one page) · **Check:** new `tests/test_pagination.py`: `page_count(41, 20) == 3`,
`page_count(40, 20) == 2`, `page_count(0, 20) == 1`.

## P2. Order dates in UTC
User problem: order dates are shown in UTC; customers expect the shop's time zone · feature F2
**Edit:** `shop/templates/filters.py:22` (`format_order_date`): convert with
`value.astimezone(ZoneInfo(settings.SHOP_TIMEZONE))` before `strftime("%d.%m.%Y %H:%M")`; naive datetimes are treated
as UTC (`value.replace(tzinfo=timezone.utc)`) · **Check:** new `tests/test_filters.py`: `2026-03-01 22:30 UTC` with
`SHOP_TIMEZONE="Europe/Berlin"` renders `01.03.2026 23:30`; the same naive datetime renders the same.

## P3. E-mail addresses with spaces
User problem: the sign-up form accepts `jane doe@example.com` · feature F3
**Edit:** `shop/validators.py:5` pattern `^.+@.+\..+$` → `^[^\s@]+@[^\s@]+\.[^\s@]+$` · **Check:** new
`tests/test_validators.py`: `jane doe@example.com` and `jane@exa mple.com` are rejected; `jane.doe@example.com` and
`j+tag@shop.co.uk` are accepted.
