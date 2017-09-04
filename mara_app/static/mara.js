$(document).ready(function () {
    // enable tooltips
    $('[data-toggle="tooltip"]').tooltip();

    if (!isTouchDevice) {
        $('#mara-navigation').mouseover(expandNavigation);
        $('#mara-navigation').mouseleave(collapseNavigation);
    }

    // highlight navigation entry for current uri
    highlightNavigationEntry(window.location.pathname + window.location.search + window.location.hash);
});

// the nav entry that matches the current page uri best
var currentNavigationEntry;

// expands and highlights the navigation entry that matches an uri best
function highlightNavigationEntry(uri) {

    // find all navigation entries that match the request uri, take the longest (most specific) match
    var matchingUris = $('#mara-navigation .mara-nav-entry > a')
        .map(function () {
            return $(this).attr('href');
        })
        .filter(function (x) {
            return uri.startsWith(this);
        });

    if (matchingUris) {
        var longestUri = matchingUris.sort(function (a, b) {
            return b.length - a.length
        })[0];

        currentNavigationEntry = $('#mara-navigation .mara-nav-entry > a[href="' + longestUri + '"]').parent();

        currentNavigationEntry.siblings().removeClass('highlighted');
        currentNavigationEntry.addClass('highlighted');
        currentNavigationEntry.addClass('visible');
        currentNavigationEntry.addClass('expanded');
        currentNavigationEntry.parentsUntil('#mara-navigation').addClass('expanded');
        currentNavigationEntry.parentsUntil('#mara-navigation').addClass('highlighted');
        currentNavigationEntry.parentsUntil('#mara-navigation').addClass('visible');
        currentNavigationEntry.parentsUntil('#mara-navigation').children('div').addClass('visible');
    }
}

// expands or collapses a navigation entry
function toggleNavigationEntry(a) {
    if ($(a).parent().hasClass('expanded')) {
        $(a).parent().removeClass('expanded');
        $(a).siblings().removeClass('visible')
            .css('height', '') // reset height if it was left over from a previous slide action
            .slideUp({queue: true});
    } else {
        $(a).parent().addClass('expanded');
        $(a).siblings().addClass('visible')
            .css('height', '') // reset height if it was left over from a previous slide action
            .slideDown({queue: true});
    }
}


// expands the navigation sidebar
function expandNavigation() {
    if ($('body').hasClass('navigation-collapsed')) {
        $('body').removeClass('navigation-collapsed');
        $('#mara-navigation .mara-nav-entry.visible:not(.level-1)')
            .css('height', '') // reset height if it was left over from a previous slide action
            .show(0);
        if (currentNavigationEntry) {
            currentNavigationEntry[0].scrollIntoView();
        }
    }
}

// collapses the navigation side bar
function collapseNavigation() {
    $('body').addClass('navigation-collapsed');
    $('#mara-navigation .mara-nav-entry.level-2.visible').slideUp({queue: true});
}

// expands or collapses the navigation side bar
function toggleNavigation() {
    if ($('body').hasClass('navigation-collapsed')) {
        expandNavigation();
    } else {
        collapseNavigation();
    }
}


// adds an alert to the bottom of the page
function showAlert(message, category) {
    alert = $('<div style="display:none" class="alert alert-' + category + ' alert-dismissible" role="alert">' +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
        '<span aria-hidden="true">&times;</span>' +
        '</button>' + message + '</div>');
    $('#alerts').append(alert);
    alert.fadeIn(2000);
}

