let params = [
    {
        field: 'rid',
        title: '记录id',
        sortable: false
    }, {
        field: 'time',
        title: '时间',
        visible: true,
    }, {
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
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '操作',
        sortable: true,
        formatter: operation1,
    },];

let params2 = [
    {
        field: 'rid',
        title: '记录id',
        sortable: false
    }, {
        field: 'time',
        title: '时间',
        visible: true,
    }, {
        field: 'bname',
        title: '分店',
        visible: true,
    }, {
        field: 'sname',
        title: '员工名字',
        sortable: true
    },{
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '操作',
        sortable: true,
        formatter: operation2,
    },];

let queryUrl = '/data/staff';
$table = createTable(queryUrl, params, '#table');

function operation(value, row, index) {
    let rowId = row['row'];
    return '<div class="d-flex flex-row"><button id="change" onclick="change(this)" type="submit" class="btn btn-primary change" data-row="' + rowId + '">申请解雇</button></div>';
}

let url = '/change/staff';

function change(e) {
    let row = getTableRow(e);
    let sid = row['sid'];

    $.ajax({
        url: url + '?sid=' + sid,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']' + row['name'] + "的解雇申请已提交，等待处理中";
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
