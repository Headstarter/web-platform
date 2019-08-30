const DomParser = require('dom-parser');
const request = require('sync-request');
var parser = new DomParser();

String.prototype.matchAll = function(regexp) {
    var matches = [];
    this.replace(regexp, function() {
      var arr = ([]).slice.call(arguments, 0);
      var extras = arr.splice(-2);
      arr.index = extras[0];
      arr.input = extras[1];
      matches.push(arr);
    });
    return matches.length ? matches : null;
  };

function page_getter(page) {
    let html = request('GET','https://www.jobs.bg/front_job_search.php?frompage=' + page * 15 + '&zone_id=0&distance=0&location_sid=&all_categories=0&all_type=0&all_position_level=1&all_company_type=1&keyword=&csrf_token=bMiduN7DDUy6ij8YLH1_J2duWpME8Y-LE0i92iVF7hY&last=0#paging').getBody('utf-8');
    console.log('Page', page + '/' + 2308 + ':');
    let reg = /job\/([0-9]*)/g;
    let matches = Array.from(String(html).matchAll(reg));
    for (let i = 0 ; i < matches.length ; i += 1)
    {
        console.log(matches[i][0], matches[i][1]);
    }
}


for (let page = 0; page < 2308; page += 1) {
    page_getter(page);
}