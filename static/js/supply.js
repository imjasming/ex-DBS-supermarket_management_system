let queryUrl = '/data/supply';
let params = [
    {
        field: 'sname',
        title: '供货商',
        sortable: true
    }, {
        field: 'sid',
        title: '供货商ID',
        sortable: true
    }, {
        field: 'pname',
        title: '产品名称',
        sortable: true,
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
        visible: false,
    }, {
        field: 'pid',
        title: 'pid',
        visible: false,
    }, {
        title: '进货',
        formatter: operation,
    }
];

$table = createTable(queryUrl, params, '#table');

function operation(value, row, index) {
    let max = row['num'];
    let rowId = row['row'];
    if (max <= 0) {
        return '<div class="d-flex flex-row"> <div class="col"> <input disabled type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button disabled id="buy" onclick="addFromSupply(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">Buy</button></div>';
    }
    return '<div class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button id="buy" onclick="addFromSupply(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">Buy</button></div>';
}

let addUrl = "/add";

function addFromSupply(e) {
    let a = e.getAttribute("data-row");
    let row = $table.bootstrapTable('getRowByUniqueId', parseInt(a));
    let sid = row["sid"];
    let num = row['num'];
    let count = parseInt($('#num' + a).val());
    let pid = row['pid'];

    if (isNaN(count) || count > num || count <= 0) {
        document.getElementById("msg").innerText = "请输入合理的购买数量";
        return
    }

    $.ajax({
        url: addUrl + '?pid=' + pid + '&sid=' + sid + '&num=' + count,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            let date = new Date();
            document.getElementById("msg").innerText = '[' + date.toLocaleString() + ']' + row['sname'] + '，商品：' + row['pname'] + ", 数量：" + count + ",进货申请成功";
            $table.bootstrapTable('load', data);
        },
        error: function (error) {
            if (error['status'] == '405') {
                document.getElementById("msg").innerText = "未登录，跳转到登录界面。。。";
                redirectTo('/login')
            } else {
                document.getElementById("msg").innerText = "服务器数据异常";
            }
        }
    })
}
