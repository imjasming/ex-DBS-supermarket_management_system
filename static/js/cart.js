let queryUrl = '/data/cart';
let params = [
    {
        field: 'rid',
        title: 'rid',
        visible: false
    }, {
        field: 'bname',
        title: '分店',
        sortable: true
    }, {
        field: 'pname',
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
        field: 'pid',
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
    let bn = row["bname"];
    let count = row['num'];
    let pid = row['pid'];
    let price = row['price'];
    let rid = row['rid'];

    $.ajax({
        url: buyUrl + "?pid=" + pid + '&bname=' + bn + '&num=' + count + '&rid=' + rid,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']' + row['PName'] + ", 数量：" + count + ",购买成功,花费：" + price * count;
            $('#modalMsg').text('购买成功');
            $('#myModal').modal('show');
            $table.bootstrapTable('load', data);
        },
        error: function (error) {
            if (error['status'] == '500' || error['status'] == '503' || error['status'] == '501') {
                document.getElementById("msg").innerText = "服务器数据异常";
                $('#modalMsg').text('服务器数据异常');
                $('#myModal').modal('show');
            } else {
                document.getElementById("msg").innerText = "未登录，跳转到登录界面。。。";
                $('#modalMsg').text('未登录，跳转到登录界面。。。');
                $('#myModal').modal('show');
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
            $('#modalMsg').text('删除成功');
            $('#myModal').modal('show');
            $table.bootstrapTable('load', data);
        },
        error: function (error) {
            if (error['status'] == '401') {
                document.getElementById("msg").innerText = "未登录，跳转到登录界面。。。";
                $('#modalMsg').text('未登录，跳转到登录界面。。。');
                $('#myModal').modal('show');
                redirectTo('/login')
            } else if (error['status'] == '405') {
                document.getElementById("msg").innerText = "您无权操作";
                $('#modalMsg').text('您无权操作');
                $('#myModal').modal('show');
            } else {
                document.getElementById("msg").innerText = "服务器数据异常";
                $('#modalMsg').text('服务器数据异常');
                $('#myModal').modal('show');
            }
        }
    })
}
