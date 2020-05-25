from flask import Flask, render_template, request, redirect
from aladin import get_books

app = Flask('SECOND HAND')

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    keyword = request.args.get('keyword')
    if keyword:
        keyword = keyword.lower()
        existing_books = db.get(keyword)
        if existing_books:
            books = existing_books
        else:
            books = get_books(keyword)
            db[keyword] = books
    else:
        return redirect("/")
    return render_template(
        "report.html",
        searching_keyword=keyword,
        result_count=len(books),
        books=books
    )


app.run()
