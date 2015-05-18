define(['knockout'], function(ko) {
    return function(id, name, dispName) {
    	var self = this;

    	self.id = id;
    	self.name = ko.observable(name);

    	if (!dispName){
    	    self.dispName = name;
    	} else {
    	    self.dispName = dispName;
    	}

    	self.factors = ko.observableArray();
    };
});
