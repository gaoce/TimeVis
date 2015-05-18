define(['knockout'], function(ko) {
    return function(id, name) {
        var self = this;

        self.id = id;
        self.name = ko.observable(name);
    };
});
