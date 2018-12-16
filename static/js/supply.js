let queryUrl = '/data/supply';
let params = [
    {
        checkbox: true,
        visible: true                  //是否显示复选框
    }, {
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
        field: 'PID',
        title: '购买',
        formatter: operation,
    }
];

$table = createTable(queryUrl, params, '#table');

function operation(value, row, index) {
    let uid = document.getElementById('user_id').getAttribute("data-id");
    let selected = JSON.stringify($table.bootstrapTable('getSelections'));
    let sid = selected['sid'];
    let max = selected['num'];
    let price = selected['price'];
    return '<form class="d-flex flex-row" action="/add?pid=' + value + '&uid=' + uid + '&price=' + price + '&sid=' + sid + '"> <div class="col"> <input type="number" class="form-control" name="num" required id="num" placeholder="count" min="1" max="' + max + '"></div><button type="submit" class="btn btn-primary">Buy</button></form>';
}

function validation() {

}
