function viewModel(){
    var self = this;
    self.sec = ko.observable('design');  // Active section
    self.opt = ko.observable('exp');     // Active option
    self.fun = ko.observable('exp_old'); // Active function
    
    self.exp_name = ko.observable();
    self.exp_people = ko.observable();
    self.exp_date = ko.observable();

    self.plate_types = [96, 384];
    self.plate_type = ko.observable();

    self.experiments = ko.observableArray(['AAA', 'BBB']);
    self.layouts = ko.observableArray(['AAA', 'BBB']);

    // Factor (independent variables)
    self.exp_fact = ko.observableArray([new ExpVar()]);

    // Channels (dependent variables)
    self.exp_chnl = ko.observableArray([new ExpVar()]);

    self.var_types = ['Category', 'Integer', 'Decimal'];

	// Add a new dependent
    self.addChnl = function() { self.exp_chnl.push(new ExpVar()) };

    // Remove a channel
    self.delChnl = function(chnl) { self.exp_chnl.remove(chnl) };

	// Add a new independent
    self.addFact = function() { self.exp_fact.push(new ExpVar()) };

    // Remove a factor
    self.delFact = function(fact) { self.exp_fact.remove(fact) };
}

var ExpVar = function() {
    var self = this;
    self.name = ko.observable();
    self.type = ko.observable();
};
ko.applyBindings(new viewModel());

// TODO oop setting, make it dynamic for all types of tables
var setting = {
    startCols:24,
    minCols:24,
    maxCols:24,
    startRows:16,
    minRows:16,
    maxRows:16,
    colWidths:42,
    manualColumnResize:true,
    manualRowResize:true,
    rowHeaders:function (i) { return String.fromCharCode(65 + i); },
    colHeaders:function (i) { return i+1; },
    contextMenu: true,
};

var container1 = document.getElementById("well"); 
var hot = new Handsontable(container1, setting);
$(document).ready(function () {
    // Assign table to .tab-pane divs
});
