$(document).ready(function() {
    var navigationUrl = '/mara-app/navigation-bar';

    $.ajax({
        url: navigationUrl,
        success: function(navigationEntries) {
            $('#mara-navigation')
                .empty()
                .append(navigationEntries)
                .fadeIn(500);

            // enable tooltips
            $('[data-toggle="tooltip"]').tooltip({ boundary: 'window' });

            // highlight navigation entry for current uri
            highlightNavigationEntry(
                window.location.pathname +
                    window.location.search +
                    window.location.hash
            );

            // on navigation entries navigate within a page, also update the navigation
            window.onhashchange = function() {
                highlightNavigationEntry(
                    window.location.pathname +
                        window.location.search +
                        window.location.hash
                );
                collapseNavigation();
            };

            // store navigation in localstorage
            localStorage.setItem('navigation-bar', navigationEntries);
        },
        error: function(xhr, textStatus, errorThrown) {
            showAlert(
                textStatus +
                    ' while fetching "<a href="' +
                    navigationUrl +
                    '">' +
                    navigationUrl +
                    '</a>": ' +
                    errorThrown,
                'danger'
            );
            $('#mara-navigation')
                .empty()
                .append('<div class="fa fa-bug"> </div>');
        }
    });

    // float headers of all tables with class `.mara-table`
    floatMaraTableHeaders();
});

// the nav entry that matches the current page uri best
var currentNavigationEntry;

// expands and highlights the navigation entry that matches an uri best
function highlightNavigationEntry(uri) {
    // find all navigation entries that match the request uri, take the longest (most specific) match
    var matchingUris = $('#mara-navigation .mara-nav-entry > a')
        .map(function() {
            return $(this).attr('href');
        })
        .filter(function(x) {
            return uri.startsWith(this);
        });

    if (matchingUris) {
        var longestUri = matchingUris.sort(function(a, b) {
            return b.length - a.length;
        })[0];

        currentNavigationEntry = $(
            '#mara-navigation .mara-nav-entry > a[href="' + longestUri + '"]'
        ).parent();

        currentNavigationEntry.siblings().removeClass('highlighted');
        currentNavigationEntry.addClass('highlighted');
        currentNavigationEntry.addClass('visible');
        currentNavigationEntry.addClass('expanded');
        currentNavigationEntry
            .parentsUntil('#mara-navigation')
            .addClass('expanded');
        currentNavigationEntry
            .parentsUntil('#mara-navigation')
            .addClass('highlighted');
        currentNavigationEntry
            .parentsUntil('#mara-navigation')
            .addClass('visible');
        currentNavigationEntry
            .parentsUntil('#mara-navigation')
            .children('div')
            .addClass('visible');
    }

    $('#mara-navigation .mara-nav-entry.visible:not(.level-1)')
        .css('height', '') // reset height if it was left over from a previous slide action
        .show(0);
    if (currentNavigationEntry) {
        currentNavigationEntry[0].scrollIntoView(false);
    }
}

// expands or collapses a navigation entry
function toggleNavigationEntry(a) {
    if (
        $(a)
            .parent()
            .hasClass('expanded')
    ) {
        // collapse entry
        $(a)
            .parent()
            .removeClass('expanded');
        $(a)
            .siblings()
            .removeClass('visible')
            .css('height', '') // reset height if it was left over from a previous slide action
            .slideUp({ queue: true });
    } else {
        // expand entry
        $(a)
            .parent()
            .siblings()
            .parent()
            .find('.expanded > a')
            .each(function() {
                $(this)
                    .parent()
                    .removeClass('expanded');
                $(this)
                    .siblings()
                    .removeClass('visible')
                    .css('height', '') // reset height if it was left over from a previous slide action
                    .slideUp({ queue: true });
            });

        $(a)
            .parent()
            .addClass('expanded');
        $(a)
            .siblings()
            .addClass('visible')
            .css('height', '') // reset height if it was left over from a previous slide action
            .slideDown({ queue: true });
    }
}

// adds an alert to the bottom of the page
function showAlert(message, category) {
    alert = $(
        '<div style="display:none" class="alert alert-' +
            category +
            ' alert-dismissible" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
            '<span aria-hidden="true">&times;</span>' +
            '</button>' +
            message +
            '</div>'
    );
    $('#alerts').append(alert);
    alert.fadeIn(2000);
}

