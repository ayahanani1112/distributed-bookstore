from flask import Flask, render_template_string
import requests

app = Flask(__name__)

CATALOG_URL = "http://catalog:5001"
ORDER_URL = "http://order:5002"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Book Store</title>
    <style>
        body {
            font-family: Arial;
            background-color: #f4f6f8;
            margin: 0;
            padding: 20px;
        }

        h1 {
            color: #333;
        }

        .container {
            max-width: 800px;
            margin: auto;
        }

        .card {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        .book {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .btn {
            background: #4CAF50;
            color: white;
            padding: 6px 12px;
            text-decoration: none;
            border-radius: 6px;
        }

        .btn:hover {
            background: #45a049;
        }

        .out {
            background: gray;
            pointer-events: none;
        }

        .orders {
            background: #fff;
            padding: 10px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body>

<div class="container">

<h1>📚 Book Store</h1>

<h2>Available Books</h2>

{% for id, book in books.items() %}
<div class="card book">
    <div>
        <b>{{book.title}}</b><br>
        Stock: {{book.stock}}
    </div>

    {% if book.stock > 0 %}
        <a class="btn" href="/buy/{{id}}">Buy</a>
    {% else %}
        <span class="btn out">Out of stock</span>
    {% endif %}
</div>
{% endfor %}

<div class="orders">
<h2>📦 Orders</h2>

{% for title, count in orders.items() %}
    <div>✔ {{title}} × {{count}}</div>
{% endfor %}

</div>

</div>

</body>
</html>
"""

@app.route('/')
def home():
    books = {}

    try:
        results = requests.get(
            f"{CATALOG_URL}/search/distributed%20systems",
            timeout=3
        ).json()

        for title, item_id in results.items():
            info = requests.get(
                f"{CATALOG_URL}/info/{item_id}",
                timeout=3
            ).json()

            books[item_id] = {
                "title": info.get("title", "Unknown"),
                "stock": info.get("stock", 0)
            }

    except Exception as e:
        print("❌ Error fetching books:", e)
        books = {}

    try:
        raw_orders = requests.get(
            f"{ORDER_URL}/orders",
            timeout=3
        ).json()

        orders = {}
        for order in raw_orders:
            title = order.get("title", "Unknown")

            if title in orders:
                orders[title] += 1
            else:
                orders[title] = 1

    except Exception as e:
        print("❌ Error fetching orders:", e)
        orders = {}

    return render_template_string(HTML, books=books, orders=orders)


@app.route('/buy/<int:item_id>')
def buy(item_id):
    try:
        requests.get(
            f"{ORDER_URL}/purchase/{item_id}",
            timeout=3
        )
    except Exception as e:
        print("❌ Purchase error:", e)

    return "<h2>✅ Purchased! <a href='/'>Back</a></h2>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)