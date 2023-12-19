document.addEventListener('DOMContentLoaded', function() {
    var modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));

    // Adiciona um ouvinte de evento ao modal quando é mostrado
    modal._element.addEventListener('show.bs.modal', function() {
        // Atualiza o valor do campo idbuao com o mesmo valor do campo oculto id
        var idbuaoInput = document.getElementById('idbuao');
        var idInput = document.getElementsByName('id')[0];

        if (idInput && idbuaoInput) {
            idbuaoInput.value = idInput.value;
        }
    });
});