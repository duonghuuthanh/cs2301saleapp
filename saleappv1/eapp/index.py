from flask import render_template, request
from eapp import app, dao


@app.route('/')
def index():

    return render_template('index.html',
                           categories=dao.get_categories(),
                           products=dao.get_products(category_id=request.args.get('category_id'),
                                                     kw=request.args.get('kw')))


if __name__ == '__main__':
    app.run(debug=True)
