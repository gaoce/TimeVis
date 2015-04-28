function viewModel(){
    var self = this;
    self.sec = ko.observable('design');  // Active section
    self.opt = ko.observable('exp');     // Active option
    self.fun = ko.observable('exp_old'); // Active function

    self.experiments = ko.observableArray(['AAA', 'BBB']);
    self.layouts = ko.observableArray(['AAA', 'BBB']);
    self.exp_vars = ko.observableArray([new ExpVar()]);
    self.var_types = ['Category', 'Integer', 'Decimal'];

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
