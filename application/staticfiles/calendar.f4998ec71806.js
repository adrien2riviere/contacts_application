
/* on instancie le jour d'aujourd'hui et ses parametres*/
today =  new Date()
var year = today.getFullYear()
var month = today.getMonth() /*var month = today.toLocaleString('default', { month: 'long' })*/
var day = today.getDate() /*var weekday = today.toLocaleDateString(locale, { weekday: 'long' })*/

/* on peut enlever +6 et -1 mois facilement pour faire une liste de dates*/
d = new Date(year, month, day)
dates = []
for (let i = -1; i <= 6; i++) {
    date = new Date(year, month+i, 1)
    dates.push(date)
}

/* on utilise le dernier tr pour rechercher des ptés puis on enlève le tr */
let tr_last = document.getElementsByTagName('tr')[7]
let td_list = tr_last.getElementsByTagName('td')
date_list = []
text_list = []
id_list = []
for (let i = 0; i < td_list.length; i++) {
    p_list = td_list[i].getElementsByTagName('p')
    id_value = parseInt(p_list[0].innerText)
    id_list.push(id_value)
    year_value = parseInt(p_list[1].innerText), month_value = parseInt(p_list[2].innerText), day_value = parseInt(p_list[3].innerText)
    date_value = new Date(year_value, month_value-1, day_value) 
    date_list.push(date_value)
    text_list.push(p_list[4].innerText)
}
tr_last.remove()

/* afficher le mois et l'année*/
i_date = 1
var dateindique = document.getElementById("date");
dateindique.innerText = dates[1].toLocaleString('en-GB', { month: 'long' }) + ' ' + dates[1].getFullYear();
var pageindique = document.getElementById("page_numero");
pageindique.innerText = '';
/* boutons associés*/
function previous(){
    if(i_date > 0){
        i_date -= 1
        dateindique.innerText = dates[i_date].toLocaleString('en-GB', { month: 'long' }) + ' ' + dates[i_date].getFullYear();
    }
    if(i_date == 0){
        pageindique.innerText = '(' + String(i_date-1) + ')';
    }
    if(i_date == 1){
        pageindique.innerText = '';
    }
    if(i_date > 1){
        pageindique.innerText = '(+' + String(i_date-1) + ')';
    }
    completer()
}
function next(){
    if(i_date < 7){
        i_date += 1
        dateindique.innerText = dates[i_date].toLocaleString('en-GB', { month: 'long' }) + ' ' + dates[i_date].getFullYear();
    }
    if(i_date == 0){
        pageindique.innerText = '(' + String(i_date-1) + ')';
    }
    if(i_date == 1){
        pageindique.innerText = '';
    }
    if(i_date > 1){
        pageindique.innerText = '(+' + String(i_date-1) +')';
    }
    completer()
}  

completer()
/*créer la fonction completer pour remplir le calendrier par des numéros */
function completer(){
    var td_list2 = document.getElementsByTagName("td");
    let i_day = 0;
    let active = false;
    /*d = new Date(dates[i_date].getFullYear(), dates[i_date].getMonth(), 1) */
    for(let i = 0; i < td_list2.length; i++){
        td_element = td_list2[i]
        if(dates[i_date].getDay() <= i+1){
            active = true;
        }
        if(i_day+1 > 28 && dates[i_date].getMonth() == 1 && (dates[i_date].getFullYear() - 1972)%4 !=0){
            active = false;
        }
        if(i_day+1 > 29 && dates[i_date].getMonth() == 1 && (dates[i_date].getFullYear() - 1972)%4 == 0){
            active = false;
        }
        if(i_day+1 > 30 && [3,5,8,10].includes(dates[i_date].getMonth())){
            active = false;
        }
        if(i_day+1 > 31){
            active = false;
        }
        if(active == false){
            td_element.className = 'unused_case';
            span_numero = td_element.getElementsByTagName('span')[0]
            span_numero.innerText = '';
            div_text = td_element.getElementsByClassName('task_text')[0]
            div_text.innerText = ''
            span_element = td_element.getElementsByTagName('span')[0]
            span_element.className = 'numero'
        }
        if(active){
            i_day += 1
            td_element.className = 'futur_case';
            span_numero = td_element.getElementsByTagName('span')[0]
            span_numero.innerText = i_day;
            div_text = td_element.getElementsByClassName('task_text')[0]
            div_text.innerText = '';
            span_element = td_element.getElementsByTagName('span')[0]
            span_element.className = 'numero'
            colorer(td_element, i_day)
            add_task(td_element, i_day, dates[i_date].getMonth(), dates[i_date].getFullYear())
        }
    }
}

