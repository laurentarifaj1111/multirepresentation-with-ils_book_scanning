class TweakOperatorParams:
    def __init__(self):
        self.book_scores = {}

    @staticmethod
    def from_solution(solution, instance):
        params = TweakOperatorParams()
        params.book_scores = TweakOperatorParams.get_book_scores(instance)
        return params

    @staticmethod
    def get_book_scores(instance):
        book_scores = {}
        for library in instance.libraries:
            for book in library.books:
                # If a book ID already exists, keep the first score (just like (existing, replacement) -> existing in Java)
                if book.id not in book_scores:
                    book_scores[book.id] = book.score
        return book_scores
