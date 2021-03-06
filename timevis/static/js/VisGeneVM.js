define(['jquery', 'knockout', 'Exp', 'Factor', 'Channel'],
    function($, ko, Exp, Factor, Channel) {
        return function() {
            var self = this;

            // API urls
            self.exp_url = "/api/v2/experiment";

            // Experiment objs
            self.experiments = ko.observableArray();
            self.current_exp = ko.observable();

            // channels
            self.channels = ko.observableArray();
            self.current_channel = ko.observable();

            // Available factor for visualization
            self.factors = ko.observableArray();

            // Factor selected
            self.factor_panels = ko.observableArray();

            // Factor chosen to be added
            self.factor_chosen = ko.observable();

            self.get_exps = function() {
                $.ajax({
                    url: self.exp_url,
                    type: "GET",
                    success: function(data) {
                        self.experiments(
                            $.map(data.experiment, function(exp){
                                return new Exp(exp);
                            })
                        );
                    }  /* success */
                });  /* ajax */
            };

            self.get_exps();

            self.validate = function() {};

            self.current_exp.subscribe(function(exp) {
                // Fill in self.factors
                if (exp){
                    self.factors(exp.factors());
                    self.channels(exp.channels());
                } else {
                    self.current_channel(null);
                    self.factor_panels.removeAll();
                }
            });

            // Add a factor selection panel
            self.add_panel = function() {
                if (self.factor_chosen()) {
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

            // =============
            // Visualization
            // =============
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

                        des = "<pre>" + JSON.stringify(json.query, ' ', 2) + 
                              "</pre>";

                        MG.data_graphic({
                                title: "Hover for Information",
                                description: des,
                                data: data,
                                target: target,
                                show_confidence_band: ['l', 'u'],
                                full_width: true,
                                top: 25,
                                left: 50,
                                right: 20,
                                point_size: 5,
                                area: false,
                                x_accessor: 'time',
                                y_accessor: 'value',
                                show_secondary_x_label: false,
                                mouseover: function(d, i) {
                                    // custom format rollover text, show days
                                    var timeFmt = d3.time.format('%H:%M');
                                    var time = timeFmt(d.time);
                                    var val = d3.formatPrefix(d.value)
                                                .scale(d.value)
                                                .toFixed(2);
                                    var selector = target + 
                                        ' svg .mg-active-datapoint';
                                    d3.select(selector).text("[" + time + 
                                            "]: " + val);
                                    d3.select(selector).style({'font-size': 
                                        '1em'});
                                }
                            });
                        self.current_graph += 1;
                    }
                });
            };
            self.row = ko.observable();           // Current experiment
        };
    }
);
