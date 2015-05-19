// A View Model to control layout information interface
define(['jquery', 'knockout', 'Exp', 'Layout', 'Channel', 'Plate', 'utils'],
    function($, ko, Exp, Layout, Channel, Plate, utils) {
        return function() {
            var self = this;

            // Urls for API
            self.exp_url = '/api/v2/experiment';
            self.layout_url = '/api/v2/layout';
            self.plate_url = '/api/v2/plate';

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

            // Channel
            self.channels = ko.observableArray();
            self.current_channel = ko.observable();
            self.disable_channel = ko.computed(function() {
                return self.current_exp()? false: true
            });

            // Plate
            self.plates = ko.observableArray();
            self.current_plate = ko.observable();
            self.disable_plate = ko.computed(function() {
                if (self.current_exp() && self.current_layout()) {
                    return false;
                } else {
                    return true;
                }
            });

            // Handsontable obj
            self.table;

            self.disable_update = ko.computed(function() {
                if (self.current_exp() && self.current_layout() && 
                    self.current_channel() && self.current_plate()) {
                    return false;
                } else {
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
                    self.current_channel(null);
                    return;
                }

                // Update self.layouts
                self.get_layouts(exp.id);

                self.channels($.map(exp.channels(), function(chnl){
                    return new Channel(chnl);
                }));

                // Create the table
                if (self.table) {
                    // Destory existing table
                    self.table.destroy();
                }

                // TODO
                var container = document.getElementById('data_table');
                var settings = new utils.createSetting(exp.well());
                self.table = new Handsontable(container, settings);

                // Set current layout to empty one
                self.current_layout(self.layouts()[0]);
                self.current_factor(null);
            });

            self.sort_dispName = function(left, right) {
                return left.dispName == right.dispName ? 0 :
                    (left.dispName < right.dispName ? -1 : 1)
            };

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

                        self.layouts.sort(self.sort_dispName);
                    }
                });
            }

            self.current_layout.subscribe(function(layout){
                if (layout) {
                    self.factors(layout.factors());
                    self.get_plates(layout.id);
                }
            });

            self.get_plates = function(lid) {
            };

            // Flash information on the page
            self.flash = function(msg) {
                $("#plate-notice").html(msg).show().delay(2000).fadeOut();
            }

            self.validate = function() {
                if (self.current_layout().name() === '') {
                    self.flash('Error: invalid layout name!');
                    return 0;
                }
            };

            self.update_plate = function() {
            };

            // Initialize
            self.get_exps();
        };
    }
);
