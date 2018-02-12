import queue
import threading
count_fetchers = 5


def source():
    return [{'n': 'a'}, {'n': 'b'}, {'n': 'c'}]


def do_work(item):
    item['r'] = 1


def worker():
    while True:
        item = queue_unprocessed_films.get()
        if item is None:
            break
        do_work(item)
        queue_unprocessed_films.task_done()

queue_unprocessed_films = queue.Queue()
film_fetchers = [threading.Thread(target=worker) for i in range(count_fetchers)]
for film_fetcher in film_fetchers:
    film_fetcher.start()
films = source()
for item in films:
    queue_unprocessed_films.put(item)

# block until all tasks are done
queue_unprocessed_films.join()

# stop workers
for i in range(count_fetchers):
    queue_unprocessed_films.put(None)
for film_fetcher in film_fetchers:
    film_fetcher.join()
print(films)
