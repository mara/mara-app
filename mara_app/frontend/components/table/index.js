import './index.scss';

export default class Table {
    // floats all mara table headers
    static floatMaraTableHeaders() {
        $('.mara-table-float-header').floatThead({
            top: 60,
            position: 'absolute'
        });
    }

    // when the page layout drastically changes,
    // then the floating headers need to be re-positioned
    static reflowMaraTableHeaders() {
        $('.mara-table-float-header').floatThead('reflow');
    }
}

window.floatMaraTableHeaders = Table.floatMaraTableHeaders;
window.reflowMaraTableHeaders = Table.reflowMaraTableHeaders;
