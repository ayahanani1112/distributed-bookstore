from flask import Flask, jsonify
import requests

app = Flask(__name__)

CATALOG_URL = "http://catalog:5001"

orders = []

@app.route('/purchase/<int:item_id>')
def purchase(item_id):
    try:
        print(f"📥 New purchase request for item {item_id}")

        # طلب من catalog لتحديث المخزون
        response = requests.get(f"{CATALOG_URL}/purchase/{item_id}", timeout=3)

        # ❗ تحقق من الخطأ
        if response.status_code != 200:
            print("❌ Item not found in catalog")
            return jsonify({"error": "Item not found in catalog"}), 404

        book = response.json()

        # ❗ تحقق من وجود title
        if "title" not in book:
            print("⚠️ No title returned from catalog")
            book["title"] = "Unknown"

    except requests.exceptions.ConnectionError:
        print("❌ Catalog service OFF")
        return jsonify({"error": "Catalog service is OFF"}), 500

    except requests.exceptions.Timeout:
        print("⏳ Catalog timeout")
        return jsonify({"error": "Catalog is too slow"}), 500

    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return jsonify({"error": str(e)}), 500

    # ✅ تسجيل الطلب بشكل واضح
    order = {
        "item_id": item_id,
        "title": book.get("title", "Unknown")
    }

    orders.append(order)

    print(f"✅ Order saved: {order}")

    return jsonify({
        "message": f"{order['title']} purchased successfully ✅"
    })


# 🟢 عرض جميع الطلبات
@app.route('/orders')
def get_orders():
    print("📦 Fetching all orders")
    return jsonify(orders)


# 🟢 (إضافة احترافية) مسح الطلبات
@app.route('/clear')
def clear_orders():
    orders.clear()
    print("🗑️ Orders cleared")
    return jsonify({"message": "All orders cleared"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)