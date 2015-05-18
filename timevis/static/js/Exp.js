// Experiment class
define(['jquery', 'knockout', 'Factor', 'Channel'], 
    function($, ko, Factor, Channel) {
        return function(exp) {
            /*  Parameters:
             *   exp: exp object returned from API
             *       id: integer. Experiment id
             *       name: string. Experiment name
             *       user: string. Experiment user
             *       well: integer. Number of wells
             *       factors: array of factors
             *       channels: array of channels
             *       displayName: name to display
             */

            var self = this;

            self.id = exp.id ? exp.id : 0;
            self.name = ko.observable(exp.name ? exp.name : '');
            self.user = ko.observable(exp.user ? exp.user : '');
            self.well = ko.observable(exp.well ? exp.well : null);
            self.well_types = [96, 384];

            // Name to display on the page
            if (self.id === 0) {
                self.dispName = 'Add New Experiment';
            } else {
                self.dispName = self.name();
            }

            self.factors = ko.observableArray(
                $.map(exp.factors ? exp.factors : [], function(fac){
                    return new Factor(fac);
                })
            );

            self.channels = ko.observableArray(
                $.map(exp.channels ? exp.channels : [], function(chnl){
                    return new Channel(chnl);
                })
            );

            // Add a new factor
            self.add_fact = function() {
                // New Factor object should have a ID of 0
                self.factors.push(new Factor({}));
            };

            // Remove a factor
            self.del_fact = function(fact) {
                self.factors.remove(fact)
            };

            // Add a new dependent
            self.add_chnl = function() { self.channels.push(new Channel({})) };

            // Remove a channel
            self.del_chnl = function(chnl) { self.channels.remove(chnl) };
        };
    }
);
