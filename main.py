import pandas_profiling as pp
import pandas as pd
from flask import Flask, abort, render_template, request, redirect, url_for, flash
from werkzeug import secure_filename
import os
import secrets

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def upload():
    random_hex = secrets.token_hex(16)
    if request.method == 'POST':
        upload_path = os.path.join(app.root_path, 'file')
        file = request.files['file']
        if ".csv" in file.filename:
            _, f_ext = os.path.splitext(file.filename)
            csv_file = random_hex + f_ext
            file.save(os.path.join(upload_path, csv_file))
            df = pd.read_csv(os.path.join(upload_path, csv_file))
            report = pp.ProfileReport(df, minimal=True)
            html_report_path = 'templates/' + random_hex + '.html'
            report.to_file(html_report_path)
            return redirect(url_for('report', val=random_hex))
        else:
            flash("Please upload a CSV file!", "danger")
    return render_template('upload.html')


@ app.route('/about')
def about():
    return render_template("about.html")


@ app.route('/report', methods=['GET', 'POST'])
def report():
    hex_val = request.args.get('val')
    report = hex_val + ".html"
    return render_template(report)


if __name__ == '__main__':
    app.run(debug=False)
