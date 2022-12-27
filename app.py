"""
A web-app that calculates the time it will take for you to get your book.
Written by Brayden/Rowan Lee for a local technology competition.
Licensed under Apache 2.0.
"""
from datetime import date
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


def get_stuff(target: str) -> Flask.request_class.json:
    """Obtains data from https://howlongtoread.com/."""
    url = f"https://api.howlongtoread.com/books/search/{target}"
    response = requests.get(url, timeout=60)
    return response.json()


def calculate_times(avg_read_time: int, position: int) -> tuple[int, int]:
    """Calculates and returns the minimum and maximum theoretical wait times."""
    day = date.today()
    minutes = avg_read_time / 60

    weekday = 45
    weekend = 60
    transport_delay = 1

    days = 0
    while minutes > 0:
        if day.weekday():
            minutes = minutes - weekday
        else:
            minutes = minutes - weekend
        days = days + 1

    days = days + transport_delay
    return (days, position * 3 * 7)


@app.route("/")
def root():
    """Program body, handles the data from the form."""
    args = request.args
    arg_len = 0
    for _ in args.items():
        arg_len = arg_len + 1
    if arg_len == 0:
        return render_template("index.html")
    book = args.get('title')
    author = args.get('author')
    position = abs(int(args.get('position')))
    json = get_stuff(f"{book} {author}")
    json = json[0]

    author = json['author']
    avg_read_time = json['averageReadingTime']
    image = json['smallImage']
    book = json['title']
    if position == 0:
        min_time = 0
        max_time = 2
    elif avg_read_time == 0:
        min_time = "(given the lack of data) an incalculable number of"
    else:
        min_time, max_time = calculate_times(avg_read_time, position)

    return render_template(
        "result.html",
        book=book,
        author=author,
        image=image,
        min_wait=min_time,
        max_wait=max_time
    )