/*Attribuer les noms de classe adéquates pourla mise en forme des cases du calendrier */
function colorer(td_element, i_day){
    if(dates[i_date].getFullYear() < today.getFullYear()){
        td_element.className = 'past_case';
    }
    if(dates[i_date].getFullYear() == today.getFullYear() && dates[i_date].getMonth() < today.getMonth()){
        td_element.className = 'past_case';
    }
    if(dates[i_date].getFullYear() == today.getFullYear() && dates[i_date].getMonth() == today.getMonth()){
        if(i_day < today.getDate()){
            td_element.className = 'past_case';
        }
    }
    if(dates[i_date].getMonth() == today.getMonth() && dates[i_date].getFullYear() == today.getFullYear()){
        if(i_day == today.getDate()){
            td_element.className = 'today';
        }
    }
}

/*Ajouter les evénements dans les cases du calendrier */
function add_task(td_element, i_day, i_month, i_year){
    for(let i = 0; i < td_list.length; i++){
        event_day = date_list[i].getDate(), event_month = date_list[i].getMonth(), event_year = date_list[i].getFullYear()
        div_text = td_element.getElementsByClassName('task_text')[0]
        if(i_month == event_month && i_year == event_year && i_day == event_day){
            div_text.innerText = text_list[i]
            has_event(true, td_element)
            break;
        }
        else{
            div_text.innerText = ''
            has_event(false, td_element)
        }
    }
}
/*Mettre en couleur les jours associés à un évenement */
function has_event(bool, td_element){
    span_element = td_element.getElementsByTagName('span')[0]
    if(bool == true){
        span_element.className = 'numero day_with_task'
    }
    else{
        span_element.className = 'numero'
    }
}

/* définir la redirection quand on clique sur une case */
document.getElementsByTagName('tbody')[0].onclick = click_redirection;
function click_redirection(e) {
    ii = i_date
    ext = ''
    /* vers page noEvent */
    if(e.target.className == 'past_case' && e.target.getElementsByClassName('task_text')[0].innerText == ''){
        window.location.pathname = "/calendar/noEvent" + "/" + i_date;
    }
    if(e.target.parentNode.className == 'past_case' && e.target.parentNode.getElementsByClassName('task_text')[0].innerText == ''){
        window.location.pathname = "/calendar/noEvent" + "/" + i_date;
    }
    /* vers page eventDetails */
    if(e.target.className == 'past_case' && e.target.getElementsByClassName('task_text')[0].innerText != ''){
        for(let i = 0; i < td_list.length; i++) {
            check_value = 0
            if(date_list[i].getFullYear() == dates[ii].getFullYear()){
                check_value +=1;
            }
            if(date_list[i].getMonth() == dates[ii].getMonth()){
                check_value +=1;
            }
            if(date_list[i].getDate() == e.target.getElementsByClassName('numero')[0].innerText){
                check_value +=1;
            }
            if(check_value == 3){
                ext = String(id_list[i])
                break;
            }
        }
        window.location.pathname = "/calendar/eventDetails/" + ext + "/" + i_date;
    }
    if(e.target.parentNode.className == 'past_case' && e.target.parentNode.getElementsByClassName('task_text')[0].innerText != ''){
        for(let i = 0; i < td_list.length; i++) {
            check_value = 0
            if(date_list[i].getFullYear() == dates[ii].getFullYear()){
                check_value +=1;
            }
            if(date_list[i].getMonth() == dates[ii].getMonth()){
                check_value +=1;
            }
            if(date_list[i].getDate() == e.target.parentNode.getElementsByClassName('numero')[0].innerText){
                check_value +=1;
            }
            if(check_value == 3){
                ext = String(id_list[i])
                break;
            }
        }
        window.location.pathname = "/calendar/eventDetails/" + ext + "/" + i_date;
    }
    /* vers page addEvent */
    if(['futur_case', 'today'].includes(e.target.className) && e.target.getElementsByClassName('task_text')[0].innerText == ''){
        date = dates[ii]
        date.setDate(e.target.getElementsByClassName('numero')[0].innerText)
        ext = date.toLocaleString('fr-FR', ).replaceAll("/", "-").slice(0, 10);
        window.location.pathname = "/calendar/addEvent/" + ext + "/" + i_date;
    }
    if(['futur_case', 'today'].includes(e.target.parentNode.className) && e.target.parentNode.getElementsByClassName('task_text')[0].innerText == ''){
        date = dates[ii]
        date.setDate(e.target.parentNode.getElementsByClassName('numero')[0].innerText)
        ext = date.toLocaleString('fr-FR', ).replaceAll("/", "-").slice(0, 10);
        window.location.pathname = "/calendar/addEvent/" + ext + "/" + i_date;
    }
    /* vers page manageEvent */
    if(['futur_case', 'today'].includes(e.target.className) && e.target.getElementsByClassName('task_text')[0].innerText != ''){
        for(let i = 0; i < td_list.length; i++) {
            check_value = 0
            if(date_list[i].getFullYear() == dates[ii].getFullYear()){
                check_value +=1;
            }
            if(date_list[i].getMonth() == dates[ii].getMonth()){
                check_value +=1;
            }
            if(date_list[i].getDate() == e.target.getElementsByClassName('numero')[0].innerText){
                check_value +=1;
            }
            if(check_value == 3){
                ext = String(id_list[i])
                break;
            }
        }
        window.location.pathname = "/calendar/manageEvent/" + ext + "/" + i_date;
    }
    if(['futur_case', 'today'].includes(e.target.parentNode.className) && e.target.parentNode.getElementsByClassName('task_text')[0].innerText != ''){
        for(let i = 0; i < td_list.length; i++) {
            check_value = 0
            if(date_list[i].getFullYear() == dates[ii].getFullYear()){
                check_value +=1;
            }
            if(date_list[i].getMonth() == dates[ii].getMonth()){
                check_value +=1;
            }
            if(date_list[i].getDate() == e.target.parentNode.getElementsByClassName('numero')[0].innerText){
                check_value +=1;
            }
            if(check_value == 3){
                ext = String(id_list[i])
                break;
            }
        }
        window.location.pathname = "/calendar/manageEvent/" + ext + "/" + i_date;
    }
}

/* retour sur la bonne page */
i_element = window.location.href.slice(-1)
if(i_element == 0){
    previous()
}
if(i_element > 1){
    for(let i = 1; i < i_element; i++){
        next()
    }
}

/* responsive for telephone and tablette*/
let width = screen.width;
if(width < 650){
    day_head_list = ['Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.', 'Sun.']
    th_head_list = document.getElementsByTagName('th')
    for(let i = 0; i < th_head_list.length; i++){
        th_head_list[i].innerText = day_head_list[i]
    }
}
window.addEventListener("resize", calendar_responsive);
function calendar_responsive(){
    let width = screen.width;
    if(width < 650){
        short_day_list = ['Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.', 'Sun.']
        th_head_list = document.getElementsByTagName('th')
        for(let i = 0; i < th_head_list.length; i++){
            th_head_list[i].innerText = short_day_list[i]
        }
    }
    else{
        long_day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        th_head_list = document.getElementsByTagName('th')
        for(let i = 0; i < th_head_list.length; i++){
            th_head_list[i].innerText = long_day_list[i]
        }
    }
}