var true_element = true;

function reservefunc(){
    if (true_element){
    var div_element = document.getElementById('reserve_id');
    var input_date = document.createElement('input');
    input_date.setAttribute('type', 'date');
    input_date.setAttribute('id', 'reserve_date');
    div_element.appendChild(input_date);
    var input_button = document.createElement('input');
    input_button.setAttribute('type', 'button');
    input_button.setAttribute('value', 'Ok');
    input_button.setAttribute('onclick', 'get_date()');
    div_element.appendChild(input_button);
    true_element = false;
    }
}

function get_date(){
    var reserve_date = document.getElementById('reserve_date').value;
    var div_element = document.getElementById('reserve_id');
    var span_element = document.createElement('span');
    var span_text = document.createTextNode(
        'Дата введена не корректно. Выберите дату в диапозоне 5 дней от нынешней даты'
        );
    span_element.appendChild(span_text)
    date_of_issue = new Date(reserve_date);
    date_of_issue.setHours(0,0,0,0)
    var book_id = document.URL.slice(-1);
    console.log(book_id); 
    var today = new Date();
    today.setHours(0,0,0,0);
    var number_of_days_to_add = 5;
    var last_day = new Date(today.getTime())
    last_day.setDate(last_day.getDate() + number_of_days_to_add)
    if (date_of_issue >= today && date_of_issue <= last_day){
        console.log(date_of_issue)
        post_info(date_of_issue, book_id)
        return date_of_issue
    } else {
        div_element.appendChild(span_element);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function post_info(date_of_issue, book_id){
    // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    date = new Date()
    var post_body = JSON.stringify({
        'date_of_issue': date_of_issue,
        'book_id': book_id
    })
    fetch('/reservation/',
    {
        method: 'POST',
        body: post_body,
        headers: {
            'X-CSRFTOKEN': csrftoken,
            'Accept': 'text/html',
            'Content-Type': 'application/json'
        }
    }).then(
        response =>{
            console.log(response)
            return response;
        }
    ).then(
        response =>{
            data_json =>console.log(data_json.status);
        }
    ).catch(
        error=>{
            console.log(error)
        }
    )
}