var table = document.getElementById('table');
selected = table.getElementsByClassName('selected');
table.onclick = highlight;
function highlight(e) {
    if(e.target.parentNode.className == '') {
        if (selected[0]) selected[0].className = '';
        if (e.target.parentNode.tagName == 'TR') e.target.parentNode.className = 'selected';
    }
    else if(e.target.parentNode.className == 'selected'){
        if (selected[0]) selected[0].className = '';
    }
}

function filter() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            td2 = tr[i].getElementsByTagName("td")[1];
            td3 = tr[i].getElementsByTagName("td")[2];
            if (td || td2 || td3) {
                txtValue = td.textContent || td.innerText;
                txtValue2 = td2.textContent || td2.innerText;
                txtValue3 = td3.textContent || td3.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                }
                else if (txtValue2.toUpperCase().indexOf(filter) > -1){
                    tr[i].style.display = "";
                }
                else if (txtValue3.toUpperCase().indexOf(filter) > -1){
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                }
            }      
        }
}