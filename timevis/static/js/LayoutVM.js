// A View Model to control layout information interface
define(['jquery', 'knockout', 'Exp', 'Layout', 'Factor', 'utils'], 
    function($, ko, Exp, Layout, Factor, utils) {
        return function() {
            var self = this;

            // Urls for API
            self.exp_url = '/api/v2/experiment';
            self.layout_url = '/api/v2/layout';

            // Factor (independent variables)
            self.experiments = ko.observableArray();
            self.current_exp = ko.observable();

            self.layouts = ko.observableArray();
            self.current_layout = ko.observable();
            // Disable layout selection if no current_exp is available
            self.disable_layout = ko.computed(function() {
                return self.current_exp()? false: true
            });

            self.factors = ko.observableArray();
            self.current_factor = ko.observable();
            self.disable_factor = ko.computed(function() {
                if (!self.current_exp() || !self.current_layout()) {
                    return true;
                } else {
                    return false;
                }
            });
            // Array of factor prototypes (same id and name as those in
            // current_exp().factors, but without levels)
            self.factors_prty = [];

            self.get_exps = function() {
                $.ajax({
                    url: self.exp_url,
                    type: "GET",
                    success: function(data) {
                        $.map(data.experiment, function(exp){
                            self.experiments.push(new Exp(exp));
                        });
                    }
                });
            };

            self.get_exps();

            self.get_layouts = function(eid) {
                $.ajax({
                    url: self.layout_url + '?eid=' + eid,
                    type: "GET",
                    success: function(data) {
                        // Populate layouts with returned objects
                        self.layouts(
                            $.map(data.layout, function(layout) {
                                return new Layout(layout);
                            })
                        );

                        // Create a place holder layout for adding new
                        self.layouts.unshift(
                            new Layout({factors: self.factors_prty})
                        );
                    }
                });
            }

            self.container = $('#layout')[0];
            self.table;
            self.current_exp.subscribe(function(exp) {
                if (!exp) {
                    self.current_layout(null);
                    self.current_factor(null);
                    return;
                }

                // Update factor prototypes
                self.factors_prty = $.map(exp.factors(), function(fac) {
                    return {id: fac.id, name: fac.name()};
                });
                self.get_layouts(exp.id);

                // Destory existing table
                if (self.table) {
                    self.table.destroy();
                }

                var settings = new utils.createSetting(exp.well());
                self.table = new Handsontable(self.container, settings);

                // Set current layout to empty one
                self.current_layout(self.layouts()[0]);
                self.current_factor(null);
            });

            self.current_layout.subscribe(function(layout){
                if (layout) {
                    self.factors(layout.factors());
                }
            });

            self.encodeData = function(levels) {
                var nWell = self.current_exp().well();
                if (levels.length > 0) {
                    var lvls = $.map(levels, function(level){
                        return level.value;
                    });
                } else {
                    var lvls = Array(nWell);
                }
                var ret = [];
                switch (nWell) {
                    case 96:
                        var nCol = 12;
                        break;
                    case 384:
                        var nCol = 24;
                        break;
                    default:
                        return;
                }
                var cur_arr = [];
                $.map(lvls, function(lvl, ind) {
                    cur_arr.push(lvl);
                    if ((ind + 1) % nCol === 0) {
                        ret.push(cur_arr);
                        cur_arr = [];
                    }
                });

                return ret;
            };

            self.decodeData = function(data) {
                var lvls = [];
                $.map(data, function(arr){
                    $.map(arr, function(d){
                        lvls.push(d);
                    });
                });
                switch (lvls.length) {
                    case 96:
                        var nRow = 8;
                        var nCol = 12;
                        break;
                    case 384:
                        var nRow = 16;
                        var nCol = 24;
                        break;
                    default:
                        return;
                }

                var ret = {};
                $.map(lvls, function(lvl, ind) {
                    // 1-based row and col num
                    var col = ind % nCol + 1;
                    var row = (ind - col + 1) / nCol + 1;
                    var well = String.fromCharCode(64 + row) + (col < 10 ? '0' : '') + col;
                    ret[well] = '' + lvl;
                })

                return ret;
            }

            self.current_factor.subscribe(function(factor){
                if (factor) {
                    var lvls = self.encodeData(factor.levels());
                    self.table.loadData(lvls);
                }
            });

            self.update_layout = function() {
                var data = self.decodeData(self.table.getData());
                var layout = ko.toJS(self.current_layout);
                var factor ={id: self.current_factor().id,
                            name: self.current_factor().name(),
                            levels: data};
                layout.factors = [factor];
                var method;
                if (self.current_layout().id === 0) {
                    method = "POST";
                } else {
                    method = "PUT";
                }

                $.ajax({
                    url: self.layout_url + '?eid=' + self.current_exp().id,
                    type: method,
                    dataType: "json",
                    data: JSON.stringify({layout: [layout]}),
                    contentType: "application/json; charset=utf-8",
                    success: function(data){
                    },
                    error: function(data){
                    }
                });
            };
        };
    }
);
