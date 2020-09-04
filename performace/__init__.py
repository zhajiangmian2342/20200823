from flask import Blueprint, render_template, request, jsonify

from performace.service import Service

performance = Blueprint('performance',
          __name__,
          static_folder='static',
          template_folder='templates',
          url_prefix='/performance')


@performance.route('/')
def index():
    return render_template('performance.html')

@performance.route('/api/v1/go',methods=['POST'])
def api_v1_go():
    data = request.get_json()
    # 参数校验
    code = data.get('code')
    if not code:
        return jsonify({
            'status':400,
            'message':'invalid parameter "code"',
            'data':data
        })
    host=data.get('host')
    if not host:
        return jsonify({
            'status':400,
            'message':'invalid parameter "host"',
            'data':data
        })
    # 业务逻辑的处理
    service = Service()
    data = service.excute(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })
