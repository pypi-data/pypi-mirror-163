(self["webpackChunkservicex_dashboard"] = self["webpackChunkservicex_dashboard"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _ServiceXLogo_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./ServiceXLogo.svg */ "./style/ServiceXLogo.svg");
/* harmony import */ var _ServiceXLogo_svg__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_ServiceXLogo_svg__WEBPACK_IMPORTED_MODULE_3__);
// Imports




var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()((_ServiceXLogo_svg__WEBPACK_IMPORTED_MODULE_3___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\r\n    See the JupyterLab Developer Guide for useful CSS Patterns:\r\n\r\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\r\n*/\r\n\r\n.servicex-logo{\r\n    background-image: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ");\r\n}\r\n\r\n#setting-editor .servicex-logo {\r\n    background-repeat: no-repeat;\r\n    background-size: 100%;\r\n    background-position: center;\r\n}\r\n\r\na{\r\n    color: #007bff;\r\n}\r\n\r\n#firstLastButton{\r\n    border-radius: 0px;\r\n    background-color: white;\r\n    color: #007bff;\r\n    border: 0.5px solid gray;\r\n    width: 20px;\r\n    height: 22.5px;\r\n}\r\n\r\n#firstLastButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#firstLastButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n#paginationButton{\r\n    border-radius: 0px;\r\n    width: 20px;\r\n    height: 22.5px;\r\n    font-size: 12px;\r\n    text-align: center;\r\n}\r\n\r\n#paginationButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#paginationButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n.my-apodWidget {\r\n    display: flex;\r\n    flex-direction: column;\r\n    overflow: auto;\r\n}\r\n\r\n#requestTable{\r\n    background-color: white;\r\n    border-collapse: collapse;\r\n    border: 0.5px solid gray;\r\n}\r\n\r\ntr:nth-child(even) {\r\n    background-color: white;\r\n}\r\n\r\ntr:nth-child(odd) {\r\n    background-color: lightgray;\r\n}\r\n\r\nth{\r\n    background-color: #343a40;\r\n    padding: 5px 10px;\r\n    border: 0.5px solid gray;\r\n    font-weight: bold;\r\n    color: white;\r\n    text-align: left;\r\n    height: 36.67px;\r\n    width: 48.35px;\r\n    position: sticky;\r\n    top: 0\r\n}\r\n\r\ntd{\r\n    padding: 5px 10px;\r\n    border: 0.5px solid gray;\r\n    text-align: top;\r\n    width: 48.35px;\r\n}\r\n\r\n#header{\r\n    background-color:  white;\r\n    font-size: 20px;\r\n    font-weight: 500;\r\n    margin: 7.5px 0px;\r\n    float: left;\r\n}\r\n\r\n#cancelButton{\r\n    background-color: #dc3545;\r\n    border: none;\r\n    color: white;\r\n    border-radius: 0.25rem;\r\n    font-size: 12px;\r\n    width : 45px;\r\n    height: 24.75px;\r\n    text-align: center;\r\n}\r\n\r\n#cancelButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#cancelButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n.progressBar{\r\n    background-color: #007bff;\r\n    display: block;\r\n    height: 15px;\r\n    border-radius: 6px;\r\n    text-align: center;\r\n    color: white;\r\n    font-size: 12.5px;\r\n    transition: 1s;\r\n}\r\n\r\n.progressBarStripes{\r\n    background-size: 1rem 1rem;\r\n    background-image: linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent);\r\n    animation: slide 1s linear infinite;\r\n}\r\n\r\n@keyframes slide{\r\n   from {\r\n    background-position: 15px,0\r\n   }    \r\n   to {\r\n    background-position: 0,0 \r\n   }\r\n}\r\n\r\n/*\r\n#inputButton{\r\n    width: 20px;\r\n    height: 10px;\r\n    margin: 5px 0 0 5px;\r\n    border: 0.5px solid gray;\r\n    font-size: 10px;\r\n}\r\n\r\n#inputButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n#inputButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24);\r\n}*/\r\n\r\n.dropdown{\r\n    position: relative;\r\n    display: inline-block\r\n}\r\n\r\n.dropdownButton{\r\n    width: 400px;\r\n    height: 20px;\r\n    border: 0.5px solid gray;\r\n    background: white;\r\n    text-align: left;\r\n    font-size: 12px;\r\n}\r\n\r\n.dropdownButton:hover{\r\n    cursor: pointer;\r\n}\r\n\r\n.dropdownDiv{\r\n    display: none;\r\n    /*position: absolute;*/\r\n    background-color: #f1f1f1;\r\n    min-width: 400px;\r\n    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\r\n    z-index: 1;\r\n}\r\n\r\n.dropdownDiv a{\r\n    color: black;\r\n    padding: 12px 16px;\r\n    text-decoration: none;\r\n    display: block;\r\n    background-color: white;\r\n    font-size: 12px;\r\n}\r\n\r\n.dropdownDiv a:hover{\r\n    background-color: lightgray;\r\n}\r\n\r\n.show{\r\n    display: block;\r\n}\r\n\r\n#exit{\r\n    width: 15px;\r\n    height: 15px;\r\n    float: right;\r\n    border: none;\r\n    border-radius: 0px;\r\n    background-color: #dc3545;\r\n    color: white;\r\n}\r\n\r\n#exit:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#exit:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;;;;CAIC;;AAED;IACI,yDAAuC;AAC3C;;AAEA;IACI,4BAA4B;IAC5B,qBAAqB;IACrB,2BAA2B;AAC/B;;AAEA;IACI,cAAc;AAClB;;AAEA;IACI,kBAAkB;IAClB,uBAAuB;IACvB,cAAc;IACd,wBAAwB;IACxB,WAAW;IACX,cAAc;AAClB;;AAEA;IACI,sBAAsB;IACtB;AACJ;;AAEA;IACI,sBAAsB;IACtB,eAAe;AACnB;;AAEA;IACI,kBAAkB;IAClB,WAAW;IACX,cAAc;IACd,eAAe;IACf,kBAAkB;AACtB;;AAEA;IACI,sBAAsB;IACtB;AACJ;;AAEA;IACI,sBAAsB;IACtB,eAAe;AACnB;;AAEA;IACI,aAAa;IACb,sBAAsB;IACtB,cAAc;AAClB;;AAEA;IACI,uBAAuB;IACvB,yBAAyB;IACzB,wBAAwB;AAC5B;;AAEA;IACI,uBAAuB;AAC3B;;AAEA;IACI,2BAA2B;AAC/B;;AAEA;IACI,yBAAyB;IACzB,iBAAiB;IACjB,wBAAwB;IACxB,iBAAiB;IACjB,YAAY;IACZ,gBAAgB;IAChB,eAAe;IACf,cAAc;IACd,gBAAgB;IAChB;AACJ;;AAEA;IACI,iBAAiB;IACjB,wBAAwB;IACxB,eAAe;IACf,cAAc;AAClB;;AAEA;IACI,wBAAwB;IACxB,eAAe;IACf,gBAAgB;IAChB,iBAAiB;IACjB,WAAW;AACf;;AAEA;IACI,yBAAyB;IACzB,YAAY;IACZ,YAAY;IACZ,sBAAsB;IACtB,eAAe;IACf,YAAY;IACZ,eAAe;IACf,kBAAkB;AACtB;;AAEA;IACI,sBAAsB;IACtB;AACJ;;AAEA;IACI,sBAAsB;IACtB,eAAe;AACnB;;AAEA;IACI,yBAAyB;IACzB,cAAc;IACd,YAAY;IACZ,kBAAkB;IAClB,kBAAkB;IAClB,YAAY;IACZ,iBAAiB;IACjB,cAAc;AAClB;;AAEA;IACI,0BAA0B;IAC1B,kLAAkL;IAClL,mCAAmC;AACvC;;AAEA;GACG;IACC;GACD;GACA;IACC;GACD;AACH;;AAEA;;;;;;;;;;;;;;;;;EAiBE;;AAEF;IACI,kBAAkB;IAClB;AACJ;;AAEA;IACI,YAAY;IACZ,YAAY;IACZ,wBAAwB;IACxB,iBAAiB;IACjB,gBAAgB;IAChB,eAAe;AACnB;;AAEA;IACI,eAAe;AACnB;;AAEA;IACI,aAAa;IACb,sBAAsB;IACtB,yBAAyB;IACzB,gBAAgB;IAChB,4CAA4C;IAC5C,UAAU;AACd;;AAEA;IACI,YAAY;IACZ,kBAAkB;IAClB,qBAAqB;IACrB,cAAc;IACd,uBAAuB;IACvB,eAAe;AACnB;;AAEA;IACI,2BAA2B;AAC/B;;AAEA;IACI,cAAc;AAClB;;AAEA;IACI,WAAW;IACX,YAAY;IACZ,YAAY;IACZ,YAAY;IACZ,kBAAkB;IAClB,yBAAyB;IACzB,YAAY;AAChB;;AAEA;IACI,sBAAsB;IACtB;AACJ;;AAEA;IACI,sBAAsB;IACtB,eAAe;AACnB","sourcesContent":["/*\r\n    See the JupyterLab Developer Guide for useful CSS Patterns:\r\n\r\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\r\n*/\r\n\r\n.servicex-logo{\r\n    background-image: url(ServiceXLogo.svg);\r\n}\r\n\r\n#setting-editor .servicex-logo {\r\n    background-repeat: no-repeat;\r\n    background-size: 100%;\r\n    background-position: center;\r\n}\r\n\r\na{\r\n    color: #007bff;\r\n}\r\n\r\n#firstLastButton{\r\n    border-radius: 0px;\r\n    background-color: white;\r\n    color: #007bff;\r\n    border: 0.5px solid gray;\r\n    width: 20px;\r\n    height: 22.5px;\r\n}\r\n\r\n#firstLastButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#firstLastButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n#paginationButton{\r\n    border-radius: 0px;\r\n    width: 20px;\r\n    height: 22.5px;\r\n    font-size: 12px;\r\n    text-align: center;\r\n}\r\n\r\n#paginationButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#paginationButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n.my-apodWidget {\r\n    display: flex;\r\n    flex-direction: column;\r\n    overflow: auto;\r\n}\r\n\r\n#requestTable{\r\n    background-color: white;\r\n    border-collapse: collapse;\r\n    border: 0.5px solid gray;\r\n}\r\n\r\ntr:nth-child(even) {\r\n    background-color: white;\r\n}\r\n\r\ntr:nth-child(odd) {\r\n    background-color: lightgray;\r\n}\r\n\r\nth{\r\n    background-color: #343a40;\r\n    padding: 5px 10px;\r\n    border: 0.5px solid gray;\r\n    font-weight: bold;\r\n    color: white;\r\n    text-align: left;\r\n    height: 36.67px;\r\n    width: 48.35px;\r\n    position: sticky;\r\n    top: 0\r\n}\r\n\r\ntd{\r\n    padding: 5px 10px;\r\n    border: 0.5px solid gray;\r\n    text-align: top;\r\n    width: 48.35px;\r\n}\r\n\r\n#header{\r\n    background-color:  white;\r\n    font-size: 20px;\r\n    font-weight: 500;\r\n    margin: 7.5px 0px;\r\n    float: left;\r\n}\r\n\r\n#cancelButton{\r\n    background-color: #dc3545;\r\n    border: none;\r\n    color: white;\r\n    border-radius: 0.25rem;\r\n    font-size: 12px;\r\n    width : 45px;\r\n    height: 24.75px;\r\n    text-align: center;\r\n}\r\n\r\n#cancelButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#cancelButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n.progressBar{\r\n    background-color: #007bff;\r\n    display: block;\r\n    height: 15px;\r\n    border-radius: 6px;\r\n    text-align: center;\r\n    color: white;\r\n    font-size: 12.5px;\r\n    transition: 1s;\r\n}\r\n\r\n.progressBarStripes{\r\n    background-size: 1rem 1rem;\r\n    background-image: linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent);\r\n    animation: slide 1s linear infinite;\r\n}\r\n\r\n@keyframes slide{\r\n   from {\r\n    background-position: 15px,0\r\n   }    \r\n   to {\r\n    background-position: 0,0 \r\n   }\r\n}\r\n\r\n/*\r\n#inputButton{\r\n    width: 20px;\r\n    height: 10px;\r\n    margin: 5px 0 0 5px;\r\n    border: 0.5px solid gray;\r\n    font-size: 10px;\r\n}\r\n\r\n#inputButton:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}\r\n\r\n#inputButton:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24);\r\n}*/\r\n\r\n.dropdown{\r\n    position: relative;\r\n    display: inline-block\r\n}\r\n\r\n.dropdownButton{\r\n    width: 400px;\r\n    height: 20px;\r\n    border: 0.5px solid gray;\r\n    background: white;\r\n    text-align: left;\r\n    font-size: 12px;\r\n}\r\n\r\n.dropdownButton:hover{\r\n    cursor: pointer;\r\n}\r\n\r\n.dropdownDiv{\r\n    display: none;\r\n    /*position: absolute;*/\r\n    background-color: #f1f1f1;\r\n    min-width: 400px;\r\n    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\r\n    z-index: 1;\r\n}\r\n\r\n.dropdownDiv a{\r\n    color: black;\r\n    padding: 12px 16px;\r\n    text-decoration: none;\r\n    display: block;\r\n    background-color: white;\r\n    font-size: 12px;\r\n}\r\n\r\n.dropdownDiv a:hover{\r\n    background-color: lightgray;\r\n}\r\n\r\n.show{\r\n    display: block;\r\n}\r\n\r\n#exit{\r\n    width: 15px;\r\n    height: 15px;\r\n    float: right;\r\n    border: none;\r\n    border-radius: 0px;\r\n    background-color: #dc3545;\r\n    color: white;\r\n}\r\n\r\n#exit:active{\r\n    transform: scale(0.98);\r\n    box-shadow: 1.5px 1px 20px 1px rgba(0, 0, 0, 0.24)\r\n}\r\n\r\n#exit:hover{\r\n    filter: grayscale(20%);\r\n    cursor: pointer;\r\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./style/ServiceXLogo.svg":
/*!********************************!*\
  !*** ./style/ServiceXLogo.svg ***!
  \********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "111565f29c8d4815f6304fc77ceff32322763413208c08499404e209c098256e.svg";

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ })

}]);
//# sourceMappingURL=style_index_js.bec232aca6ae67249d5e.js.map