from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
@app.route('/home', methods=['POST'])
def index():
    return render_template("dxr_test.html")

if __name__ == '__main__':
    app.run(debug=True)