// ========================================================================
// viewModel class
// ========================================================================
function viewModel(){
    var self = this;

    // ========================================================================
    // Controls subpage
    // ========================================================================
    // | Section  | Option  |  Function |  Comment  |
    // | -------- | ------- | --------- | --------- |
    // | design   |  exp    |  exp_old  |           |
    // |          |         |  exp_new  |           |
    // |          |  lay    |  lay_old  |           |
    // |          |         |  lay_new  |           |
    // |          |  imp    |  imp_file |           |
    // |          |         |  imp_manu |           |
    // | vis      |  plate  |           |           |
    // |          |  genes  |           |           |
    // | analysis |  norm   |           |           |
    // |          |  expt   |           |           |
    //
    self.sec = ko.observable('design');  // Active section
    self.opt = ko.observable('exp');     // Active option
    self.fun = ko.observable('exp_old'); // Active function

    // Experiment subpage
    self.exp = new ExpVM();

    // Experiment subpage
    self.gene = new GeneVM();

    // ========================================================================
    // Layout subpage
    // ========================================================================
    //
    // Factor (independent variables)
    self.exp_fact = ko.observableArray([new ExpVar()]);
    self.layouts = ko.observableArray(['AAA', 'BBB']);
    self.layout_exps = ko.observableArray(['AAA','AAA']);

    // ========================================================================
    // Plates
    // ========================================================================

    // Visualize plate
    self.vis_plate = ko.observable(false);


    // ========================================================================
    // Genes Vis: Time series curve vis
    // ========================================================================
    // vis row
    self.row = ko.observableArray([ ['a', 'b'], ['c', 'd'] ]);

}

// ============================================================================
// Experiment View Model
// ============================================================================
function ExpVM() {
    var self = this;

    // =====================
    // Current functionality
    // =====================
    // Possible values: old, new
    self.fun = ko.observable('old');

    // Reset current_exp every time fun changes
    self.fun.subscribe(function(){self.current_exp(null);})

    // =====================
    // Experiment objs
    // =====================
    self.experiments = ko.observableArray();
    self.current_exp = ko.observable();
    // Factor (independent variables)
    self.exp_fact = ko.observableArray([new ExpVar()]);
    // Channels (dependent variables)
    self.exp_chnl = ko.observableArray();

    // Reset exp_fact everytime the current_exp is reset
    self.current_exp.subscribe(function(exp){
        self.exp_fact([]);
        if (exp) {
            for (f in exp.factors){
                self.exp_fact.push(exp.factors[f]);
            }
        }
    })

    // Reset exp_chnl everytime the current_exp is reset
    self.current_exp.subscribe(function(exp){
        self.exp_chnl([]);
        if (exp) {
            for (c in exp.channels){
                self.exp_chnl.push(exp.channels[c]);
            }
        }
    })

    // General information
    self.name = ko.computed(function(){
        if (self.current_exp()){
            return self.current_exp().name;
        }
    });

    self.user = ko.computed(function(){
        if (self.current_exp()){
            return self.current_exp().user;
        }
    });

    // Well numbers
    self.well_types = [96, 384];
    self.well = ko.computed(function(){
        if (self.current_exp()){
            return self.current_exp().well;
        }
    })

    // TODO: refresh button
    $.ajax({
        url: "/api/v2/experiment",
        type: "GET",
        success: function(data){
            for (e in data.experiment){
                self.experiments.push(data.experiment[e]);
            }
        }
    });

    // TODO disable update button if there is no change
    self.update_exp = function() {
        $.ajax({
            url: "/api/v2/experiment",
            type: "PUT",
            dataType: "json",
            data: JSON.stringify({experiment: [self.current_exp()]}),
            contentType: "application/json; charset=utf-8",
            success: function(data){
                self.current_exp(data);
            }
        });
    };


    self.var_types = ['Category', 'Integer', 'Decimal'];

    // Add a new dependent
    self.add_chnl = function() { self.exp_chnl.push(new ExpVar()) };

    // Remove a channel
    self.del_chnl = function(chnl) { self.exp_chnl.remove(chnl) };

    // Add a new independent
    self.add_fact = function() { self.exp_fact.push(new ExpVar()) };

    // Remove a factor
    self.del_fact = function(fact) { self.exp_fact.remove(fact) };
}

