define(['jquery', 'knockout', 'Level'], function($, ko, Level) {
    return function(fac) {
        /* Parameters:
         *   fac: factor object, returned from API, w/ the following properties:
         *     id: factor id
         *     name: factor name
         *     type: type should be within self.factor_types
         *     levels: unique levels of the factor
         */

        var self = this;

        /*
         * Basic information of a factor object: id, name, type and levels if
         * provided
         */
        self.id = fac.id ? fac.id : 0;
        self.name = ko.observable(fac.name ? fac.name : '');
        self.type = ko.observable(fac.type ? fac.type : null);

        lvls = fac.levels ? fac.levels : [];
        if (typeof lvls === 'object') {
            var arr = []
            $.map(Object.keys(lvls).sort(), function(k){
                arr.push(lvls[k]);
            });
            lvls = arr;
        }
        self.levels = ko.observableArray(
            $.map(lvls, function(lvl){ return new Level(lvl); })
        );

        // Make sure input factor type is valid
        self.factor_types = ['Category', 'Integer', 'Decimal', null];
        if (self.factor_types.indexOf(self.type()) == -1){
            throw new Error(self.type() + ' is not allowed!');
        }

        /*
         * Helper function to select levels in factor
         */
        //TODO keep the selection status while hidden
        self.query = ko.observable();
        self.query.subscribe(function(val){
            // check if string is empty
            if (val){
                for (g in self.levels()){
                    if (self.levels()[g].name.search(val) === -1){
                        self.levels()[g]._destroy = true;
                    } else {
                        self.levels()[g]._destroy = false;
                    }
                }
            } else {
                for (g in self.levels()){
                    self.levels()[g]._destroy = false;
                }
            }
            self.levels.valueHasMutated();
        }, self);
        self.chosen_levels = ko.observableArray();

        self.get_chosen_levels = function(){
            return $.map(self.chosen_levels(), function(l){return l.name})
        }

    };
});
