// attach ready event
$(document).ready(function () {

    // close message on click
    $('.message .close').on('click', function () {
        $(this).closest('.message').transition('fade');
    });

    // show dropdown on hover
    $('#profile-dropdown').dropdown({
        on: 'hover'
    });

    $('.small.modal')
        .modal('attach events', '#delete_account', 'show');

    $('input:text, .ui.button', '.ui.action.input')
        .on('click', function (e) {
            $('input:file', $(e.target).parents()).click();
        });

    $('input:file', '.ui.action.input')
        .on('change', function (e) {
            var name = e.target.files[0].name;
            $('input:text', $(e.target).parent()).val(name);
        });

});