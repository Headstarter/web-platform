const DomParser = require('dom-parser');
const request = require('request-promise');
var parser = new DomParser();

async function page_getter(page) {
    request('https://www.jobs.bg/front_job_search.php?frompage=' + page * 15 + '&zone_id=0&distance=0&location_sid=&all_categories=0&all_type=0&all_position_level=1&all_company_type=1&keyword=&csrf_token=bMiduN7DDUy6ij8YLH1_J2duWpME8Y-LE0i92iVF7hY&last=0#paging')
        .then(function(response) {
            let html = response;
            console.log('Page', page + '/' + 2304 + ':');
            let ind = 0;
            let page_jobs = "";
            while (ind != -1) {
                ind = html.indexOf('job/', ind) + 1;
                let number = "";
                for (let x = ind - 1; html[x] != '"'; x += 1) {
                    number += html[x];
                }
                if (number.indexOf('DOCTYPE') == -1) {
                    console.log(number);
                }
            }
        })
        .catch(function(e) {});
}


for (let page = 0; page < 2304; page += 1) {
    page_getter(page);
}
// -----------------------------------------------------------
const DomParser = require('dom-parser');
const request = require('sync-request');
var parser = new DomParser();

for (let job = 0; job < 10000000; job += 1) {
    let html = request('GET', 'https://www.jobs.bg/job/' + job).getBody('utf-8');
    console.log('Job', job + ':');
    const dom = parser.parseFromString(html);
    try {
        let jobTitle = dom.getElementsByTagName("td")[9].children[1].innerHTML;
        let jobAuthor = dom.getElementsByTagName("td")[9].children[2].innerHTML;
        let jobLocation = dom.getElementsByTagName("td")[10].innerHTML.split(';')[0].substring(12);

        let jobAddedTags = dom.getElementsByTagName("td")[10].innerHTML.split(';').map((x) => '&lt;' + x + '&gt;').join(' ');

        let jobDescription = dom.getElementsByTagName("td")[12].innerHTML + '<br><br>' + jobAddedTags + '<br><br>Author: ' + jobAuthor;

        /*let options = {
            method: 'POST',
            uri: 'https://headstarter.eu/internship/new',
            body: {
                'id': '-1',
                'job-title': jobTitle,
                'email': 'contact_us@headstarter.eu',
                'location': jobLocation,
                'company_id': 2,
                'description': jobDescription,
                'job-available': False,
                'duration': 12,
                'job-type': '8ч.',
                'job-age': '18+',
                'job-category': '58'
            }
        };
        let record = request(options);
        if (record.status == 200)
            console.log('job', job + ': Put successfully');
        else
            console.log('job', job + ': Can\'t puting failed');
        */
        console.log('job', job + ': Available');
    } catch (e) {
        console.log('job', job + ': Can\'t get the offer');
    }
}