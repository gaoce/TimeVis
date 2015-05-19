define({
    setCookie: function(cname, cvalue) {
        var exdays = 1;
        var d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
    },
    getCookie: function(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
        }
        return "";
    },
    createSetting: function(nWell) {
        var self = this;
        switch (nWell) {
            case 96:
                var nRow = 8;
                var nCol = 12;
                break;
            case 384:
                var nRow = 16;
                var nCol = 24;
                break;
            default:
                return
        }
        self.startRows = nRow;
        self.minRows = nRow;
        self.maxRows = nRow;

        self.startCols = nCol;
        self.minCols = nCol;
        self.maxCols = nCol;

        self.colWidths = 750/(nCol+2);

        self.manualColumnResize = true;
        self.manualRowResize = true;
        self.contextMenu = true;

        self.rowHeaders = function(i) { return String.fromCharCode(65 + i); };
        self.colHeaders = function(i) { return i+1; };
        self.className = 'htCenter';
    },
    createDataSetting: function(nWell) {
        var self = this;
        switch (nWell) {
            case 96:
                var nRow = 8;
                var nCol = 12;
                break;
            case 384:
                var nRow = 16;
                var nCol = 24;
                break;
            default:
                return
        }
        self.startRows = 4;

        self.startCols = nWell + 1;
        self.minCols = nWell + 1;
        self.maxCols = nWell + 1;
        self.stretchH = 'all';

        self.manualColumnResize = true;
        self.manualRowResize = true;
        self.contextMenu = true;

        self.columns = [{}];
        for (var i = 0; i < nWell; i++) {
            self.columns.push({type: 'numeric', format: '0.00'});
        }

        self.colHeaders = function(i) {
            if (i > 0){
                var col = (i - 1) % nCol + 1;
                var row = (i - col) / nCol + 1;
                return String.fromCharCode(64 + row) + (col < 10 ? '0' : '') +
                    col;
            } else {
                return 'Time';
            }
        };
        self.className = 'htCenter';
    }
});
