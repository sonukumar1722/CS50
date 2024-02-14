
def main():
    now = input("What time is it? ")
    try:
        time, am_pm = now.split(" ")
        hours, minutes = time.split(":")
        if am_pm == 'p.m.':
            hours = int(hours) + 12
        elif am_pm == 'a.m.':
            hours = int(hours)
        else:
            ...
        convert(f"{hours}:{minutes}")
    except :
        convert(now)


def convert(time):
    hours, minutes = time.split(":")
    hours = int(hours)
    minutes = int(minutes)

    if  7 <= hours <= 8:
        print("breakfast time")
    elif 12 <= hours <= 13:
        print("lunch time")
    elif 18 <= hours <= 19:
        print("dinner time")
    else:
        pass

    return hours + minutes / 60

if __name__ == "__main__":
    main()