// ============================================================================
// Gene View Model
// ============================================================================
function GeneVM() {
    var self = this;

    // =====================
    // Experiment objs
    // =====================
    self.experiments = ko.observableArray();
    self.current_exp = ko.observable();           // Current experiment


    // TODO: trigger by switching to gene page.
    $.ajax({
        url: "/api/v2/experiment",
        type: "GET",
        success: function(data){
            for (e in data.experiment){
                self.experiments.push(data.experiment[e]);
            }
        }
    });

    // ========================================================================
    // Factor selection and query
    // ========================================================================
    self.current_exp.subscribe(function(exp){
        // Fill in self.factors
        if (exp){
            self.factors([]);
            for (var i in exp.factors){
                f = exp.factors[i];
                self.factors.push(new Factor(f.id, f.name, f.levels))
            }
        } else {
            self.factor_panels.removeAll();
        }
    });
    // Available factor for visualization
    self.factors = ko.observableArray();

    // Factor selected
    self.factor_panels = ko.observableArray();

    // Factor chosen to be added
    self.factor_chosen = ko.observable();

    // Add a factor selection panel
    self.add_panel = function() {
        if (self.factor_chosen()){
            self.factor_panels.push(self.factor_chosen());
            self.factors.remove(self.factor_chosen());
            self.factor_chosen(null);
        }
    };

    // Remove a factor
    self.del_panel = function(fact) {
        self.factor_panels.remove(fact);
        self.factors.push(fact);
        self.factors.sort(function(left, right) {
            return left.name == right.name ? 0 :
            (left.name < right.name ? -1 : 1)
        });
        self.factor_chosen();
    };

    // ========================================================================
    // Visualization
    // ========================================================================
    self.visualize = function(){};
    self.row = ko.observable();           // Current experiment
}

// ============================================================================
// Experiment class
// ============================================================================
function Exp(name, user, well_num) {
    var self = this;
    self.id = eid;
    self.name = name;
    self.user = user;
    self.well_num = 96;

    self.layouts = ko.observableArray();
}


// ============================================================================
// Factor class
// ============================================================================
var Factor = function(id, name, levels) {
    var self = this;
    self.id = id;
    self.name = name;
    self.query = ko.observable();

    //TODO keep the selection status while hidden
    self.query.subscribe(function(val){
        // check if string is empty
        if (val){
            for (g in self.levels()){
                if (self.levels()[g].name.search(val) === -1){
                    self.levels()[g]._destroy = true;
                } else {
                    self.levels()[g]._destroy = false;
                }
            }
        } else {
            for (g in self.levels()){
                self.levels()[g]._destroy = false;
            }
        }
        self.levels.valueHasMutated();
    }, self);

    self.levels = ko.observableArray();
    for (var i in levels){
        self.levels.push(new Level(levels[i]))
    }

    self.chosen_levels = ko.observableArray();
}

// ========================================================================
// Layout class
// ========================================================================
function Layout(name, well_num) {
    var self = this;
}

// Get Factor for experiment
// return a observableArray of Factor
function getFactors(exp) {
    return ko.observableArray([new Factor('A'),
                               new Factor('B')]);
}

// Search


var Level = function(name){
    var self = this;
    self.name = name;
    self.value = 1;
}

var ExpVar = function() {
    var self = this;
    self.name = ko.observable();
    self.type = ko.observable();
};
var vm = new viewModel();
ko.applyBindings(vm);

// ========================================================================
// handsontable
// ========================================================================
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

