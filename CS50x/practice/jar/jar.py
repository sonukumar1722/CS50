class Jar:

    def __init__(self, capacity=12):
        self.jar = capacity
        if self.jar < 0:
            raise ValueError()


    def __str__(self):
        return "🍪" * self.jar

    def deposit(self, n):
        self.cookie = 0
        self.cookie += n
        if self.cookie > self.jar:
            raise ValueError()

    def withdraw(self, n):
        self.cookie -= n
        if self.cookie < 0:
            raise ValueError()

    @property
    def capacity(self):
        return jar

    @property
    def size(self):
        return self.cookie



def main():
    jar = Jar()
    print(str(jar.jar))
    print(str(jar))
    jar.deposit(2)
    print(str(jar))
    jar.withdraw(1)
    print(str(jar))

if __name__ == "__main__":
    main()

