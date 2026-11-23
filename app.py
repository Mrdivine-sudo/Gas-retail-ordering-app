# Gas Retail Ordering App - by Igwe Divine Chimaobi
# Run: pip install flask -> python app.py -> open http://127.0.0.1:5000
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Simple inventory - in real app, use MySQL
inventory = [
    {"id": 1, "name": "12.5kg Gas Refill", "price": 18500, "stock": 45},
    {"id": 2, "name": "6kg Gas Refill", "price": 9500, "stock": 30},
    {"id": 3, "name": "50kg Gas Refill", "price": 72000, "stock": 12},
    {"id": 4, "name": "12.5kg New Cylinder + Gas", "price": 65000, "stock": 8},
]

orders = []

HTML = """
<!DOCTYPE html><html><head><title>Gas Ordering App</title>
<style>body{font-family:Arial;max-width:800px;margin:auto;padding:20px;background:#f8fafc}
.card{background:#fff;padding:16px;border-radius:12px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
.btn{background:#f97316;color:#fff;padding:10px 18px;border-radius:20px;text-decoration:none;border:none;cursor:pointer;font-weight:700}
input,select{padding:10px;width:100%;margin:6px 0;border-radius:8px;border:1px solid #ddd}
</style></head><body>
<h1>⛽ Gas Retail Ordering App</h1>
<p>Order gas in Enugu - Fast delivery, pay on delivery.</p>
<h2>Available Gas</h2>
{% for item in inventory %}
<div class="card"><div><b>{{item.name}}</b><br>₦{{item.price}} | Stock: {{item.stock}}</div>
<a class="btn" href="/order/{{item.id}}">Order Now</a></div>
{% endfor %}
<h2>Recent Orders: {{orders|length}}</h2>
{% for o in orders %}<div class="card">{{o.name}} - {{o.product}} - ₦{{o.price}} - {{o.phone}}</div>{% endfor %}
<p>Built by Igwe Divine Chimaobi | divineigwe09@gmail.com | 0806 622 6992</p>
</body></html>
"""

ORDER_HTML = """
<!DOCTYPE html><html><head><title>Order</title>
<style>body{font-family:Arial;max-width:500px;margin:auto;padding:20px}
input{padding:12px;width:100%;margin:8px 0;border-radius:8px;border:1px solid #ddd}
button{background:#f97316;color:#fff;padding:12px;width:100%;border:none;border-radius:20px;font-weight:800}</style></head><body>
<h2>Order: {{item.name}} - ₦{{item.price}}</h2>
<form method="POST">
<input name="name" placeholder="Your Full Name" required>
<input name="phone" placeholder="Phone e.g. 0806..." required>
<input name="address" placeholder="Delivery Address in Enugu" required>
<button type="submit">Confirm Order via WhatsApp</button>
</form></body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, inventory=inventory, orders=orders)

@app.route("/order/<int:id>", methods=["GET","POST"])
def order(id):
    item = next((x for x in inventory if x["id"]==id), None)
    if request.method=="POST":
        new_order = {"name": request.form["name"], "phone": request.form["phone"], "product": item["name"], "price": item["price"]}
        orders.append(new_order)
        item["stock"] -= 1
        # WhatsApp link
        msg = f"Hi Divine, I want to order {item['name']} - ₦{item['price']}. Name: {new_order['name']}, Address: {request.form['address']}, Phone: {new_order['phone']}"
        import urllib.parse
        return redirect(f"https://wa.me/2348066226992?text={urllib.parse.quote(msg)}")
    return render_template_string(ORDER_HTML, item=item)

if __name__=="__main__":
    app.run(debug=True)
