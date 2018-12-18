let params = [
    {
        field: 'time',
        title: '时间',
        sortable: true
    }, {
        field: 'uname',
        title: '用户',
        visible: false,
    }, {
        field: 'pname',
        title: '商品名称',
        sortable: true
    }, {
        field: 'price',
        title: '单价',
        sortable: true,
    }, {
        field: 'num',
        title: '数量',
        visible: false,
    }, {
        field: 'total',
        title: '总价',
        visible: true,
    }, {
        field: 'row',
        title: 'row',
        visible: false,
    },];

let queryUrl = '/data/record';
$table = createTable(queryUrl, params, '#table');