function viewModel(){
    var self = this;
    self.activeSec = ko.observable('design');  // Active section
    self.activeOpt = ko.observable('exp');     // Active option
    self.activeFun = ko.observable('exp_old'); // Active function
    self.experiments = ko.observableArray(['AAA', 'BBB']);
    self.layouts = ko.observableArray(['AAA', 'BBB']);
    self.exp_vars = ko.observableArray([new ExpVar()]);
    self.var_types = ['categorical', 'numerical (integer)', 'numerical (flat)'];

	// Add a new variable
    self.addVar = function() { self.exp_vars.push(new ExpVar()) };
    // Remove a variable
    self.removeVar = function(variable) { self.exp_vars.remove(variable) };
}

var ExpVar = function() {
    var self = this;
    self.name = ko.observable();
    self.type = ko.observable();
};
ko.applyBindings(new viewModel());
