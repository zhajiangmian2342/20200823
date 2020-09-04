function init_team(){
       var url='/variable/api/v1/aggregate'
       //type指的是数据库表
       var data = {
            type : 'team',
            key: 'team'
       }
       http(url,'post',data,function(data){
        console.log(data)
        //做一个动态拼接  option拼接
        var html = ""
        for(index in data['data']){
            //html拼接
            html += '<option value="'+data['data'][index]['_id']+'">'+data['data'][index]['_id']+'</option>'
        }
        //把html追加到下team的下拉框里面
        $('#team').append(html)


       },function(data){
            console.log(data)

       })

}


$(function(){
    init_team()

})