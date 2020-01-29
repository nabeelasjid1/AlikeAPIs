from flask import Flask


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return "Hello From The Other World!"


if __name__ == "__main__":
    app.run(debug=True, port=3030)