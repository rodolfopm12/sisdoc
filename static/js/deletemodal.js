    $('body').on('click', '.modal-eliminar', function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();

        $('#modal-eliminar #modal-url').attr('href', $(this).attr('href'));
        $('#modal-eliminar #modal-descripcion').html($(this).data('description'));
        $('#modal-eliminar').modal('show');
    });

    $('body').on('click', '#modal-url', function(event) {
        $('#deletemodal').modal('hide');
    });