from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/download")
def download():
    return render_template('download.html')

@app.route("/products")
def products():
    return render_template('products.html')

@app.route("/spacebuilder")
def spacebuilder():
    return render_template('space-builder.html')

@app.route("/viewer")
def viewer():
    return render_template('viewer.html')