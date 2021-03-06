define(['knockout'], function(ko) {
    return function(chnl) {
        var self = this;

        self.id = chnl.id ? chnl.id : 0;
        self.name = ko.observable(chnl.name ? chnl.name : '');
        self.dispName = self.name();
        self.time = chnl.time ? chnl.time : [];
        self.well = chnl.well ? chnl.well : [];
        self.value = chnl.value ? chnl.value : [];
    };
});
