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

            // Channel
            self.channels = ko.observableArray();
            self.current_channel = ko.observable();
            self.disable_channel = ko.computed(function() {
                return self.current_plate()? false: true
            });
            // Array of channel prototypes (same id and name as those in
            // current_exp().channels, but without values)
            self.channel_prty = [];

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

                // Update channel prototypes
                self.channel_prty = $.map(exp.channels(), function(chnl) {
                    return {id: chnl.id, name: chnl.name()};
                });

                // Update self.layouts
                self.get_layouts(exp.id);

                // Create the table
                if (self.table) {
                    // Destory existing table
                    self.table.destroy();
                }

                // TODO
                var container = document.getElementById('data_table');
                var settings = new utils.createDataSetting(exp.well());
                self.table = new Handsontable(container, settings);

                // Set current layout to empty one
                self.current_layout(null);
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
                    self.get_plates(layout.id);
                } else {
                    self.current_plate(null);
                }
            });

            self.get_plates = function(lid) {
                $.ajax({
                    url: self.plate_url + '?lid=' + lid,
                    type: "GET",
                    success: function(data) {
                        // Populate layouts with returned objects
                        self.plates(
                            $.map(data.plate, function(plate) {
                                return new Plate(plate);
                            })
                        );

                        self.plates.sort(self.sort_dispName);
                        self.plates.unshift(new Plate({}));
                    }
                });
            };

            self.current_plate.subscribe(function(plate){
                if (plate) {
                    self.channels(plate.channels());
                }
            });

            self.encodeData = function(value, time){
                for (var i in value) {
                    value[i].unshift(time[i]);
                }
                return value;
            };
            self.decodeData = function(){};
            self.current_channel.subscribe(function(chnl){
                if (chnl) {
                    var data = self.encodeData(chnl.value, chnl.time);
                    self.table.loadData(data);
                }
            });

            // Flash information on the page
            self.flash = function(msg) {
                $("#plate-notice").html(msg).show().delay(2000).fadeOut();
            }

            self.update_plate = function() {
            };

            // Initialize
            self.get_exps();
        };
    }
);
