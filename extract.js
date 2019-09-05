const DomParser = require('dom-parser');
const request = require('sync-request');
var parser = new DomParser();

var fs = require('fs');

let companies = new Set();
let regexes = {
    'companyLink': /(https:\/\/www\.jobs\.bg\/company\/[0-9]+)/g,
    'companyId': {
        exec: function(str) {
            return str.substring(28);
        }
    },
    'companyLogo': {
        exec: function(str) {
            let answer = '';
            for (let i = str.indexOf('https://assets.jobs.bg/assets/logo/') ; str [i] != '"' ; i += 1)
                answer += str [i];
            return answer;
        }
    },
    'contacts': {
        'exec': function(str) {
            let answer = '';
            let i = 0;
            for ( ; str.substring(i, i + 'Контакти'.length) != 'Контакти' ; i += 1){}
            for ( ; str.substring(i, i + 4) != '</td>' ; i += 1)
                answer += str[i];
            return answer;
        }
    }
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
    console.log('TRYING: Company', companyLink);
    const dom = parser.parseFromString(html);

    let id = regexes.companyId.exec(companyLink);
    // console.log('id =', id);
    let uid = gen_code();
    // console.log('uid =', uid);

    let name = dom.getElementsByTagName('h1')[0].innerHTML;
    // console.log('name =', name);
    let description = dom.getElementsByClassName('htmlTemplate')[0].innerHTML;
    // console.log('logo regex =', regexes.companyLogo.exec(html));
    let logo = regexes.companyLogo.exec(html);
    let website = '(Няма въведена интернет страница на фирмата)';
    let contacts = '(Няма въведена информация за фирмата';

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
        console.log('TRYING: Job    ', job);
        const dom = parser.parseFromString(html);
        try {
            let jobTitle = dom.getElementsByTagName("b")[2].innerHTML;

            let companyLink = regexes.companyLink.exec(html)[1];
            let companyId = regexes.companyId.exec(companyLink)[1];
            try {
                let company = company_deparse(companyLink);
                console.log("RESULT|COMPANY:", JSON.stringify(company));
                fs.open('companies.txt', 'a', (err, fd) => {
                    if (err) throw err;
                    fs.appendFile(fd, JSON.stringify(company) + '\n', 'utf8', (err) => {
                        fs.close(fd, (err) => {
                            if (err) throw err;
                        });
                        if (err) throw err;
                    });
                });
            } catch (e) {
                console.log('ERROR: Company', companyLink, 'creation failed.');
            }

            let jobLocation = dom.getElementsByTagName("td")[10].innerHTML.split(';')[0].substring(12);

            let jobAddedTags = dom.getElementsByTagName("td")[10].innerHTML.split(';').map((x) => '&lt;' + x + '&gt;').join(' ');

            let jobDescription = dom.getElementsByTagName("td")[12].innerHTML + '<br><br>' + jobAddedTags;

            let job_obj = {
                'id': job,
                'job-title': jobTitle,
                'email': 'contact_us@headstarter.eu',
                'location': jobLocation,
                'company_id': companyId,
                'description': jobDescription,
                'job-available': false,
                'duration': 12,
                'job-type': '8ч.',
                'job-age': '18+',
                'job-category': '58'
            };

            console.log("RESULT|JOB:", JSON.stringify(job_obj));

            fs.open('jobs.txt', 'a', (err, fd) => {
                if (err) throw err;
                fs.appendFile(fd, JSON.stringify(job_obj) + '\n', 'utf8', (err) => {
                    fs.close(fd, (err) => {
                        if (err) throw err;
                    });
                    if (err) throw err;
                });
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
            console.log('SUCCESS: job', job, 'is generated');
        } catch (e) {
            console.log('ERROR: job', job, 'can\'t be gathered', e);
        }
    } catch (e) {
        console.log('ERROR: job', job, 'can\'t be gathered', e);
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