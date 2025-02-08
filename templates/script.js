document.addEventListener('DOMContentLoaded', function() {
    let filters = document.querySelectorAll(".filter-option");
    let filterreset = document.getElementById("filter0");
    let selectedFilters = new Set();

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
                console.log("Help");
                filter.classList.toggle("select");
            }
        });
        if (noneSelected()) {
            filterreset.classList.add("select");
        }
    })
});