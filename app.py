from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = int(request.form['age'])
    income = int(request.form['income'])
    state = request.form['state']
    caste = request.form['caste'].lower()

    eligible_schemes = []

    if income < 250000:
        eligible_schemes.append("Pradhan Mantri Awas Yojana")
        eligible_schemes.append("PM Ujjwala Yojana")

    if caste in ['sc', 'st', 'obc']:
        eligible_schemes.append("Pre-Matric Scholarship Scheme")

    if state.lower() == "andhra pradesh":
        eligible_schemes.append("YSR Pension Kanuka")

    if not eligible_schemes:
        eligible_schemes.append("No major schemes found. Try again with more accurate data.")

    return render_template('result.html', name=name, schemes=eligible_schemes)

if __name__ == '__main__':
    app.run(debug=True)
