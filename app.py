import os
from flask import Flask, render_template, request, send_from_directory
import pandas as pd

app = Flask(__name__)
df = pd.read_excel('medi_price_Fixed.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    if query:
        results = df[df['الرمز - Code'].astype(str).str.contains(query, case=False, na=False) |
                     df['Medication Name'].str.contains(query, case=False, na=False) |
                     df['اسم الدواء'].str.contains(query, case=False, na=False)]
        if not results.empty:
            results['الرمز - Code'] = results['الرمز - Code'].astype('Int64').astype(str)
            tables = [results.to_html(classes='results-table', header=True, index=False)]
            return render_template('index.html', tables=tables)
        else:
            message = "not found - لايوجد"
            return render_template('index.html', message=message)
    else:
        message = "Please enter a search query."
        return render_template('index.html', message=message)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(directory='.', path=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
