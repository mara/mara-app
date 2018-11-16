// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

// eslint-disable-next-line no-global-assign
parcelRequire = (function (modules, cache, entry, globalName) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports, this);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [function (require, module) {
      module.exports = exports;
    }, {}];
  };

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (entry.length) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(entry[entry.length - 1]);

    // CommonJS
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = mainExports;

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
     define(function () {
       return mainExports;
     });

    // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }

  // Override the current require with this new one
  return newRequire;
})({"../components/table/index.scss":[function(require,module,exports) {

},{}],"../components/table/index.js":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

require("./index.scss");

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var Table =
/*#__PURE__*/
function () {
  function Table() {
    _classCallCheck(this, Table);
  }

  _createClass(Table, null, [{
    key: "floatMaraTableHeaders",
    // floats all mara table headers
    value: function floatMaraTableHeaders() {
      $('.mara-table-float-header').floatThead({
        top: 60,
        position: 'absolute'
      });
    } // when the page layout drastically changes,
    // then the floating headers need to be re-positioned

  }, {
    key: "reflowMaraTableHeaders",
    value: function reflowMaraTableHeaders() {
      $('.mara-table-float-header').floatThead('reflow');
    }
  }]);

  return Table;
}();

exports.default = Table;
window.floatMaraTableHeaders = Table.floatMaraTableHeaders;
window.reflowMaraTableHeaders = Table.reflowMaraTableHeaders;
},{"./index.scss":"../components/table/index.scss"}],"../components/alert/index.js":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

require("./index.scss");

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var Alert =
/*#__PURE__*/
function () {
  function Alert() {
    _classCallCheck(this, Alert);
  }

  _createClass(Alert, null, [{
    key: "showAlert",
    // adds an alert to the bottom of the page
    value: function showAlert(message, category) {
      var $alerts = document.getElementById('alerts');
      var $alert = document.createElement('div');
      $alert.classList.add('alert', 'alert--hidden', "alert-".concat(category), "alert-dismissible");
      $alert.innerHTML = "\n            <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n              <span aria-hidden=\"true\">&times;</span>\n            </button>\n            ".concat(message, "\n        ");
      $alerts.appendChild($alert);
      setTimeout(function () {
        $alert.classList.remove('alert--hidden');
      }, 1000);
    }
  }]);

  return Alert;
}();

exports.default = Alert;
},{"./index.scss":"../components/table/index.scss"}],"../js/content-loader.js":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _table = _interopRequireDefault(require("../components/table"));

var _alert = _interopRequireDefault(require("../components/alert"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var ContentLoader =
/*#__PURE__*/
function () {
  function ContentLoader() {
    _classCallCheck(this, ContentLoader);
  }

  _createClass(ContentLoader, null, [{
    key: "loadAndReplace",
    value: function loadAndReplace(containerId, url, divHeightKey) {
      var $container = document.getElementById(containerId);
      fetch(url).then(function (response) {
        return response.text();
      }).then(function (content) {
        $container.innerHTML = content;

        _table.default.reflowMaraTableHeaders();
      }).catch(function (error) {
        _alert.default.showAlert("\"".concat(error, "\" while fetching \"<a href=\"").concat(url, "\">").concat(url, "</a>\""), 'danger');

        $container.innerHTML = '<span class="fa fa-bug"></span>';
      });
    }
  }]);

  return ContentLoader;
}();

exports.default = ContentLoader;
window.loadContentAsynchronously = ContentLoader.loadAndReplace;
},{"../components/table":"../components/table/index.js","../components/alert":"../components/alert/index.js"}],"../components/card/index.js":[function(require,module,exports) {
"use strict";

require("./index.scss");
},{"./index.scss":"../components/table/index.scss"}],"../js/window.js":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var Window =
/*#__PURE__*/
function () {
  function Window() {
    _classCallCheck(this, Window);
  }

  _createClass(Window, null, [{
    key: "triggerResize",
    value: function triggerResize() {
      var _ref = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {},
          _ref$delay = _ref.delay,
          delay = _ref$delay === void 0 ? 300 : _ref$delay;

      setTimeout(function () {
        window.dispatchEvent(new Event('resize'));
      }, delay);
    }
  }]);

  return Window;
}();

