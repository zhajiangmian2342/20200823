from flask import Blueprint, render_template, request, jsonify

from variable.service import Service

variable = Blueprint('variable',
          __name__,
          static_folder='static',
          template_folder='templates',
          url_prefix='/variable')

@variable.route('/')
def index():
    return render_template('variable.html')

@variable.route('/keyword')
def keyword():
    return render_template('keyword.html')


@variable.route('/api/v1/delete',methods=['POST'])
def api_v1_delete():
    # post请求
    data = request.get_json()
    # 参数校验
    if 'id_list' not in data or not data['id_list']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters type',
            'data': data
        })

    # 业务逻辑处理
    try:
        service = Service()
        data = service.delete(data)
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 0,
            'message': str(e),
            'data': data
        })


@variable.route('/api/v1/update',methods=['POST'])
def api_v1_update():
    # post请求
    data = request.get_json()
    # 参数校验
    if 'id' not in data or not data['id']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters _id',
            'data': data
        })
    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters type',
            'data': data
        })

    if 'team' not in data or not data['team']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters key',
            'data': data
        })
    if 'project' not in data or not data['project']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters key',
            'data': data
        })
    if 'name' not in data or not data['name']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters name',
            'data': data
        })
    if 'value' not in data or not data['value']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters value',
            'data': data
        })

    # 业务逻辑处理
    try:
        service = Service()
        data = service.update(data)
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': str(e),
            'data': data
        })

@variable.route('/api/v1/create',methods=['POST'])
def api_v1_create():
    # post请求
    data = request.get_json()
    # 参数校验
    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters type',
            'data': data
        })

    if 'team' not in data or not data['team']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters key',
            'data': data
        })
    if 'project' not in data or not data['project']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters key',
            'data': data
        })
    if 'name' not in data or not data['name']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters name',
            'data': data
        })
    if 'value' not in data or not data['value']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters value',
            'data': data
        })

    # 业务逻辑处理
    try:
        service = Service()
        data = service.create(data)
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': str(e),
            'data': data
        })
# get请求
@variable.route('/api/v1/search')
def api_v1_search():
    data = request.values.to_dict()
    # 参数校验
    if 'type' not in data or not data['type']:
        return jsonify({
            'status':400,
            'message':'invalid parameters type',
            'data':data
        })

    # if 'team' not in data or not data['team']:
    #     return jsonify({
    #         'status':400,
    #         'message':'invalid parameters team',
    #         'data':data
    #     })

    # 业务逻辑处理
    try:
        service = Service()
        data = service.search(data)
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': str(e),
            'data': data
        })

@variable.route('/api/v1/aggregate',methods=['POST'])
def api_v1_aggregate():
    # post请求
    data = request.get_json()
    # 参数校验
    if 'type' not in data or not data['type']:
        return jsonify({
            'status':400,
            'message':'invalid parameters type',
            'data':data
        })

    if 'key' not in data or not data['key']:
        return jsonify({
            'status':400,
            'message':'invalid parameters key',
            'data':data
        })

    # 业务逻辑处理
    service = Service()
    data = service.aggregate(data)
    print(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })


@variable.route('/api/v1/debug',methods=['POST'])
def api_v1_debug():
    # post请求
    data = request.get_json()
    # 参数校验
    if 'mock' not in data or not data['mock']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters mock',
            'data': data
        })

    if 'snippet' not in data or not data['snippet']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters snippet',
            'data': data
        })

    # 业务逻辑处理
    try:
        service = Service()
        data = service.debug(data)
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': str(e),
            'data': data
        })


@variable.route('/api/v1/save',methods=['POST'])
def api_v1_save():
    # post请求
    data = request.get_json()
    # 参数校验
    if 'mock' not in data or not data['mock']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters mock',
            'data': data
        })

    if 'snippet' not in data or not data['snippet']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameters snippet',
            'data': data
        })

    # 业务逻辑处理
    try:
        service = Service()
        data = service.save(data)
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': str(e),
            'data': data
        })