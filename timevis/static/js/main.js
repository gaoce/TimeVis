// Set cookie
function setCookie(cname, cvalue) {
 	var exdays = 1;
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

// Get cookie
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}

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

    var opt = getCookie('opt');
    if (opt) {
        self.opt = ko.observable(opt);
    } else {
        self.opt = ko.observable('exp');     // Active option
    }
    self.opt.subscribe(function (newOpt){ setCookie('opt', newOpt)})

    // TODO: implement this at option level
    var fun = getCookie('fun');
    if (fun) {
        self.fun = ko.observable(fun);
    } else {
        self.fun = ko.observable('exp');     // Active funion
    }
    self.fun.subscribe(function (newFun){ setCookie('fun', newFun)})

    // Experiment subpage
    self.exp = new ExpVM();

    // Experiment subpage
    self.gene = new GeneVM();

    // ========================================================================
    // Layout subpage
    // ========================================================================
    //
    // Factor (independent variables)
    self.exp_fact = ko.observableArray([new Factor()]);
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
    // Experiment objs
    // =====================
    self.experiments = ko.observableArray();
    self.current_exp = ko.observable();

    self.get_exp = function() {
        $.ajax({
            url: "/api/v2/experiment",
            type: "GET",
            success: function(data){
                exps = data.experiment;
                $.map(exps, function(exp){
                    self.experiments.push(
                        new Exp(exp.id, exp.name, exp.user, exp.well,
                            exp.factors, exp.channels)
                    );
                });
                if (!self.current_exp()){
                    self.current_exp(self.experiments()[0]);
                }
            }
        });
    };
    self.get_exp();

    self.update_current_exp = function(exp_obj) {
        if (!self.current_exp()) {
            self.current_exp(new Exp(null, null, null, null, [], []));
        }
        var e = self.current_exp();
        e.id = exp_obj.id;
        e.name(exp_obj.name);
        e.user(exp_obj.user);
        e.well(exp_obj.well);
        e.factors(
            $.map(exp_obj.factors, function(f){
                return new Factor(f.id, f.name, f.type, f.levels);
            })
        );
        e.channels(
            $.map(exp_obj.channels, function(c){
                return new Channel(c.id, c.name);
            })
        );

        self.current_exp.valueHasMutated();
    };

    // ================================================
    // Current functionality, possible values: old, new
    // ================================================
    switch(getCookie('exp_fun')) {
        case '':
        case 'old':
        case 'new':
            self.fun = ko.observable('old');
            break;
        // case 'new':
        //     self.fun = ko.observable('new');
        //     self.update_current_exp({id: 0, name: "", user: "", well: "",
        //         factors: [], channels: [] })
    }

    // self.fun = exp_fun != '' ? ko.observable(exp_fun) : ko.observable('old');
    // A holder for existing experiment obj
    self.last_exp;
    self.fun.subscribe(function(newFun){
        setCookie('exp_fun', newFun)
        if (newFun === 'new') {
            self.last_exp = ko.toJS(self.current_exp);
            self.update_current_exp({id: 0, name: "", user: "", well: "",
                factors: [], channels: [] })
        } else {
            self.update_current_exp(self.last_exp)
        }
    });


    self.flash = function(msg) {
        $("#exp-notice").html(msg).show().delay(2000).fadeOut();
    }

    // Validate input fields, incl. experiment names, factors and channels
    self.validate = function() {
        // Check if there is an experiment name
        if (self.current_exp().name() === ''){
            self.flash('Error: invalid experiment name!');
            return 0;
        }

        // Validate Factors
        if (self.current_exp().factors().length === 0) {
            self.flash('Error: no factors available!');
            return 0;
        }

        // Check factor name and type availability
        for (var i in self.current_exp().factors()){
            var f = self.current_exp().factors()[i];
            if (f.name() === '' || !f.type()){
                self.flash('Error: invalid Factors!');
                return 0;
            }
        }

        // Validate Channels
        if (self.current_exp().channels().length === 0) {
            self.flash('Error: no channels available!');
            return 0;
        }

        // Check channel name and type availability
        for (var i in self.current_exp().channels()){
            var c = self.current_exp().channels()[i];
            if (c.name() === ''){
                self.flash('Error: invalid Channels!');
                return 0;
            }
        }
    }

    // TODO disable update button if there is no change
    self.put_exp = function() {
        if (self.validate() === 0){ return };

        // Send to server
        $.ajax({
            url: "/api/v2/experiment",
            type: "PUT",
            dataType: "json",
            data: JSON.stringify({experiment: [ko.toJS(self.current_exp())]}),
            contentType: "application/json; charset=utf-8",
            success: function(data){
                self.current_exp(data.experiment[0]);
                self.flash('Succeed!');
            },
            error: function(data){
                self.flash('Failed! ' + $.parseJSON(data.responseText)['Error']);
            }
        });
    };

    self.post_exp = function(){
        if (self.validate() === 0){ return };

        // Send to server
        $.ajax({
            url: "/api/v2/experiment",
            type: "POST",
            dataType: "json",
            data: JSON.stringify({experiment: [ko.toJS(self.current_exp())]}),
            contentType: "application/json; charset=utf-8",
            success: function(data){
                self.update_current_exp(data.experiment[0]);
                self.flash('Succeed!');
            },
            error: function(data){
                self.flash('Failed! ' + $.parseJSON(data.responseText)['Error']);
            }
        });
    };


    self.factor_types = ['Category', 'Integer', 'Decimal'];

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
    self.channels = ko.observableArray();
    self.current_channel = ko.observable();

    // ========================================================================
    // Factor selection and query
    // ========================================================================
    // self.current_exp.subscribe(function(exp){
    //     // Fill in self.factors
    //     if (exp){
    //         self.factors([]);
    //         $.map(exp.factors, function(f){
    //             self.factors.push(new Factor(f.id, f.name, f.levels))
    //         })
    //         $.map(exp.channels, function(c){
    //             self.channels.push(new Channel(c.id,  c.name))
    //         })
    //     } else {
    //         self.current_channel(null);
    //         self.factor_panels.removeAll();
    //     }
    // });
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
    self.graphs = ko.observableArray();
    self.current_graph = 0;
    self.current_graph_id = "";
    self.visualize = function(){
        var factors = $.map(self.factor_panels(), function(f){
            return {"id": f.id, "levels": f.get_chosen_levels()}
        })
        var res = {
            experiment: self.current_exp().id,
            channel: self.current_channel().id,
            factors: factors

        }
        $.ajax({
            url: "/api/v2/timeseries",
            type: "POST",
            dataType: "json",
            data: JSON.stringify(res),
            contentType: "application/json; charset=utf-8",
            success: function(json){
                self.current_graph_id = "id" + self.current_graph;
                self.graphs.push({id: self.current_graph_id})

                var target = "#" + self.current_graph_id;
                var data = json.result;
                data = MG.convert.date(data, 'time', "%H:%M:%S");

                des = "<pre>" + JSON.stringify(json.query, ' ', 2) + "</pre>";
                MG.data_graphic({
                        title: "Hover for Information",
                        description: des,
                        data: data,
                        target: target,
                        show_confidence_band: ['l', 'u'],
                        full_width: true,
                        top: 25,
                        left: 20,
                        right: 20,
                        point_size: 5,
                        area: false,
                        x_accessor: 'time',
                        y_accessor: 'value',
                        show_secondary_x_label: false,
                        mouseover: function(d, i) {
                            // custom format the rollover text, show days
                			var timeFmt = d3.time.format('%H:%M');
                    		var time = timeFmt(d.time);
                            var val = d3.formatPrefix(d.value)
                                        .scale(d.value)
                                        .toFixed(2);
                            var selector = target + ' svg .mg-active-datapoint';
                            d3.select(selector).text("[" + time + "]: " + val);
                            d3.select(selector).style({'font-size': '1em'});
                        }
                    });
                self.current_graph += 1;
            }
        });
    };
    self.row = ko.observable();           // Current experiment
}

