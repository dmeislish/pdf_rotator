from flask import Flask, render_template, request, send_file
import os
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rotate", methods=["GET", "POST"])
def rotate_pdf():
    if request.method == "POST":
        pdf_file = request.files["pdf_file"]
        degrees = int(request.form["degrees"])

        filename = secure_filename(pdf_file.filename)
        input_path = os.path.join("uploads", filename)
        output_path = os.path.join("uploads", f"rotated_{filename}")

        os.makedirs("uploads", exist_ok=True)
        pdf_file.save(input_path)

        doc = fitz.open(input_path)
        for page in doc:
            page.set_rotation(degrees)
        doc.save(output_path)

        return send_file(output_path, as_attachment=True)
    return render_template("rotate.html")

@app.route("/number", methods=["GET", "POST"])
def add_page_numbers():
    if request.method == "POST":
        pdf_file = request.files["pdf_file"]
        style = request.form["style"]

        filename = secure_filename(pdf_file.filename)
        input_path = os.path.join("uploads", filename)
        output_path = os.path.join("uploads", f"numbered_{filename}")

        os.makedirs("uploads", exist_ok=True)
        pdf_file.save(input_path)

        doc = fitz.open(input_path)

        for i, page in enumerate(doc, start=1):
            if style == "1":
                number = str(i)
            elif style == "-1-":
                number = f"-{i}-"
            elif style == "Page":
                number = f"Page {i}"
            else:
                number = str(i)
            page.insert_text((50, page.rect.height - 30), number, fontsize=12, color=(0, 0, 0))

        doc.save(output_path)
        return send_file(output_path, as_attachment=True)
    return render_template("number.html")

if __name__ == "__main__":
    app.run(debug=True)
