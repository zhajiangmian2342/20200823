from flask import Blueprint, render_template, request, jsonify
from interface.service import Service

interface = Blueprint('interface',
          __name__,
          static_folder='static',
          template_folder='templates',
          url_prefix='/interface')


@interface.route('/create')
def index():
    return render_template('interface.html')


@interface.route('/list')
def list():
    return render_template('interface_list.html')


@interface.route('/suite/list')
def suite_list():
    return render_template('interface_suite.html')


@interface.route('/api/v1/list')
def api_v1_list():
    data = request.values.to_dict()
    service = Service()
    data = service.interface_list(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })


@interface.route('/edit/<id>')
def edit(id):

    return render_template('interface_edit.html')


@interface.route('/api/v1/delete',methods=['POST'])
def api_v1_delete():
    data = request.get_json()
    id_list = data.get('id_list')
    if not id_list:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter id_list',
            'data': data
        })
    service = Service()
    data = service.interface_delete(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })


@interface.route('/api/v1/debug', methods=['POST'])
def api_v1_debug():
    # debug按钮就相当于send,发起请求

    data = request.get_json()
    print(data)
    # 参数校验
    method = data.get('method')
    if not method:
        return jsonify({
            'status': 400,
            'message':'invalid parameter method',
            'data':data
        })
    url = data.get('url')
    if not url:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter url',
            'data': data
        })
    # 获取数据主要目的：发起请求
    service = Service()
    # 包含响应值的data
    # 做变量替换
    data = service.run(data)

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })


@interface.route('/api/v1/save',methods=['POST'])
def api_v1_save():
    data = request.get_json()
    print(data)
    # 参数校验
    method = data.get('method')
    if not method:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter method',
            'data': data
        })
    url = data.get('url')
    if not url:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter url',
            'data': data
        })
    # 获取数据主要目的：发起请求
    service = Service()
    # 保存data数据到数据库里面
    id = service.save_cases(data)


    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': id

    })


@interface.route('/api/v1/team_and_project')
def api_v1_team_and_project():
    data = request.values.to_dict()
    service = Service()
    data = service.interface_team_and_project()
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })

@interface.route('/api/v1/search')
def api_v1_search():
    data = request.values.to_dict()
    id = data.get('id')
    if not id:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter id',
            'data': data
        })

    service = Service()
    # 保存data数据到数据库里面
    data = service.interface_search(data)

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })

@interface.route('/api/v1/update',methods=['POST'])
def api_v1_update():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter id',
            'data': data
        })

    service = Service()
    # 保存data数据到数据库里面
    data = service.interface_update(data)

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })


# 保存测试套件到数据库
@interface.route('/api/v1/suite',methods=['POST'])
def api_v1_suite():
    data = request.get_json()
    cases = data.get('cases')
    if not cases:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter cases',
            'data': data
        })
    team= data.get('team')
    if not team:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter team',
            'data': data
        })
    project = data.get('project')
    if not project:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter project',
            'data': data
        })

    service = Service()
    # 保存data数据到数据库里面
    data = service.save_suite(data)

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })

# /interface/api/v1/suite/list

@interface.route('/api/v1/suite/list')
def api_v1_suite_list():
    data = request.values.to_dict()
    service = Service()
    data = service.suite_list(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })


@interface.route('/api/v1/suite/delete',methods=['POST'])
def api_v1_suite_delete():
    data = request.get_json()
    id_list = data.get('id_list')
    if not id_list:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter id_list',
            'data': data
        })
    service = Service()
    data = service.suite_delete(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data
    })

# /interface/api/v1/trigger

@interface.route('/api/v1/trigger')
def api_v1_trigger():
    data = request.values.to_dict()
    service = Service()
    data = service.trigger(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': data

    })










