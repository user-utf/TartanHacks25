document.addEventListener('DOMContentLoaded', function() {
    let filters = document.querySelectorAll(".filter-option");
    let filterreset = document.getElementById("filter0");
    let whitebuttons = document.querySelectorAll(".leftbuttons");

    function noneSelected() {
        for (let filter of filters) {
            if (filter.classList.contains("select")) {
                return false;
            }
        }
        return true;
    }

    document.addEventListener('click', function(event) {
        if (document.getElementById("dropbtn").contains(event.target)) {
            document.getElementById("dropdown-content").classList.toggle("show");
        } else if (document.getElementById("dropdown-content").contains(event.target)){
            document.getElementById("dropdown-content").classList.add("show");
        } else {
            document.getElementById("dropdown-content").classList.remove("show");
        }
        if (filterreset.contains(event.target)) {
            filters.forEach(filter => {
                filter.classList.remove("select");
            });
            filterreset.classList.toggle("select");
        }
        filters.forEach(filter => {
            if (filter.contains(event.target)) {
                filter.classList.toggle("select");
            }
        });
        if (noneSelected()) {
            filterreset.classList.add("select");
        }
        whitebuttons.forEach(buttons => {
            if (buttons.contains(event.target)) {
                console.log("help");
                document.getElementById("loadingscreen").classList.add("load");
            }
        });
    })

    window.onload = function() {
        document.getElementById("loadingscreen").classList.remove("load");
        if (document.getElementById("artist-pic").src.indexOf("no") != -1 || !document.getElementById("artist-pic").src) {
            document.getElementById("artist-box").classList.add("hide");
        }
        if (document.getElementById("artist-desc").innerHTML == "no" || !document.getElementById("artist-desc").src) {
            document.getElementById("artist-desc").classList.add("hide");
        }
    };    
});