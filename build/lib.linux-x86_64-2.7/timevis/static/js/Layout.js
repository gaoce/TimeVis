define(['knockout', 'Factor'], function(ko, Factor) {
    return function(layout) {
        var self = this;

        self.id = layout.id ? layout.id : 0;
        self.name = ko.observable(layout.name ? layout.name : '');

        // Name to display on the page
        if (self.id === 0) {
            self.dispName = 'Add New Layout';
        } else {
            self.dispName = self.name();
        }

        self.factors = ko.observableArray(
            $.map(layout.factors ? layout.factors : [], function(fac){
                return new Factor(fac);
            })
        );
    };
});
