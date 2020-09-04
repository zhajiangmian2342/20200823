# 必须用python run.py去运行才能生成覆盖率的报告
import coverage



cov = coverage.Coverage()
cov.start()

from flask import Flask, render_template

from automation import automation
from interface import interface
from variable import variable
from performace import performance

app = Flask(__name__)
app.register_blueprint(interface)
app.register_blueprint(variable)
app.register_blueprint(automation)
app.register_blueprint(performance)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    cov.stop()
    cov.save()
    cov.html_report()