// ============================================================================
// Experiment class
// ============================================================================
function Exp(id, name, user, well, factors, channels) {
    // Parameters:
    //  id: integer. Experiment id
    //  name: string. Experiment name
    //  user: string. Experiment user
    //  well: integer. Number of wells
    //  factors: array of factors
    //  channels: array of channels
    var self = this;

    self.id = id;
    self.name = ko.observable(name);
    self.user = ko.observable(user);
    self.well = ko.observable(well);
    self.well_types = [96, 384];

    self.factors = ko.observableArray(
        $.map(factors, function(f){
            return new Factor(f.id, f.name, f.type, f.levels);
        })
    );

    self.channels = ko.observableArray(
        $.map(channels, function(c){
            return new Channel(c.id, c.name);
        })
    );

    // Add a new factor
    self.add_fact = function() {
		// New Factor object should have a ID of 0
        self.factors.push(new Factor(0, '', null, []));
    };

    // Remove a factor
    self.del_fact = function(fact) {
        self.factors.remove(fact)
    };

    // Add a new dependent
    self.add_chnl = function() { self.channels.push(new Channel(0, '')) };

    // Remove a channel
    self.del_chnl = function(chnl) { self.channels.remove(chnl) };
}


// ============
// Factor class
// ============
var Factor = function(id, name, type, levels) {
    var self = this;
    self.id = id;
    self.name = ko.observable(name);
    self.type = ko.observable(type);
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

    self.get_chosen_levels = function(){
        return $.map(self.chosen_levels(), function(l){return l.name})
    }
}

// ============
// Layout class
// ============
function Layout(id, name) {
    var self = this;

    self.id = id;
    self.name = name;
}

// =============
// Channel class
// =============
function Channel(id, name) {
    this.id = id;
    this.name = ko.observable(name);
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

var vm;
$(function(){
    vm = new viewModel();
    ko.applyBindings(vm);
});
