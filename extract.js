const DomParser = require('dom-parser');
const request = require('sync-request');
var parser = new DomParser();

var fs = require('fs');

function job_deparse(job) {
    try {
        let html = request('GET', 'http://www.jobs.bg/job/' + job).getBody('utf-8');
        console.log('Job', job + ':');
        const dom = parser.parseFromString(html);
        try {
            let jobTitle = dom.getElementsByTagName("b")[0].innerHTML;
            let jobAuthor = dom.getElementsByClassName("company_link")[0].innerHTML;
            let jobLocation = dom.getElementsByTagName("td")[10].innerHTML.split(';')[0].substring(12);

            let jobAddedTags = dom.getElementsByTagName("td")[10].innerHTML.split(';').map((x) => '&lt;' + x + '&gt;').join(' ');

            let jobDescription = dom.getElementsByTagName("td")[12].innerHTML + '<br><br>' + jobAddedTags + '<br><br>Author: ' + jobAuthor;

            console.log(
                {
                    'id': '-1',
                    'job-title': jobTitle,
                    'email': 'contact_us@headstarter.eu',
                    'location': jobLocation,
                    'company_id': 2,
                    'description': jobDescription,
                    'job-available': false,
                    'duration': 12,
                    'job-type': '8ч.',
                    'job-age': '18+',
                    'job-category': '58'
                }
            );

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
            console.log('job', job + ': Generated');
        } catch (e) {
            console.log('job', job + ': Can\'t get the offer', e);
        }
    } catch (e) {
        console.log('job', job + ': Can\'t get the offer', e);
    }
}

let line = '';

fs.readFile('jobs', {encoding: 'utf-8'}, function(err,text){
    if (!err) {
        for (const data of text) {
            if (data == '\n')
            {
                if (line[0] == 'j')
                {
                    // job/<number> <number>
                    let job_number = line.split(' ')[1];
                    job_deparse(job_number);
                }
                else {
                    // Page logger
                }
                line = '';
            }
            else {
                line += data;
            }
        }
    } else {
        console.log(err);
    }
});