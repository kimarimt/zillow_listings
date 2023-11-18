from helper import get_listings, populate_form


def main():
    listings = get_listings()
    populate_form(listings)


if __name__ == '__main__':
    main()
