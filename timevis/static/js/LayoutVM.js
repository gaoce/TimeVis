// A View Model to control layout information interface
define(['jquery', 'knockout', 'Exp', 'Layout', 'Factor', 'Level', 'utils'],
    function($, ko, Exp, Layout, Factor, Level, utils) {
        return function() {
            var self = this;

            // Urls for API
            self.exp_url = '/api/v2/experiment';
            self.layout_url = '/api/v2/layout';

            // Array for Experiment obj and current obj
            self.experiments = ko.observableArray();
            self.current_exp = ko.observable();

            // Layout
            self.layouts = ko.observableArray();
            self.current_layout = ko.observable();
            // Disable layout selection if no current_exp is available
            self.disable_layout = ko.computed(function() {
                return self.current_exp()? false: true
            });

            // Factor
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

            // Handsontable obj
            self.table;

            self.disable_update = ko.computed(function() {
                if (!self.current_exp() || !self.current_layout() || !self.current_factor()){
                    return true;
                }
            });

            self.get_exps = function() {
                $.ajax({
                    url: self.exp_url,
                    type: "GET",
                    success: function(data) {
                        self.experiments(
                            $.map(data.experiment, function(exp){
                                return new Exp(exp);
                            })
                        );
                    }  /* success */
                });  /* ajax */
            };

            self.current_exp.subscribe(function(exp) {
                if (!exp) {
                    // Disable all following functionalities if exp is null
                    self.current_layout(null);
                    self.current_factor(null);
                    return;
                }

                // Update factor prototypes
                self.factors_prty = $.map(exp.factors(), function(fac) {
                    return {id: fac.id, name: fac.name()};
                });

                // Update self.layouts
                self.get_layouts(exp.id);

                // Create the table
                if (self.table) {
                    // Destory existing table
                    self.table.destroy();
                }

                var container = document.getElementById('layout');
                var settings = new utils.createSetting(exp.well());
                self.table = new Handsontable(container, settings);

                // Set current layout to empty one
                self.current_layout(self.layouts()[0]);
                self.current_factor(null);
            });

            // Retrieve layout info given an experiment id
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

                        self.layouts.sort(self.sort_layout);

                        // Create a place holder layout for adding new
                        self.layouts.unshift(
                            new Layout({factors: self.factors_prty})
                        );
                    }
                });
            }

            self.current_layout.subscribe(function(layout){
                if (layout) {
                    self.factors(layout.factors());
                }
            });

            // Construct an array used by Handsontable based on factor levels
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

            // Flash information on the page
            self.flash = function(msg) {
                $("#layout-notice").html(msg).show().delay(2000).fadeOut();
            }

            self.sort_layout = function(left, right) {
                return left.dispName == right.dispName ? 0 :
                    (left.dispName < right.dispName ? -1 : 1)
            };

            self.validate = function() {
                if (self.current_layout().name() === '') {
                    self.flash('Error: invalid layout name!');
                    return 0;
                }
            };

            self.update_factor = function() {
                // Validate fields on the page
                if (self.validate() === 0){ return };

                var data = self.decodeData(self.table.getData());
                var layout = ko.toJS(self.current_layout);
                var factor ={id: self.current_factor().id,
                            name: self.current_factor().name(),
                            levels: data};
                layout.factors = [factor];
                // Maybe we should move the following 3 lines into ajax
                self.current_factor().levels($.map(data, function(d) {
                    return new Level(d);
                }));

                // New exp's ID is 0
                var http_method = self.current_layout().id === 0 ? 'POST' : 'PUT';

                $.ajax({
                    url: self.layout_url + '?eid=' + self.current_exp().id,
                    type: http_method,
                    dataType: "json",
                    data: JSON.stringify({layout: [layout]}),
                    contentType: "application/json; charset=utf-8",
                    success: function(data){
                        self.flash('Succeed!');
                    },
                    error: function(data){
                        self.flash('Error: '+
                                $.parseJSON(data.responseText)['Error']);
                    }
                });
            };

            // Initialize
            self.get_exps();
        };
    }
);
