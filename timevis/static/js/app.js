require.config({
    paths: {
        jquery: 'lib/jquery.min',
        knockout: 'lib/knockout.min',
		domReady: 'lib/domReady',
    }
});

require(['knockout', 'ViewModel', 'domReady!'], function(ko, ViewModel, h){
	var vm = new ViewModel();
    ko.applyBindings(vm);
    window.vm = vm;
});
