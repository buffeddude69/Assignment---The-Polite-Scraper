from catalogue import discover_books
from books import fetch_book


def main():

    books = discover_books()

    records = []

    for book in books:

        record = fetch_book(book)

        if record is not None:
            records.append(record)

    print(
        f"detail_pages={len(records)}"
    )

    if records:

        print("\nFIRST RAW RECORD:")

        print(records[0])


if __name__ == "__main__":
    main()