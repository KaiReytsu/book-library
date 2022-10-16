function redirecturl(){
    window.location.href="/catalog/";
}

function hidebutton(date_id){
    var today = new Date()
    date_id.setAttribute('id', today);
}