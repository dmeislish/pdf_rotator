from flask import Flask, request, send_file, render_template
import fitz  # PyMuPDF
import io
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rotate', methods=['POST'])
def rotate_pdf():
    uploaded_file = request.files['pdf_file']
    angle = float(request.form['degrees'])

    # שמירה זמנית של הקובץ המקורי
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        uploaded_file.save(temp_input.name)
        input_path = temp_input.name

    # יצירת קובץ זמני לפלט
    output_stream = io.BytesIO()
    rotated_doc = fitz.open()

    doc = fitz.open(input_path)

    for page in doc:
        rotation_matrix = fitz.Matrix(1, 1).prerotate(angle)
        pix = page.get_pixmap(matrix=rotation_matrix, alpha=False)
        new_page = rotated_doc.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(new_page.rect, pixmap=pix)

    rotated_doc.save(output_stream)
    output_stream.seek(0)

    return send_file(output_stream, as_attachment=True, download_name="rotated.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
