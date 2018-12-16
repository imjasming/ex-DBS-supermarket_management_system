let queryUrl = '/data/product';
let pageSize = 20;

let $table = $('#product').bootstrapTable({
    url: queryUrl,                      //请求后台的URL（*）
    method: 'GET',                      //请求方式（*）
    //toolbar: '#toolbar',              //工具按钮用哪个容器
    //striped: true,                      //是否显示行间隔色
    cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
    pagination: true,                   //是否显示分页（*）
    sortable: true,                     //是否启用排序
    // sortClass:'pid',
    sortOrder: "asc",                   //排序方式
    sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
    pageNumber: 1,                      //初始化加载第一页，默认第一页,并记录
    pageSize: pageSize,                     //每页的记录行数（*）
    pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
    search: true,                      //是否显示表格搜索
    searchTimeOut: 10000,
    searchOnEnterKey: true,
    singleSelect: true,
    strictSearch: false,
    showColumns: true,                  //是否显示所有的列（选择显示的列）
    showPaginationSwitch: true,
    showRefresh: true,                  //是否显示刷新按钮
    trimOnSearch: true,
    minimumCountColumns: 2,             //最少允许的列数
    clickToSelect: true,                //是否启用点击选中行
    //height: 500,                      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
    uniqueId: "row",                     //每一行的唯一标识，一般为主键列
    //showToggle: true,                   //是否显示详细视图和列表视图的切换按钮
    cardView: false,                    //是否显示详细视图
    detailView: false,                  //是否显示父子表
    //上传服务器的参数
    queryParams: function (params) {
        //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
        var temp = {
            rows: params.limit,                         //页面大小
            page: (params.offset / params.limit) + 1,   //页码
            sort: params.sort,      //排序列名
            sortOrder: params.order //排位命令（desc，asc）
        };
        return temp;
    },
    columns: [{
        checkbox: true,
        visible: true                  //是否显示复选框
    }, {
        field: 'BName',
        title: '分店',
        sortable: true
    }, {
        field: 'PName',
        title: '产品名称',
        sortable: true
    }, {
        field: 'price',
        title: '价格',
        sortable: true,
    }, {
        field: 'num',
        title: '库存',
        sortable: true,
    }, {
        field: 'PID',
        title: 'pid',
        visible: false,
    }, {
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '购买',
        formatter: operation,
    }
    ]/*,
        onLoadSuccess: function () {
        },
        onLoadError: function () {
            showTips("data loading fail");
        },
        onDblClickRow: function (row, $element) {
            var id = row.ID;
            EditViewById(id, 'view');
        },*/
});

function operation(value, row, index) {
    //let selected = JSON.stringify($table.bootstrapTable('getRowByUniqueId', row));
    let r = $table.bootstrapTable('getRowByUniqueId', index);
    let max = row['num'];
    return '<div class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required id="num" placeholder="count" min="1" max="' + max + '"></div><button id="buy" onclick="buy(this)" type="submit" class="btn btn-primary buy" data-row="' + row['row'] + '">Buy</button></div>';
}

let uid = document.getElementById('user_id').getAttribute("data-id");
let buyUrl = "/buy";

function buy(e) {
    let a = e.getAttribute("data-row");
    let row = $table.bootstrapTable('getRowByUniqueId', parseInt(a));
    let bn = row["BName"];
    let num = row['num'];
    let pid = row['Pid'];

    $.ajax({
        url: buyUrl + '?uid=' + uid + "&pid=" + pid + '&bname=' + bn + '&num=' + num,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            document.getElementById("msg").innerText = "购买成功";
            $table.bootstrapTable('load', data);
        },
        error: function (data) {
            location = '/login';
        }
    })
};
