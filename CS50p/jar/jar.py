class Jar:
    def __init__(self, capacity=12):
        # Check if the capacity is non-negative.
        if capacity < 0:
            raise ValueError

        # Initialize the number of cookies in the jar to 0
        self.cookies_jar = 0

    def __str__(self):
        # Return a string representation of the jar
        return "🍪"*self.size

    def deposit(self, n):
        # Check if the number of cookies to deposit is greater than the capacity.
        if n > self.capacity:
            raise ValueError

        # Deposit the cookies into the jar.
        self.cookies_jar += n

        # Return the number of cookies deposited.
        return n

    def withdraw(self, n):
        # Check if the number of cookies to withdraw is greater than the number of cookies in the jar.
        if self.size < n:
            raise ValueError

        # Withdraw the cookies from the jar.
        self.cookies_jar -= n

        # Return the number of cookies withdrawn.
        return n

    @property
    def capacity(self):
        # Return thee calculated capacity of the jar.
        return 12 - self.cookies_jar

    @property
    def size(self):
        # Return the number of cookies in the jar.
        return self.cookies_jar