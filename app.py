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

@app.route('/ads.txt')
def ads():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'ads.txt') 
    
    
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

@app.route('/number', methods=['POST'])
def number_pdf():
    if 'pdf_file' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['pdf_file']
    if file.filename == '':
        return 'No selected file.', 400

    style = request.form.get('style', '1')

    filename = secure_filename(file.filename)
    input_path = os.path.join('uploads', filename)
    output_path = os.path.join('output', f"numbered_{filename}")

    os.makedirs('uploads', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    file.save(input_path)
    doc = fitz.open(input_path)

    for page_number in range(len(doc)):
        page = doc[page_number]
        num = page_number + 1

        if style == '1':
            text = str(num)
        elif style == '-1-':
            text = f"-{num}-"
        elif style == 'Page':
            text = f"Page {num}"
        else:
            text = str(num)

        rect = page.rect
        x = rect.width / 2
        y = rect.height - 20
        page.insert_text((x, y), text, fontsize=12, color=(0, 0, 0), render_mode=0, align=1)

    doc.save(output_path)
    doc.close()

    return send_file(output_path, as_attachment=True)