exports.default = Window;
},{}],"../components/navigation/index.js":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

require("./index.scss");

var _window = _interopRequireDefault(require("../../js/window"));

var _filters = _interopRequireDefault(require("../filters"));

var _alert = _interopRequireDefault(require("../alert"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// the nav entry that matches the current page uri best
var currentNavigationEntry;

var Navigation =
/*#__PURE__*/
function () {
  function Navigation() {
    _classCallCheck(this, Navigation);
  }

  _createClass(Navigation, null, [{
    key: "expandNavigation",
    // expands the navigation sidebar
    value: function expandNavigation() {
      $('#mara-navigation .mara-nav-entry.visible:not(.level-1)').css('height', '') // reset height if it was left over from a previous slide action
      .show(0);
      var $body = $('body');
      $body.addClass('show-navigation');

      if (currentNavigationEntry) {
        currentNavigationEntry[0].scrollIntoView(false);
      }

      if (window.matchMedia('(max-width: 1280px)').matches) {
        _filters.default.collapseFilters();
      }

      document.querySelector('.js-page-header__menu').classList.add('page-header__menu--open');

      _window.default.triggerResize();
    } // collapses the navigation side bar

  }, {
    key: "collapseNavigation",
    value: function collapseNavigation() {
      var $body = $('body');
      $body.removeClass('show-navigation');
      document.querySelector('.js-page-header__menu').classList.remove('page-header__menu--open');

      _window.default.triggerResize();
    } // expands or collapses the navigation side bar

  }, {
    key: "toggleNavigation",
    value: function toggleNavigation(event) {
      var $body = $('body');

      if ($body.hasClass('show-navigation')) {
        Navigation.collapseNavigation();
      } else {
        Navigation.expandNavigation();
      }
    } // expands and highlights the navigation entry that matches an uri best

  }, {
    key: "highlightNavigationEntry",
    value: function highlightNavigationEntry() {
      var uri = window.location.pathname + window.location.search + window.location.hash; // find all navigation entries that match the request uri, take the longest (most specific) match

      var matchingUris = $('#mara-navigation .mara-nav-entry > a').map(function (_, el) {
        return $(el).attr('href');
      }).filter(function (_, href) {
        return uri.startsWith(href);
      }).sort(function (a, b) {
        return b.length - a.length;
      });

      if (matchingUris.length) {
        var longestUri = matchingUris[0];
        currentNavigationEntry = $("#mara-navigation a[href=\"".concat(longestUri, "\"]")).parent();
        currentNavigationEntry.siblings().removeClass('highlighted');
        currentNavigationEntry.addClass('highlighted').addClass('visible').addClass('expanded');
        currentNavigationEntry.parentsUntil('#mara-navigation').addClass('expanded').addClass('highlighted').addClass('visible').children('div').addClass('visible');
      }
    } // expands or collapses a navigation entry

  }, {
    key: "toggleNavigationEntry",
    value: function toggleNavigationEntry(a) {
      var $a = $(a);

      if ($a.parent().hasClass('expanded')) {
        $a.parent().removeClass('expanded');
        $a.siblings().removeClass('visible') // .css('height', '') // reset height if it was left over from a previous slide action
        .slideUp({
          queue: true
        });
      } else {
        // expand entry
        $a.parent().siblings().parent().find('.expanded > a').each(function () {
          $(this).parent().removeClass('expanded');
          $(this).siblings().removeClass('visible') // .css('height', '') // reset height if it was left over from a previous slide action
          .slideUp({
            queue: true
          });
        });
        $a.parent().addClass('expanded');
        $a.siblings().addClass('visible') // .css('height', '') // reset height if it was left over from a previous slide action
        .slideDown({
          queue: true
        });
      }
    }
  }, {
    key: "loadContent",
    value: function loadContent() {
      var url = '/mara-app/navigation-bar';
      $.ajax({
        url: url,
        success: Navigation.updateContent,
        error: function error(_, textStatus, errorThrown) {
          var message = "<span class=\"fa fa-bug\"></span>\n            ".concat(textStatus, " while fetching <a href=\"").concat(url, "\">").concat(url, "</a>: ").concat(errorThrown);

          _alert.default.showAlert(message, 'danger');

          $('#mara-navigation').empty().append('<div class="fa fa-bug"> </div>');
        }
      });
    }
  }, {
    key: "updateContent",
    value: function updateContent(content) {
      $('#mara-navigation').empty().append(content).fadeIn(500); // enable tooltips

      $('[data-toggle="tooltip"]').tooltip({
        boundary: 'window'
      }); // highlight navigation entry for current uri

      Navigation.highlightNavigationEntry(); // on navigation entries navigate within a page, also update the navigation

      window.onhashchange = function () {
        Navigation.highlightNavigationEntry();
        Navigation.collapseNavigation();
      }; // store navigation in localstorage


      localStorage.setItem('navigation-bar', content);
    }
  }]);

  return Navigation;
}();

exports.default = Navigation;
$(document).ready(function () {
  Navigation.loadContent();
});
window.toggleNavigationEntry = Navigation.toggleNavigationEntry;
window.toggleNavigation = Navigation.toggleNavigation;
},{"./index.scss":"../components/table/index.scss","../../js/window":"../js/window.js","../filters":"../components/filters/index.js","../alert":"../components/alert/index.js"}],"../components/filters/index.js":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

