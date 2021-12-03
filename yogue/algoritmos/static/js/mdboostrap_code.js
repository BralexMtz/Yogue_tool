// Without JQuery
window.addEventListener('DOMContentLoaded', event => {
    var slider = document.getElementById("customRange1");
    slider.oninput = function(sliderValue) {
        document.getElementById("numClustersSliderVal").innerHTML = slider.value;
    }

});
