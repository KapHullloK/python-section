from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias, Iterator

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int):
        self.per_page = per_page
        self.page = 1

    def __iter__(self) -> Iterator[SomeRemoteData]:
        while True:
            response = request(
                Query(per_page=self.per_page, page=self.page)
            )

            for item in response.results:
                yield item

            if response.next is None:
                break

            self.page = response.next


class Fibo:
    def __init__(self, n: int):
        self.n = n

    def __iter__(self) -> 'Fibo':
        self.prev, self.cur = 0, 1
        self.position = 0
        return self

    def __next__(self) -> int:
        if self.position >= self.n:
            raise StopIteration

        self.position += 1

        if self.position == 1:
            return self.prev
        elif self.position == 2:
            return self.cur
        else:
            self.prev, new_cur = self.cur, self.cur + self.prev
            self.cur = new_cur
            return self.cur
