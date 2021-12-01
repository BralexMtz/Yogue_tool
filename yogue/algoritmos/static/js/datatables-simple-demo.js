window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple,{searchable:false});
    }
    const datatablesFrecuency = document.getElementById('datatableFrecuency');
    if (datatablesFrecuency) {
        new simpleDatatables.DataTable(datatablesFrecuency,{searchable:false});
    }
    const datatableDistance = document.getElementById('datatable_dist');
    if (datatableDistance) {
        new simpleDatatables.DataTable(datatableDistance,{searchable:false});
    }
});
