require.config({
    paths: {
        jquery: 'lib/jquery.min',
        knockout: 'lib/knockout.min',
		domReady: 'lib/domReady',
		handsontable: 'lib/handsontable.full.min'
    }
});

require(['knockout', 'ViewModel', 'domReady!'], function(ko, ViewModel){
	var vm = new ViewModel();
    ko.applyBindings(vm);
});
