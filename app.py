from flask import Flask, render_template, request, send_file
import os
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/rotate', methods=['GET', 'POST'])
def rotate():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        degrees = int(request.form['degrees'])

        filename = secure_filename(pdf_file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, 'rotated_' + filename)

        pdf_file.save(input_path)
        rotate_pdf(input_path, output_path, degrees)

        return send_file(output_path, as_attachment=True)

    return render_template('rotate.html', title='Rotate PDF')

@app.route('/number', methods=['GET', 'POST'])
def number():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        style = request.form['style']

        filename = secure_filename(pdf_file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, 'numbered_' + filename)

        pdf_file.save(input_path)
        add_page_numbers(input_path, output_path, style)

        return send_file(output_path, as_attachment=True)

    return render_template('number.html', title='Number Pages')

def rotate_pdf(input_path, output_path, angle):
    doc = fitz.open(input_path)
    rotated_doc = fitz.open()

    for page in doc:
        mat = fitz.Matrix(1, 1).prerotate(angle)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        new_page = rotated_doc.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(new_page.rect, pixmap=pix)

    rotated_doc.save(output_path)

def add_page_numbers(input_path, output_path, style):
    doc = fitz.open(input_path)

    for i, page in enumerate(doc, start=1):
        if style == "1":
            text = str(i)
        elif style == "-1-":
            text = f"-{i}-"
        elif style == "Page":
            text = f"Page {i}"
        else:
            text = str(i)

        rect = fitz.Rect(50, page.rect.height - 30, page.rect.width - 50, page.rect.height - 10)
        page.insert_textbox(rect, text, fontsize=12, align=1)

    doc.save(output_path)

if __name__ == '__main__':
    app.run(debug=True)
