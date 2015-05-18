// Organizational classes
define(['jquery', 'knockout', 'Level'], function($, ko, Level) {
    return function(id, name, type, levels) {
        var self = this;
        self.id = id;
        self.name = ko.observable(name);
        self.type = ko.observable(type);
        self.query = ko.observable();

        //TODO keep the selection status while hidden
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

        self.levels = ko.observableArray();
        for (var i in levels){
            self.levels.push(new Level(levels[i]))
        }

        self.chosen_levels = ko.observableArray();

        self.get_chosen_levels = function(){
            return $.map(self.chosen_levels(), function(l){return l.name})
        }

        self.factor_types = ['Category', 'Integer', 'Decimal'];
    };
});
