from flask import Flask, jsonify

app = Flask(__name__)

books = {
    1: {"title": "DOS Guide", "stock": 5, "price": 50, "topic": "distributed systems"},
    2: {"title": "RPC for Noobs", "stock": 3, "price": 40, "topic": "distributed systems"},
    3: {"title": "Undergrad Survival", "stock": 7, "price": 30, "topic": "undergraduate"},
    4: {"title": "Cooking Guide", "stock": 2, "price": 20, "topic": "undergraduate"}
}

@app.route('/info/<int:item_id>')
def info(item_id):
    if item_id in books:
        return jsonify(books[item_id])
    return jsonify({"error": "Not found"}), 404


@app.route('/purchase/<int:item_id>')
def update_stock(item_id):

   
    if item_id in books:
        if books[item_id]["stock"] > 0:
            books[item_id]["stock"] -= 1

            return jsonify({
                "title": books[item_id]["title"],   # 👈 مهم جدًا
                "stock": books[item_id]["stock"]
            })

        return jsonify({"error": "Out of stock"}), 400

    return jsonify({"error": "Not found"}), 404

@app.route('/search/<topic>')
def search(topic):
    result = {}

    for id, book in books.items():
        if book["topic"] == topic:
            result[book["title"]] = id

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)