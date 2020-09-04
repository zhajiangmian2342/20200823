
function success(data) {
    console.log(data)
}

function error(data) {
    console.log(data)
}

function http(url, method, data, success, error) {
    data = method == 'get' ? data : JSON.stringify(data)
    $.ajax({
        url: url,        //请求的服务器地址
        type: method,               //请求方法支持get，post...
        contentType: 'application/json; charset=UTF-8',  //请求的数据类型
        data: data,                  //请求携带的数据
        dataType: 'json',           //相应的数据类型
        success: success,              //成功时执行的函数
        error: error                    //失败时执行的函数
    });
}
