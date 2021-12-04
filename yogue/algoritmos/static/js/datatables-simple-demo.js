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
    const datatableCorr = document.getElementById('datatableCorr');
    if (datatableCorr) {
        new simpleDatatables.DataTable(datatableCorr,{searchable:false});
    }
    const datatableCluster = document.getElementById('datatableCluster');
    if (datatableCluster) {
        var table = new simpleDatatables.DataTable(datatableCluster,{searchable:false});
        
    }
    const datatableClasif = document.getElementById('datatableClasif');
    if (datatableClasif) {
        var table = new simpleDatatables.DataTable(datatableClasif,{searchable:false});
        
    }
});
