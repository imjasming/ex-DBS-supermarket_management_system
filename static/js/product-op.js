let params = [
    {
        field: 'BName',
        title: '分店',
        sortable: true
    }, {
        field: 'PName',
        title: '产品名称',
        sortable: true
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
        field: 'price',
        title: '价格',
        sortable: true,
        formatter: operation,
    },];

let queryUrl = '/data/product-op';
$table = createTable(queryUrl, params, '#table');

function operation(value, row, index) {
    let rowId = row['row'];
    let price = row['price'];
    return '<div class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required step="0.1" id="num' + rowId + '" placeholder="' + price + '" min="0" value="' + price + '"' + ' data-old="' + price + '"></div><button id="change" onclick="change(this)" type="submit" class="btn btn-primary change" data-row="' + rowId + '">Save</button></div>';
}

let url = '/change/price';

function change(e) {
    let rowId = e.getAttribute("data-row");
    let input = $('#num' + rowId);
    let oldPrice = input.data("old");
    let newPrice = input.val();
    let row = getTableRow(e);
    let bname = row['BName'];
    let pid = row['Pid'];

    $.ajax({
        url: url + '?pid=' + pid + '&bname=' + bname + '&price=' + newPrice,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']' + row['PName'] + "的价格修改成功(原价" + oldPrice + ")";
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
