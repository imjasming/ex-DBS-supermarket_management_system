let queryUrl = '/data/product';
let params = [
    {
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
    }];

$table = createTable(queryUrl, params, '#table');

function operation(value, row, index) {
    //let selected = JSON.stringify($table.bootstrapTable('getRowByUniqueId', row));
    let max = row['num'];
    let rowId = row['row'];
    if (max <= 0) {
        return '<div class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button disabled id="buy" onclick="buy(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">Buy</button></div>';
    }
    return '<div class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button id="buy" onclick="buy(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">Buy</button></div>';
}

let uid = document.getElementById('user_id').getAttribute("data-id");
let buyUrl = "/buy";

function buy(e) {
    let a = e.getAttribute("data-row");
    let row = $table.bootstrapTable('getRowByUniqueId', parseInt(a));
    let bn = row["BName"];
    let num = row['num'];
    let count = parseInt($('#num' + a).val());
    let pid = row['Pid'];
    let price = row['price'];

    if (isNaN(count) || count > num || num <= 0) {
        document.getElementById("msg").innerText = "请输入合理的购买数量";
        return
    }

    $.ajax({
        url: buyUrl + '?uid=' + uid + "&pid=" + pid + '&bname=' + bn + '&num=' + count,
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
