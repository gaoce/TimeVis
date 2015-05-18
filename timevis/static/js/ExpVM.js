define(['jquery', 'knockout', 'Exp'], function($, ko, Exp) {
    return function() {
    	var self = this;
        // API url
    	self.url = "/api/v2/experiment";

    	// Array of experiment objs
    	self.experiments = ko.observableArray();

  		// Current one displayed on the page
    	self.current_exp = ko.observable();

    	// Function to retrieve exp objs through API
    	self.get_exp = function() {
    	    $.ajax({
    	        url: self.url,
    	        type: "GET",
    	        success: function(data) {
                    // Clean before anything
    	            self.experiments.removeAll();

                    // Convert exp from API to Exp obj and append them to
                    // experiment array
    	            $.map(data.experiment, function(exp) {
    	                self.experiments.push(new Exp(exp));
    	            });

    	            // Add empty experiment in the front
    	            self.experiments.unshift(new Exp({}));

    	            // By default, current_exp is empty
    	            self.current_exp(self.experiments()[0]);
    	        },
                error: function(data) {
    	            self.flash('Error: '+
                        $.parseJSON(data.responseText)['Error']);
                }
    	    });
    	};

        // Retrieve exp objs thru API
    	self.get_exp();

    	// Flash information on the page
    	self.flash = function(msg) {
    	    $("#exp-notice").html(msg).show().delay(2000).fadeOut();
    	}

    	// Validate input fields, including experiment names, factors and
        // channels, return 0 if any of them is invalid
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

        // Utility function to sort experiment array
        self.sort_exp = function(left, right) {
            return left.dispName == right.dispName ? 0 :
                (left.dispName < right.dispName ? -1 : 1)
        };

    	// POST (if id=0) or PUT current_exp thru API
    	self.update_exp = function() {
            // Validate fields on the page
    	    if (self.validate() === 0){ return };

            // New exp's ID is 0
    	    var http_method = self.current_exp().id === 0 ? 'POST' : 'PUT';

    	    // Send to server
    	    $.ajax({
    	        url: self.url,
    	        type: http_method,
    	        dataType: "json",
    	        data: JSON.stringify({
                    experiment: [ko.toJS(self.current_exp())]
                }),
    	        contentType: "application/json; charset=utf-8",
    	        success: function(data){
                    // If POST/PUT succeed, the uploaded/updated exp obj will be
                    // returned, we use it to update the current page
    	            var exp = new Exp(data.experiment[0]);
    	            self.experiments.remove(self.current_exp());
    	            self.experiments.push(exp);
                    self.experiments.sort(self.sort_exp);
    	            self.current_exp(exp);

                    // Add a new empty exp obj
    	            if (http_method === "POST"){
    	                self.experiments.unshift(new Exp({}));
    	            }
    	            self.flash('Succeed!');
    	        },
    	        error: function(data){
    	            self.flash('Error: '+
                            $.parseJSON(data.responseText)['Error']);
    	        }
    	    });
    	};
	};
});
