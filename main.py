from flask import Flask, render_template, url_for, request, redirect, flash
import os
import sys
import subprocess
import torch
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'your_secret_key'  # Needed for flashing messages

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
    # Determine the latest generated model
    static_dir = os.path.join(os.getcwd(), "static")
    ply_files = [f for f in os.listdir(static_dir) if f.endswith('.ply')]
    if ply_files:
        latest_ply = sorted(ply_files)[-1]  # Assuming lex order corresponds to generation order
        model_url = url_for('static', filename=latest_ply)
    else:
        model_url = None  # No model generated yet
    return render_template('space-builder.html', model_url=model_url)

@app.route("/viewer")
def viewer():
    return render_template('viewer.html')

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt")
    if not prompt:
        flash("Please enter a prompt.", "warning")
        return redirect(url_for("spacebuilder"))

    # Define the path to the modeling script
    modeling_script = os.path.join(os.getcwd(), "shap_e", "examples", "modeling.py")

    # Execute the modeling script with the prompt
    try:
        # Using subprocess to call the modeling script
        subprocess.run([sys.executable, modeling_script, prompt], check=True)
        flash("Model generated successfully!", "success")
    except subprocess.CalledProcessError as e:
        print(f"Error generating model: {e}")
        flash("Failed to generate model. Please try again.", "danger")

    return redirect(url_for("spacebuilder"))

if __name__ == "__main__":
    app.run(debug=True)
