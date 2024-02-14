def main():
    date = get_date()
    print(f'{date[0].zfill(4)}-{date[1].zfill(2)}-{date[2].zfill(2)}')

def get_date():
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    while True:
        try:
            date = input("Date: ").strip()
            try:
                month, day, year = date.split('/')
                if 1 <= int(month) <= 12  and 1 <= int(day) <= 31 and len(year) == 4:
                    return (year, month, day)
            except:
                month, day, year = date.split()
                if ',' in day:
                    day = day.replace(',', '')
                    if month in months and 1 <= int(day) <= 31 and len(year) == 4:
                        return (year, str(months.index(month.capitalize()) + 1), day)
        except:
            pass


main()