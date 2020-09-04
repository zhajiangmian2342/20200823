from flask import Blueprint, render_template, jsonify, request

from automation.service import Service

automation=Blueprint('automation',__name__,
          static_folder='static',
          template_folder='templates',
          url_prefix='/automation/')

@automation.route('/')
def index():
    return render_template('automation.html')

@automation.route('/api/v1/run',methods=['POST'])
def run():
    data = request.get_json()
    if 'casename' not in data or not data['casename']:
        return jsonify({
            'status':400,
            'message':'invalid parameter [casename]',
            'data':data

        })
    if 'commands' not in data or not data['commands']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [commands]',
            'data': data

        })
    try:
        service = Service()
        service.execute(data['commands'])
        return jsonify({
            'status':0,
            'message':'ok',
            'data':data
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': str(e),
            'data': data

        })


@automation.route('/api/v1/save',methods=['POST'])
def save():
    data = request.get_json()
    if 'casename' not in data or not data['casename']:
        return jsonify({
            'status':400,
            'message':'invalid parameter [casename]',
            'data':data

        })
    if 'commands' not in data or not data['commands']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [commands]',
            'data': data

        })
    try:
        service = Service()
        data = service.save(data)
        return jsonify({
            'status':0,
            'message':'ok',
            'data':data
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': str(e),
            'data': data

        })


@automation.route('/api/v1/trigger')
def api_v1_trigger():
    '''
    需要传测试用例的id值到后台
    '''
    data = request.values.to_dict()
    id = data.get('id')
    if not id:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [id]',
            'data': data

        })
    service = Service()
    data = service.trigger(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })