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
            if (td || td2) {
                txtValue = td.textContent || td.innerText;
                txtValue2 = td2.textContent || td2.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } 
                else if (txtValue2.toUpperCase().indexOf(filter) > -1){
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                }
            }      
        }
}

/*pagination ??? >>>> echec !!!!!
var tr_list = [];
for (i = 0; i < tr_list.length; i++) {
    if (tr[i].style.display=='') {
        tr_list += tr[i]
    }
}
nb_pages = Math.floor(tr_list.length/2);
var div = document.getElementById('pagination');
for (i = 0; i < nb_pages; i++) {
    let els = document.createElement('button');
    let content = document.createTextNode(String(i));
    els.appendChild(content);
    div.appendNode(els);
}*/

/*
function deletePopUp() {
    var win = window.open(href=http://127.0.0.1:8000/contacts/deleteContact, height=400, width=400, resizable=yes);
    win.focus();
    return false;
}*/