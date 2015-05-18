define(['knockout'], function(ko) {
    return function(chnl) {
        var self = this;

        self.id = chnl.id ? chnl.id : 0;
        self.name = ko.observable(chnl.name ? chnl.name : '');
    };
});
