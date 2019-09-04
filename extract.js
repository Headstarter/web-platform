const DomParser = require('dom-parser');
const request = require('sync-request');
var parser = new DomParser();

var fs = require('fs');

let companies = new Set();
let regexes = {
    'companyLink': /href="(.*)"/g,
    'companyId': /https:\/\/www\.jobs\.bg\/company\/([0-9]+)/g,
    'companyLogo': /url\('(.*)'\)/g,
};

function gen_code() {
    var result = '';
    var characters = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM';
    var charactersLength = characters.length;
    for (var i = 0; i < 16; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function company_deparse(companyLink) {
    if (companies.has(companyLink)) {
        throw new Exception('Company is already processed.');
    } else {
        companies.add(companyLink);
    }
    let html = request('GET', companyLink).getBody('utf-8');
    console.log('Company', companyLink + ':');
    const dom = parser.parseFromString(html);

    let id = regexes.companyId.exec(companyLink)[1];
    let uid = gen_code();

    let name = dom.getElementsByTagName('h1')[0].innerHTML;
    let description = dom.getElementsByClassName('htmlTemplate')[0].innerHTML;
    let logo = regexes.companyLogo.exec(dom.getElementsByClassName('profileCoverImg')[0].outerHTML)[1];
    let website = '(Няма въведена интернет страница)';
    let contacts = dom.getElementsByTagName('table')[3].children[0].children[0].children[0].children[4].innerHTML.replace(/\s+/g, '');

    return {
        'id': id,
        'uid': uid,
        'description': description,
        'logo': logo,
        'website': website,
        'contacts': contacts
    };
}

function job_deparse(job) {
    try {
        let html = request('GET', 'http://www.jobs.bg/job/' + job).getBody('utf-8');
        console.log('Job', job + ':');
        const dom = parser.parseFromString(html);
        for (let i = 0; i < dom.getElementsByClassName("company_link").length; i += 1) {
            console.log(i, dom.getElementsByClassName("company_link")[i].outerHTML.substring(0, 150))
        }
        try {
            let jobTitle = dom.getElementsByTagName("b")[2].innerHTML;

            let companyLink = regexes.companyLink.exec(jobAuthor)[1];
            let companyId = regexes.companyId.exec(companyLink)[1];
            try {
                let company = company_deparse(companyLink);
                fs.writeFile('companies.txt', JSON.stringify(company) + '\n', function(err) {
                    if (err) throw err;
                });
            } catch (e) {
                console.log(companyLink, e);
            }

            let jobLocation = dom.getElementsByTagName("td")[10].innerHTML.split(';')[0].substring(12);

            let jobAddedTags = dom.getElementsByTagName("td")[10].innerHTML.split(';').map((x) => '&lt;' + x + '&gt;').join(' ');

            let jobDescription = dom.getElementsByTagName("td")[12].innerHTML + '<br><br>' + jobAddedTags + '<br><br>Author: ' + jobAuthor;

            let job = {
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
            };

            fs.writeFile('companies.txt', JSON.stringify(company) + '\n', function(err) {
                if (err) throw err;
            });

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

fs.readFile('jobs', { encoding: 'utf-8' }, function(err, text) {
    if (!err) {
        for (const data of text) {
            if (data == '\n') {
                if (line[0] == 'j') {
                    // job/<number> <number>
                    let job_number = line.split(' ')[1];
                    job_deparse(job_number);
                } else {
                    // Page logger
                }
                line = '';
            } else {
                line += data;
            }
        }
    } else {
        console.log(err);
    }
});