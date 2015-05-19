define(['knockout', 'Channel'], function(ko, Channel) {
    return function(plate) {
        var self = this;

        self.id = plate.id ? plate.id : 0;
        // self.name = ko.observable(plate.name ? plate.name : '');
        self.name = 'Plate ' + plate.id;

        // Name to display on the page
        if (self.id === 0) {
            self.dispName = 'Add New Plate';
        } else {
            self.dispName = self.name;
        }

        self.channels = ko.observableArray(
            $.map(plate.channels ? plate.channels : [], function(chnl){
                return new Channel(chnl);
            })
        );

    };
});
