define(['knockout', 'utils', 'ExpVM', 'LayoutVM', 'PlateVM', 'VisGeneVM'], 
    function(ko, utils, ExpVM, LayoutVM, PlateVM, VisGeneVM) {
        return function() {
            var self = this;
    
            /*
            * ================
            * Controls subpage
            * ================
            * | Section  | Option     |  Function |  Comment  |
            * | -------- | ---------  | --------- | --------- |
            * | design   |  exp       |           |           |
            * |          |  lay       |           |           |
            * |          |  plt       |           |           |
            * | vis      |  vis_plate |           |           |
            * |          |  vis_gene  |           |           |
            * | analysis |  norm      |           |           |
            * |          |  expt      |           |           |
            */
            self.sec = ko.observable('design');  // Active section
    
            var opt = utils.getCookie('opt');
            if (opt) {
                self.opt = ko.observable(opt);
            } else {
                self.opt = ko.observable('exp');     // Active option
            }
            self.opt.subscribe(function(newOpt){
                utils.setCookie('opt', newOpt)});
    
            // TODO: implement this at option level
            var fun = utils.getCookie('fun');
            if (fun) {
                self.fun = ko.observable(fun);
            } else {
                self.fun = ko.observable('exp');     // Active funion
            }
            self.fun.subscribe(function (newFun){
                utils.setCookie('fun', newFun)})
    
            // Experiment subpage
            self.exp = new ExpVM();
    
            // Layout subpage
            self.layout = new LayoutVM();
            self.layouts = [];

            // Plate import subpage
            self.plate = new PlateVM();
    
            // Experiment subpage
            self.vis_gene = new VisGeneVM();
    
            // Visualize plate
            self.vis_plate = ko.observable(false);
    
            // vis row
            self.row = ko.observableArray([ ['a', 'b'], ['c', 'd'] ]);
        };
    }
);
