from flask import Flask, render_template, request, make_response
# from websiteSearchCopy import get_data
from housing_search import get_data, get_sortedData
import pandas as pd

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    apts = pd.DataFrame({'Name': [], 'Link': [], 'Price': [], 'Beds': [], 'Bath': []})
    if request.method == 'POST':
        text = request.form['text']
        apts = get_data(text)
        # print(apts)
    return render_template('index.html', apts=apts)

@app.route('/sort', methods=['GET','POST'])
def sort():
    apts = pd.DataFrame({'Name': [], 'Link': [], 'Price': [], 'Beds': [], 'Bath': []})
    sort_type = request.form['value']
    print(sort_type)
    apts = get_sortedData(sort_type)
    print(f'{apts}')
    return render_template('index.html', apts = apts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    # app.run()