require("./index.scss");

var _navigation = _interopRequireDefault(require("../navigation"));

var _window = _interopRequireDefault(require("../../js/window"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var Filters =
/*#__PURE__*/
function () {
  function Filters() {
    _classCallCheck(this, Filters);
  }

  _createClass(Filters, null, [{
    key: "toggleFilters",
    value: function toggleFilters() {
      if ($('body').hasClass('show-filters')) {
        Filters.collapseFilters();
      } else {
        Filters.expandFilters();
      }
    }
  }, {
    key: "collapseFilters",
    value: function collapseFilters() {
      $('body').removeClass('show-filters');

      _window.default.triggerResize();
    }
  }, {
    key: "expandFilters",
    value: function expandFilters() {
      $('body').addClass('show-filters');

      if (window.matchMedia('(max-width: 1280px)').matches) {
        _navigation.default.collapseNavigation();
      }

      _window.default.triggerResize();
    }
  }]);

  return Filters;
}();

exports.default = Filters;
window.toggleFilters = Filters.toggleFilters;
},{"./index.scss":"../components/table/index.scss","../navigation":"../components/navigation/index.js","../../js/window":"../js/window.js"}],"../components/header/index.js":[function(require,module,exports) {
"use strict";

require("./index.scss");
},{"./index.scss":"../components/table/index.scss"}],"../components/layout/index.js":[function(require,module,exports) {
"use strict";

require("./index.scss");
},{"./index.scss":"../components/table/index.scss"}],"../components/main/index.js":[function(require,module,exports) {
"use strict";

require("./index.scss");
},{"./index.scss":"../components/table/index.scss"}],"../components/**/index.js":[function(require,module,exports) {
module.exports = {
  "alert": require("./../alert/index.js"),
  "card": require("./../card/index.js"),
  "filters": require("./../filters/index.js"),
  "header": require("./../header/index.js"),
  "layout": require("./../layout/index.js"),
  "main": require("./../main/index.js"),
  "navigation": require("./../navigation/index.js"),
  "table": require("./../table/index.js")
};
},{"./../alert/index.js":"../components/alert/index.js","./../card/index.js":"../components/card/index.js","./../filters/index.js":"../components/filters/index.js","./../header/index.js":"../components/header/index.js","./../layout/index.js":"../components/layout/index.js","./../main/index.js":"../components/main/index.js","./../navigation/index.js":"../components/navigation/index.js","./../table/index.js":"../components/table/index.js"}],"mara.js":[function(require,module,exports) {
"use strict";

require("../js/content-loader");

require("../scss/base.scss");

require("../components/**/index.js");
},{"../js/content-loader":"../js/content-loader.js","../scss/base.scss":"../components/table/index.scss","../components/**/index.js":"../components/**/index.js"}]},{},["mara.js"], null)
//# sourceMappingURL=/mara.map