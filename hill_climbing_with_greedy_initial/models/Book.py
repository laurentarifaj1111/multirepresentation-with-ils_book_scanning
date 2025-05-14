class Book:
    def __init__(self, id: int, score: int):
        self.id = id
        self.score = score

    def __str__(self):
        return f"Book(id={self.id}, score={self.score})"

    def __repr__(self):
        return self.__str__()
