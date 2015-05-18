// Organizational classes
define(function() {
    return function(id, name) {
        this.id = id;
        this.name = ko.observable(name);
    }
});
