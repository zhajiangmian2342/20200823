//打开网址
function browser(){
    var html = '\
    <div class="row" command="browser">\
        <label>打开:</label>\
        <input type="text" placeholder="请输入url地址">\
    </div>\
    '
    $('#cases').append(html)
}
//点击动作
function click(){
    var html = '\
        <div class="row" command="click">\
            <label>动作:</label>\
            <select>\
                <option value="click">click</option>\
            </select>\
        </div>\
        '
        $('#cases').append(html)

}


//对应着元素库，元素-查找元素的方法
function find(){
    var html = '\
    <div class="row" command="find">\
        <label>使用:</label>\
        <select>\
            <option value="xpath">xpath</option>\
            <option value="css selector">css selector</option>\
            <option value="name">name</option>\
            <option value="class name">class name</option>\
            <option value="id">id</option>\
            <option value="tag name">tag name</option>\
            <option value="link text">link text</option>\
        </select>\
        <label>参数: </label>\
        <input type="text">\
    </div>\
    '
    $('#cases').append(html)

}

//输入文本
function send(){
    var html = '\
    <div class="row" command="send">\
        <label>填写:</label>\
        <input type="text">\
    </div>\
    '
    $('#cases').append(html)

}
//等待函数
function wait(){
    var html = '\
    <div class="row" command="wait">\
        <label>填写等待时间:</label>\
        <input type="text">\
    </div>\
    '
    $('#cases').append(html)

}
//解析函数的参数，具体函数要携带哪些参数
function parse_parameters(html){
    //data = {
     //   'command':'get'，
     //   'parameter':'url'
    //}
    var  data = {}
    var command = $(html).attr("command")
    if (command == 'browser'){
        data['command'] = 'get'
        data['parameter'] = {
            'value':$(html).find('input').val()
        }
    }else if (command == 'find'){
        data['command'] = 'find'
        data['parameter'] = {
            'by':$(html).find('select').val(),
            'selector':$(html).find('input').val()
        }
    }else if (command == 'send'){
        data['command'] = 'send'
        data['parameter'] = {
            'value':$(html).find('input').val()
        }

    }else if (command == 'click'){
        data['command'] = 'click'
        data['parameter'] = {}
    }else if (command == 'wait'){
        data['command'] = 'wait'
        data['parameter'] = {
            'value':$(html).find('input').val()
        }

    }else{
        console.log('错误的html')

    }
    console.log(data)
    return data
}


//根据页面上面获取到的命令不同去运行不同的函数
//实现html的一个拼接
function add_element(){
    var command = $('#option').val()
    if (command == 'browser'){
        browser()
    }else if (command == 'find'){
        find()
    }else if (command == 'send'){
        send()
    }else if (command == 'wait'){
        wait()
    }else if(command == 'click'){
        click()
    }else{
        alert('错误的方法')
    }
}

//run的函数
function run(){
    //查看你所有的拼接的测试步骤，cases的div里面去看
    var list = $('#cases').find('div')
    var data = {
        //用例的名字
        'casename':$('#name').val(),
        //从前端收集的操作的命令
        'commands':[]
    }
    $(list).each(function(index,item){
        var command = parse_parameters(item)
        data['commands'].push(command)
    })
    console.log(data)
    var url = '/automation/api/v1/run'
    http(url,'post',data,success,error)
}
//保存的函数
function save(){
    //查看你所有的拼接的测试步骤，cases的div里面去看
    var list = $('#cases').find('div')
    var data = {
        //用例的名字
        'casename':$('#name').val(),
        //从前端收集的操作的命令
        'commands':[]
    }
    $(list).each(function(index,item){
        var command = parse_parameters(item)
        data['commands'].push(command)
    })
    console.log(data)
    var url = '/automation/api/v1/save'
    http(url,'post',data,function(data){
        alert(data['message'])
    },error)
}





$(function(){
    //点击添加，添加元素
    $('#command').click(add_element)
    // 点击run这个按钮，运行
    $('#run').click(run)
    //点击save这个按钮，保存
    $('#save').click(save)

})
