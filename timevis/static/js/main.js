function viewModel(){
    var self = this;
    self.activeSec = ko.observable('design');
    self.activeOpt = ko.observable('exp');
}
ko.applyBindings(new viewModel());
