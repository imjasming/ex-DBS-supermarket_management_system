let queryUrl = '/data/cart';
let params = [
    {
        field: 'rid',
        title: 'rid',
        sortable: false
    }, {
        field: 'BName',
        title: '分店',
        sortable: false
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
        title: '数量',
        sortable: true,
    }, {
        field: 'Pid',
        title: 'pid',
        visible: false,
    }, {
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '添加至购物车',
        formatter: operation,
    }];

$table = createTable(queryUrl, params, '#table');

function operation(value, row, index) {
    let rowId = row['row'];
    return '<div class="d-flex flex-row"><button id="allow" onclick="buy(this)" type="submit" class="btn btn-primary allow" data-table="2" data-row="' + rowId + '">购买</button><button id="allow" onclick="rm(this)" type="submit" class="btn btn-primary allow" data-table="2" data-row="' + rowId + '">删除</button></div>';
}

//let uid = document.getElementById('user_id').getAttribute("data-id");
let buyUrl = "/buy";

function buy(e) {
    let a = e.getAttribute("data-row");
    let row = $table.bootstrapTable('getRowByUniqueId', parseInt(a));
    let bn = row["BName"];
    let count = row['num'];
    let pid = row['Pid'];
    let price = row['price'];

    $.ajax({
        url: buyUrl + "?pid=" + pid + '&bname=' + bn + '&num=' + count,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']' + row['PName'] + ", 数量：" + count + ",购买成功,花费：" + price * count;
            $table.bootstrapTable('load', data);
        },
        error: function (error) {
            if (error['status'] == '500' || error['status'] == '503' || error['status'] == '501') {
                document.getElementById("msg").innerText = "服务器数据异常";
            } else {
                document.getElementById("msg").innerText = "未登录，跳转到登录界面。。。";
                redirectTo('/login')
            }
        }
    })
}

let removeUrl = '/remove';

function rm(e) {
    let a = e.getAttribute("data-row");
    let row = $table.bootstrapTable('getRowByUniqueId', parseInt(a));
    let rid = row['rid'];

    $.ajax({
        url: removeUrl + '?rid=' + rid,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']删除成功';
            $table.bootstrapTable('load', data);
        },
        error: function (error) {
            if (error['status'] == '401') {
                document.getElementById("msg").innerText = "未登录，跳转到登录界面。。。";
                redirectTo('/login')
            } else if (error['status'] == '405') {
                document.getElementById("msg").innerText = "您无权操作";

            } else {
                document.getElementById("msg").innerText = "服务器数据异常";
            }
        }
    })
}