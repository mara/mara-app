import './index.scss';

import Navigation from '../navigation';
import Window from '../../js/window';

export default class Filters {
    static toggleFilters() {
        if ($('body').hasClass('show-filters')) {
            Filters.collapseFilters();
        } else {
            Filters.expandFilters();
        }
    }

    static collapseFilters() {
        $('body').removeClass('show-filters');

        Window.triggerResize();
    }

    static expandFilters() {
        $('body').addClass('show-filters');

        if (window.matchMedia('(max-width: 1280px)').matches) {
            Navigation.collapseNavigation();
        }

        Window.triggerResize();
    }
}

window.toggleFilters = Filters.toggleFilters;
