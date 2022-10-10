document.addEventListener("DOMContentLoaded", todelete);

function todelete(){
    var td_element = document.getElementsByTagName("td");
    for(var i = 0; i < td_element.length; i++){
        if (td_element[i].innerHTML == 'забронировано'){
            var delete_button = document.createElement('button');
            // delete_button.setAttribute('type', 'button');
            delete_button.setAttribute('class', 'delete_button');
            // delete_button.setAttribute('value', 'Отменить бронирование');
            delete_button.setAttribute('onclick', 'opendialog(this)');
            var button_text = document.createElement('span');
            button_text.setAttribute('id', 'boot-icon');
            button_text.setAttribute('class', 'bi bi-trash');
            delete_button.appendChild(button_text);
            td_element[i].appendChild(delete_button);
        }
    }
}

function opendialog(element){
    var dialog = document.querySelector('dialog');
    var res_id = element.parentNode.parentNode.lastElementChild.innerHTML;
    dialog.showModal();
    document.querySelector('#no').onclick = function() {
        dialog.close();
    };
    document.querySelector('#yes').onclick = function() {
        post_info(res_id).then((
        )=>{
            dialog.close();
            window.location.reload();
        }).catch(error => {
            console.log(error);
            alert('Во время удаления возникла ошибка. Обратитесь к администратору по адресу mail@lib.com')
        })
        
    };
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function post_info(res_id){
    var post_body = JSON.stringify({
        'id': res_id,
    })
    return fetch('/profile/',
    {
        method: 'POST',
        body: post_body,
        headers: {
            'X-CSRFTOKEN': csrftoken,
            'Accept': 'text/html',
            'Content-Type': 'application/json'
        }
    })
}