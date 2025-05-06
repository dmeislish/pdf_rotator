from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rotate', methods=['POST'])
def rotate():
    degrees = int(request.form['degrees'])
    file = request.files['pdf_file']

    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='rotated.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)