// floats all mara table headers
function floatMaraTableHeaders() {
    $('.mara-table-float-header').floatThead({
        top: 60,
        position: 'absolute'
    });
}

// when the page layout drastically changes,
// then the floating headers need to be re-positioned
function reflowMaraTableHeaders() {
    $('.mara-table-float-header').floatThead('reflow');
}

// Replaces the content of the element with id `containerId` with the result of calling url
function loadContentAsynchronously(containerId, url, divHeightKey) {
    $.ajax({
        url: url,
        error: function(xhr, textStatus, errorThrown) {
            var icon = '<span class="fa fa-bug"> </span> ';
            showAlert(
                icon +
                    textStatus +
                    ' while fetching "<a href="' +
                    url +
                    '">' +
                    url +
                    '</a>": ' +
                    errorThrown,
                'danger'
            );
            $('#' + containerId)
                .empty()
                .append(icon);
        },
        success: function(data) {
            $('#' + containerId).css('height', '');
            $('#' + containerId)
                .empty()
                .hide()
                .append(data)
                .fadeIn(300);
            reflowMaraTableHeaders();
            if (divHeightKey) {
                localStorage.setItem(
                    divHeightKey,
                    $('#' + containerId).height()
                );
            }
        }
    });
}

(window => {
    class Cookies {
        static set(cookieName, cookieValue, daysToExpire = 30) {
            const date = new Date();
            date.setTime(date.getTime() + daysToExpire * 24 * 60 * 60 * 1000);

            document.cookie =
                cookieName +
                '=' +
                cookieValue +
                '; path=/; expires=' +
                date.toGMTString();
        }

        static get(cookieName) {
            const name = cookieName + '=';
            const allCookieArray = document.cookie.split(';');

            for (let i = 0; i < allCookieArray.length; i++) {
                const temp = allCookieArray[i].trim();
                if (temp.indexOf(name) == 0)
                    return temp.substring(name.length, temp.length);
            }
            return '';
        }

        static remove(cookieName) {
            const date = new Date();
            date.setTime(date.getTime() - 1000 * 60 * 60 * 24);

            const expires = 'path=/; expires=' + date.toGMTString();
            window.document.cookie = cookieName + '=' + '; ' + expires;
        }
    }

    window.Cookies = Cookies;
})(window);

(window => {
    class Layout {
        constructor({ $element }) {
            this.$element = $element;
            this.Cookies = window.Cookies;

            if (this.Cookies.get('mara-navigation')) {
                this._expandNavigation();
            }

            if (this.Cookies.get('mara-filters')) {
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

            this.Cookies.remove('mara-filters');

            this.triggerResize();
        }

        _expandFilters() {
            this.$element.classList.add('layout--show-filters');

            if (window.matchMedia('(max-width: 1280px)').matches) {
                this._collapseNavigation();
            }

            this.Cookies.set('mara-filters', 'open');

            this.triggerResize();
        }

        _expandNavigation() {
            this.$element.classList.add('layout--show-navigation');

            if (window.matchMedia('(max-width: 1280px)').matches) {
                this._collapseFilters();
            }

            this.Cookies.set('mara-navigation', 'open');

            document
                .querySelector('.js-page-header__menu')
                .classList.add('page-header__menu--open');

            this.triggerResize();
        }

        _collapseNavigation() {
            this.$element.classList.remove('layout--show-navigation');

            this.Cookies.remove('mara-navigation');

            document
                .querySelector('.js-page-header__menu')
                .classList.remove('page-header__menu--open');

            this.triggerResize();
        }

        toggleNavigation() {
            if (this.$element.classList.contains('layout--show-navigation')) {
                this._collapseNavigation();
            } else {
                this._expandNavigation();
            }
        }

        triggerResize({ delay = 300 } = {}) {
            setTimeout(() => {
                window.dispatchEvent(new Event('resize'));
            }, delay);
        }
    }

    const initLayout = id => {
        return new Layout({ $element: document.getElementById(id) });
    };

    window.Layout = initLayout;
})(window);
