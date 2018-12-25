let queryUrl = '/data/product';
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
        field: 'price',
        title: '价格',
        sortable: true,
    }, {
        field: 'num',
        title: '库存',
        sortable: true,
    }, {
        field: 'kind',
        title: '分类',
        visible: true,
    }, {
        field: 'Pid',
        title: 'pid',
        visible: false,
    }, {
        field: 'row',
        title: 'row',
        visible: false,
    }, {
        title: '操作',
        formatter: operation,
    }];

$table = createTable(queryUrl, params, '#table');

function operation(value, row, index) {
    //let selected = JSON.stringify($table.bootstrapTable('getRowByUniqueId', row));
    let max = row['num'];
    let rowId = row['row'];
    let e = document.getElementById('user_id');
    let right = null;
    try {
        right = e.getAttribute("data-right");
    }catch (e) {
        right = null
    }

    if (max <= 0 || (right != 'customer' && right != null)) {
        return '<div disabled class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button disabled id="buy" onclick="addToCart(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">添加至购物车</button></div>';
    }
    return '<div class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button id="buy" onclick="addToCart(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">添加至购物车</button></div>';
}

//let uid = document.getElementById('user_id').getAttribute("data-id");
let addUrl = "/add/cart";

function addToCart(e) {
    let a = e.getAttribute("data-row");
    let row = $table.bootstrapTable('getRowByUniqueId', parseInt(a));
    let bn = row["BName"];
    let num = row['num'];
    let count = parseInt($('#num' + a).val());
    let pid = row['Pid'];
    let price = row['price'];
    let pname = row['PName'];

    if (isNaN(count) || count > num || count <= 0) {
        document.getElementById("msg").innerText = "请输入合理的购买数量";
        return
    }

    $.ajax({
        url: addUrl + "?pid=" + pid + '&bname=' + bn + '&num=' + count + '&pname=' + pname + '&price=' + price,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']添加至购物车成功';
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
