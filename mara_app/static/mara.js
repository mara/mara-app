$(document).ready(function () {
    if (!isTouchDevice) {
        $('#mara-navigation').mouseover(expandNavigation);
        $('#mara-navigation').mouseleave(collapseNavigation);
    }

    var navigationUrl = '/mara-app/navigation-bar';
    $.ajax({
        url: navigationUrl,
        success: function (navigationEntries) {
            $('#mara-navigation').empty().append(navigationEntries).fadeIn(500);

            // enable tooltips
            $('[data-toggle="tooltip"]').tooltip();

            // highlight navigation entry for current uri
            highlightNavigationEntry(window.location.pathname + window.location.search + window.location.hash);

            window.onhashchange = function () {
                highlightNavigationEntry(window.location.pathname + window.location.search + window.location.hash);
            };

            localStorage.setItem('navigation-bar', navigationEntries);
        },
        error: function (xhr, textStatus, errorThrown) {
            showAlert(textStatus + ' while fetching "<a href="' + navigationUrl + '">' + navigationUrl + '</a>": ' + errorThrown,
                'danger');
            $('#mara-navigation').empty().append('<div class="fa fa-bug"> </div>');
        },
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
        error: function (xhr, textStatus, errorThrown) {
            var icon = '<span class="fa fa-bug"> </span> ';
            showAlert(icon + textStatus + ' while fetching "<a href="' + url + '">' + url + '</a>": ' + errorThrown,
                'danger');
            $('#' + containerId).empty().append(icon);
        },
        success: function (data) {
            $('#' + containerId).css('height', '');
            $('#' + containerId).empty().hide().append(data).fadeIn(300);
            reflowMaraTableHeaders();
            if (divHeightKey) {
                localStorage.setItem(divHeightKey, $('#' + containerId).height());
            }
        }
    });
}

