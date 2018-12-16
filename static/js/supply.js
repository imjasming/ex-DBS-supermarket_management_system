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
    let max = row['num'];
    let rowId = row['row'];
    if (max <= 0) {
        return '<div class="d-flex flex-row"> <div class="col"> <input disabled type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button disabled id="buy" onclick="buy(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">Buy</button></div>';
    }
    return '<div class="d-flex flex-row"> <div class="col"> <input type="number" class="form-control" name="num" required id="num' + rowId + '" placeholder="count" min="1" max="' + max + '"></div><button id="buy" onclick="buy(this)" type="submit" class="btn btn-primary buy" data-row="' + rowId + '">Buy</button></div>';
}

function validation() {

}
