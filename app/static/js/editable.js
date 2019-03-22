

function hideModal(element) {
    element.removeClass("in");
    $(".modal-backdrop").remove();
    $('body').removeClass('modal-open');
    $('body').css('padding-right', '');
    element.hide();
    element.remove();
}
$(document).ready(function() {


  $('.summernote').summernote({
    lang: 'bg-BG' // default: 'en-US'
  });

  $('#submit').on('click', function () {
    function init_loading_modal () {
        $('body').append (`
        <div class="modal fade" id="loading" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" style="padding-right: 17px; display: block;">
		  <div class="modal-dialog" role="document">
			<div class="modal-content">
			  <div class="modal-header">
				<h5 class="modal-title" id="loading_label">Обработват се Вашите промени</h5>
				<button onclick='hideModal($("#loading"));' type="button" class="close">
				  <span aria-hidden="true">×</span>
				</button>
			  </div>
			  <div class="modal-body" id="loading_body">
<center>
			    <p> Моля, изчакайте! </p>
			      <i class="fas fa-spinner fa-pulse fa-10x"></i></center>
			  </div>
			  <div class="modal-footer">
				<button onclick='hideModal($("#loading"));' type="button" class="btn btn-secondary">Close</button>
			  </div>
			</div>
		  </div>
		</div>
        `);
        $('#loading').modal('show');
    }

    function init_end_modal (html) {
        $('body').append (`
        <div class="modal fade" id="changes_done" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" style="padding-right: 17px; display: block;">
		  <div class="modal-dialog" role="document">
			<div class="modal-content">
			  <div class="modal-header">
				<h5 class="modal-title" id="changes_done_label">Вашите промени бяха извършени:</h5>
				<button onclick='hideModal($("#changes_done"));' type="button" class="close">
				  <span aria-hidden="true">×</span>
				</button>
			  </div>
			  <div class="modal-body" id="changes_done_body">
` + html + `
			  </div>
			  <div class="modal-footer">
				<button onclick='hideModal($("#changes_done"));' type="button" class="btn btn-secondary">Close</button>
			  </div>
			</div>
		  </div>
		</div>
        `);
        $('#changes_done').modal('show');
    }
    init_loading_modal ();

    var end_modal = "";
    var updates_done = $('.summernote').length;
    $('.summernote').each (function (_) {
        var code = $(this).summernote ('code');
        var data_id = $(this).attr ('data-id');
        var data_name = $(this).attr ('data-name').replace('<p>', '').replace('</p>', '');

        $.post('/p/update', {
            code: code,
            id: data_id,
            name: data_name
        }).done(function(response) {
            console.log(response);
            console.log (response.value);
            end_modal += ('<p class="success">Променихте ' + data_name + ' успешно.</p>')
            updates_done -= 1;
        }).fail(function(response) {
            end_modal += ('<p class="danger">Не променихте ' + data_name + ': ' + response.status.toString () + '</p>')
            console.log (response.status);
            updates_done -= 1;
        });
    });

    var t;

    function modal_loading () {
        if (updates_done == 0) {
            hideModal($("#loading"));
            init_end_modal (end_modal);
            clearInterval(t);
        }
    }

    t = setInterval (modal_loading, 1000);
  });
});