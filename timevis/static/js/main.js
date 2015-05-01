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

    // Visualize plate
    self.vis_plate = ko.observable(false);

    // Available factor for visualization
    self.avi_factors = ko.observableArray([createFactor('A'), createFactor('B')]);

    // Factor chosen to be added
    self.chosen_factor = ko.observable(createFactor('C'));

    // Add a factor selection panel
    self.add_panel = function() {
        self.factor_selected.push(self.chosen_factor);
    };

    // Factor selected
    self.factor_selected = ko.observableArray([createFactor('A'), createFactor('B')]);
}

var createFactor = function(name) {
    var self = this;
    self.name = name;
    self.levels = [1, 2, 3, 4];
    self.chosen_levels = ko.observable([]);
}

var ExpVar = function() {
    var self = this;
    self.name = ko.observable();
    self.type = ko.observable();
};
ko.applyBindings(new viewModel());

var createSetting = function(nRow, nCol, fixRow){
    self.startRows = nRow;
    self.minRows = nRow;
    if (fixRow) {
        self.maxRows = nRow;
    }

    self.startCols = nCol;
    self.minCols = nCol;
    self.maxCols = nCol;

    self.manualColumnResize = true;
    self.manualRowResize = true;
    self.contextMenu = true;

    self.rowHeaders = function(i) { return String.fromCharCode(65 + i); };
    self.colHeaders = function(i) { return i+1; };
};

// TODO oop setting, make it dynamic for all types of tables
var setting = {
    startCols:12,
    minCols:12,
    maxCols:12,
    // colWidths: 28,
    startRows:8,
    manualColumnResize:true,
    manualRowResize:true,
    rowHeaders:function (i) { return String.fromCharCode(65 + i); },
    colHeaders:function (i) { return i+1; },
    contextMenu: true
};

var container1 = document.getElementById("well");
var hot1 = new Handsontable(container1, setting);
var container2 = document.getElementById("data_table");
var hot2 = new Handsontable(container2, setting);

$("#time-slider").slider();
