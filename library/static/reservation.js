function reservefunc(){
    var reserv_date = document.getElementById('reserv_date');
    var show = document.getElementById('show');
        reserv_date.style.display = 'block';
        var today = new Date()
        var month = today.getUTCMonth() + 1;
        var day = today.getUTCDate();
        var year = today.getUTCFullYear();
        today.setHours(0,0,0,0);
        var number_of_days_to_add = 5;
        var last_date = new Date(today.getTime())
        last_date.setDate(last_date.getDate() + number_of_days_to_add)
        var last_month = last_date.getUTCMonth() + 1;
        var last_day = last_date.getUTCDate();
        var last_year = last_date.getUTCFullYear();
        reserv_date.setAttribute('min', ( year+ "-" +  month + "-" +day));
        reserv_date.setAttribute('max', (last_year + "-" + last_month + "-" +last_day ));
        reserv_date.setAttribute('value', ( year+ "-" +  month + "-" +day));
        show.style.display = 'block';
    }

function get_date(){
    var reserve_date = document.getElementById('reserv_date').value;
    var div_element = document.getElementById('reserve_id');
    var span_element = document.createElement('span');
    var span_text = document.createTextNode(
        'Дата введена не корректно. Выберите дату в диапозоне 5 дней от нынешней даты'
        );
    span_element.appendChild(span_text)
    date_of_issue = new Date(reserve_date);
    date_of_issue.setHours(0,0,0,0)
    var book_id = document.URL.split('/').slice(-2)[1];
    console.log(book_id)
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
        response =>
            response.json()
    ).then(
        data =>{
            var dialog = document.querySelector('dialog');
            if (data.res_status){
                var text = document.getElementById('dialog_text')
                text.innerHTML = 'Вы уже бронировали эту книгу, но ещё не вернули её.' + ' ' +
                                    'Эту книгу можно забронировать вновь при возврате предыдущей'
                dialog.showModal();

            } else {
                var month_names = ["янв", "фев", "мар", "апр", "мая", "июня",
                                "июля", "авг", "сен", "окт", "ноя", "дек"
                                ];
                date = data.reservation_date_of_return.split('-');           
                document.getElementById('return_date').innerHTML = date[2] + ' ' + month_names[date[1] - 1] + ' ' + date[0];
                document.getElementById('res_id').innerHTML = data.reservation_id;
                dialog.showModal();
            }
            document.querySelector('#close').onclick = function() {
                window.location.reload();
                dialog.close();
            };}
    ).catch(
        error=>{
            console.log(error)
        }
    )
}