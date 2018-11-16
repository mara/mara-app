import './index.scss';

import Window from '../../js/window';
import Filters from '../filters';
import Alert from '../alert';

// the nav entry that matches the current page uri best
var currentNavigationEntry;

export default class Navigation {
    // expands the navigation sidebar
    static expandNavigation() {
        $('#mara-navigation .mara-nav-entry.visible:not(.level-1)')
            .css('height', '') // reset height if it was left over from a previous slide action
            .show(0);

        const $body = $('body');
        $body.addClass('show-navigation');

        if (currentNavigationEntry) {
            currentNavigationEntry[0].scrollIntoView(false);
        }

        if (window.matchMedia('(max-width: 1280px)').matches) {
            Filters.collapseFilters();
        }

        document
            .querySelector('.js-page-header__menu')
            .classList.add('page-header__menu--open');

        Window.triggerResize();
    }

    // collapses the navigation side bar
    static collapseNavigation() {
        const $body = $('body');
        $body.removeClass('show-navigation');

        document
            .querySelector('.js-page-header__menu')
            .classList.remove('page-header__menu--open');

        Window.triggerResize();
    }

    // expands or collapses the navigation side bar
    static toggleNavigation(event) {
        const $body = $('body');

        if ($body.hasClass('show-navigation')) {
            Navigation.collapseNavigation();
        } else {
            Navigation.expandNavigation();
        }
    }

    // expands and highlights the navigation entry that matches an uri best
    static highlightNavigationEntry() {
        const uri =
            window.location.pathname +
            window.location.search +
            window.location.hash;

        // find all navigation entries that match the request uri, take the longest (most specific) match
        var matchingUris = $('#mara-navigation .mara-nav-entry > a')
            .map((_, el) => $(el).attr('href'))
            .filter((_, href) => uri.startsWith(href))
            .sort((a, b) => b.length - a.length);

        if (matchingUris.length) {
            const longestUri = matchingUris[0];

            currentNavigationEntry = $(
                `#mara-navigation a[href="${longestUri}"]`
            ).parent();

            currentNavigationEntry.siblings().removeClass('highlighted');

            currentNavigationEntry
                .addClass('highlighted')
                .addClass('visible')
                .addClass('expanded');

            currentNavigationEntry
                .parentsUntil('#mara-navigation')
                .addClass('expanded')
                .addClass('highlighted')
                .addClass('visible')
                .children('div')
                .addClass('visible');
        }
    }

    // expands or collapses a navigation entry
    static toggleNavigationEntry(a) {
        const $a = $(a);

        if ($a.parent().hasClass('expanded')) {
            $a.parent().removeClass('expanded');

            $a.siblings()
                .removeClass('visible')
                // .css('height', '') // reset height if it was left over from a previous slide action
                .slideUp({ queue: true });
        } else {
            // expand entry
            $a.parent()
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
                        // .css('height', '') // reset height if it was left over from a previous slide action
                        .slideUp({ queue: true });
                });

            $a.parent().addClass('expanded');

            $a.siblings()
                .addClass('visible')
                // .css('height', '') // reset height if it was left over from a previous slide action
                .slideDown({ queue: true });
        }
    }

    static loadContent() {
        const url = '/mara-app/navigation-bar';

        $.ajax({
            url,
            success: Navigation.updateContent,
            error(_, textStatus, errorThrown) {
                const message = `<span class="fa fa-bug"></span>
            ${textStatus} while fetching <a href="${url}">${url}</a>: ${errorThrown}`;

                Alert.showAlert(message, 'danger');

                $('#mara-navigation')
                    .empty()
                    .append('<div class="fa fa-bug"> </div>');
            }
        });
    }

    static updateContent(content) {
        $('#mara-navigation')
            .empty()
            .append(content)
            .fadeIn(500);

        // enable tooltips
        $('[data-toggle="tooltip"]').tooltip({ boundary: 'window' });

        // highlight navigation entry for current uri
        Navigation.highlightNavigationEntry();

        // on navigation entries navigate within a page, also update the navigation
        window.onhashchange = () => {
            Navigation.highlightNavigationEntry();
            Navigation.collapseNavigation();
        };

        // store navigation in localstorage
        localStorage.setItem('navigation-bar', content);
    }
}

$(document).ready(() => {
    Navigation.loadContent();
});

window.toggleNavigationEntry = Navigation.toggleNavigationEntry;
window.toggleNavigation = Navigation.toggleNavigation;
