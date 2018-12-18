let params = [
    {
        field: 'rid',
        title: '记录id',
        sortable: false
    }, /*{
        field: 'time',
        title: '时间',
        visible: true,
    }, */{
        field: 'bname',
        title: '分店',
        visible: true,
    }, {
        field: 'pname',
        title: '产品名称',
        sortable: true
    }, {
        field: 'num',
        title: '数量',
        sortable: true,
    }, {
        field: 'price',
        title: '价格',
        visible: true,
    }, {
        field: 'status',
        title: '状态',
        visible: true,
    }, {
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '操作',
        sortable: false,
        formatter: operation,
    },];

let params2 = [
    {
        field: 'rid',
        title: '记录id',
        sortable: false
    }, /*{
        field: 'time',
        title: '时间',
        visible: true,
    }, */{
        field: 'bname',
        title: '分店',
        visible: true,
    }, {
        field: 'sname',
        title: '员工名字',
        sortable: true
    }, {
        field: 'status',
        title: '状态',
        visible: true,
    }, {
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '操作',
        sortable: true,
        formatter: operation,
    },];

let queryUrl = '/data/request-goods';
let queryUrl2 = '/data/request-staff';
$table1 = createTable(queryUrl, params, '#table');

let $table2 = null;
setTimeout(function () {
    $table2 = createTable(queryUrl2, params2, '#table2');
}, 1500);

function operation(value, row, index) {
    let rowId = row['row'];
    let status = row['status'];
    if (status == '待处理') {
        if (row['pname'] != undefined) {
            return '<div class="d-flex flex-row"><button id="allow" onclick="allow(this)" type="submit" class="btn btn-primary allow" data-table="1" data-row="' + rowId + '">同意</button><button id="allow" onclick="deny(this)" type="submit" class="btn btn-primary allow" data-table="1" data-row="' + rowId + '">拒绝</button></div>';
        } else {
            return '<div class="d-flex flex-row"><button id="allow" onclick="allow(this)" type="submit" class="btn btn-primary allow" data-table="2" data-row="' + rowId + '">同意</button><button id="allow" onclick="deny(this)" type="submit" class="btn btn-primary allow" data-table="2" data-row="' + rowId + '">拒绝</button></div>';
        }
    } else {
        if (row['pname'] != undefined) {
            return '<div class="d-flex flex-row"><button hidden id="allow" onclick="remove(this)" type="submit" class="btn btn-primary allow" data-table="1" data-row="' + rowId + '">删除</button></div>';
        } else {
            return '<div class="d-flex flex-row"><button hidden id="allow" onclick="remove(this)" type="submit" class="btn btn-primary allow" data-table="2" data-row="' + rowId + '">删除</button></div>';
        }
    }
}

let url1 = '/response/staff';
let url2 = '/response/goods';

function allow(e) {
    action(e, "同意")
}

function deny(e) {
    action(e, "不同意")
}

function action(e, status) {
    var table = e.getAttribute('data-table');
    if (table == '1') {
        table = $table1
    } else {
        table = $table2
    }
    let row = getTableRowBytable(e, table);
    let rid = row['rid'];

    if (row['pname'] == undefined) {
        sendToServer(url1 + '?rid=' + rid + '&status=' + status, '操作成功', table)
    } else {
        sendToServer(url2 + '?rid=' + rid + '&status=' + status, '操作成功', table)
    }
}

function sendToServer(url, successMsg, table) {
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']' + successMsg;
            table.bootstrapTable('load', data);
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
