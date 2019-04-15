$(document).ready(function() {
    $("ul.list.form-control li:not(.add)").append(`
        <a onclick="$(this).parent('li').remove();" class="btn btn-danger btn-raised">Изтрии</a><br>
    `);
});
