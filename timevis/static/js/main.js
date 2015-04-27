function viewModel(){
    var self = this;
    self.active = ko.observable('');
    self.activeA = ko.observable(false);
    self.activeB = ko.observable(false);
    self.activeC = ko.observable(false);
    self.activeAItem = function(){self.active('a')};
    self.activeBItem = function(){self.active('b')};
    self.activeCItem = function(){self.active('c')};
}
ko.applyBindings(new viewModel());
