let params = [
    {
        field: 'name',
        title: '姓名',
        sortable: true
    }, {
        field: 'sid',
        title: '员工编号',
        visible: true,
    }, {
        field: 'position',
        title: '职位',
        sortable: true
    }, {
        field: 'tel',
        title: '联系方式',
        sortable: true,
    }, {
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '操作',
        sortable: true,
        formatter: operation,
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
            $('#modalMsg').text("申请已提交");
            $('#myModal').modal('show');
            $table.bootstrapTable('load', data);
        },
        error: function (error) {
            if (error['status'] == '401') {
                document.getElementById("msg").innerText = "未登录，跳转到登录界面。。。";
                $('#modalMsg').text("未登录，跳转到登录界面。。。");
                $('#myModal').modal('show');
                redirectTo('/login')
            } else if (error['status'] == '405') {
                document.getElementById("msg").innerText = "您无权操作";
                $('#modalMsg').text("您无权操作");
                $('#myModal').modal('show');
            } else if (error['status'] == '500') {
                document.getElementById("msg").innerText = "已提交的申请";
                $('#modalMsg').text("已提交的申请");
                $('#myModal').modal('show');
            } else {
                document.getElementById("msg").innerText = "服务器数据异常";
                $('#modalMsg').text("服务器数据异常");
                $('#myModal').modal('show');
            }
        }
    })
}
