import './index.scss';

import Window from '../../js/window';

import Cookies from 'js-cookie';

export default class Layout {
    constructor({ $element }) {
        this.$element = $element;

        if (Cookies.get('mara-navigation')) {
            this._expandNavigation();
        }

        if (Cookies.get('mara-filters')) {
            this._expandFilters();
        }

        this._initEventHandlers();
    }

    _initEventHandlers() {
        window.toggleNavigation = this.toggleNavigation.bind(this);
        window.toggleFilters = this.toggleFilters.bind(this);
    }

    toggleFilters() {
        if (this.$element.classList.contains('layout--show-filters')) {
            this._collapseFilters();
        } else {
            this._expandFilters();
        }
    }

    _collapseFilters() {
        this.$element.classList.remove('layout--show-filters');

        Cookies.remove('mara-filters');

        Window.triggerResize();
    }

    _expandFilters() {
        this.$element.classList.add('layout--show-filters');

        if (window.matchMedia('(max-width: 1280px)').matches) {
            this._collapseNavigation();
        }

        Cookies.set('mara-filters', 'open');

        Window.triggerResize();
    }

    _expandNavigation() {
        this.$element.classList.add('layout--show-navigation');

        if (window.matchMedia('(max-width: 1280px)').matches) {
            this._collapseFilters();
        }

        Cookies.set('mara-navigation', 'open');

        document
            .querySelector('.js-page-header__menu')
            .classList.add('page-header__menu--open');

        Window.triggerResize();
    }

    _collapseNavigation() {
        this.$element.classList.remove('layout--show-navigation');

        Cookies.remove('mara-navigation');

        document
            .querySelector('.js-page-header__menu')
            .classList.remove('page-header__menu--open');

        Window.triggerResize();
    }

    toggleNavigation() {
        if (this.$element.classList.contains('layout--show-navigation')) {
            this._collapseNavigation();
        } else {
            this._expandNavigation();
        }
    }
}

export const initLayout = id => {
    return new Layout({ $element: document.getElementById(id) });
};

window.Layout = initLayout;
