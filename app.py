from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
@app.route("/<q>")
def index(q=""):
    # if no query just render the base.html
    if not q:
        return render_template("base.html")
    return jsonify({'response': q})

if __name__ == "__main__":
    app.run(debug=True)
