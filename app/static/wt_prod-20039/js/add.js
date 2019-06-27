$(document).ready(function() {
    $('#blank_lang, #blank_edu, #blank_project, #blank_skill, #blank_hobby').append(`
    <a href="#todo" onclick="$(this).parent().remove();" class="remove">− Премахни</button>
    `);
    let elements = ['lang', 'edu', 'project', 'skill', 'hobby'];
    for (let i = 0 ; i < elements.length ; i += 1) {
        $(".add_" + elements[i]).click(function() {
            $("#blank_" + elements[i]).parent().append($("#blank_" + elements[i])[0].outerHTML.replace('id="blank_' + elements[i] + '"', ''));
            $(".form-input").change(function(){
                let sections = ['language', 'education', 'project', 'skill', 'hobby'];
                let json_out = ['languages', 'education', 'projects', 'skills', 'hobbies'];
                for (let i = 0 ; i < sections.length ; i += 1) {
                    //console.log($('#' + sections [i] + '_list'));
                    let e = $('#' + sections [i] + '_list').find("div.rd-form.rd-mailform.form-lg.form-corporate");
                    let arr = [];
                    for (let i = 1 ; i < e.length ; i += 1) {
                        arr[i-1] = $(e[i]).find('.form-input').serializeArray().reduce((data, x) => { data[x.name]=x.value; return data; }, {});
                    }
                    //console.log(arr);
                    $('[name=' + json_out [i] + ']').val(JSON.stringify(arr));
                }
            });
        });
    }

});