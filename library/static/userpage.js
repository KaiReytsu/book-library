document.addEventListener("DOMContentLoaded", todelete);

function todelete() {
  var td_element = document.getElementsByTagName("td");
  var div_leme = document.querySelector(".usernamediv");
  console.log(div_leme);
  for (var i = 0; i < td_element.length; i++) {
    if (td_element[i].innerHTML == "забронировано") {
      createbutton(td_element[i]);
    } else if (td_element[i].innerHTML == "просрочено") {
      td_element[i].parentNode.style.color = "red";
      var dialog = document.querySelector("dialog");
      var dialog_text = document.getElementById("dialog_text");
      var yesbutton = document.getElementById("yes");
      yesbutton.innerHTML = "Понятно";
      dialog_text.innerHTML =
        "Срок возврата книги, которую вы взяли в библиотеке прошел, просьба вернуть как можно скорее";
      dialog.showModal();
      yesbutton.onclick = function () {
        dialog.close();
      };
      document.querySelector("#no").style.display = "None";
    }
  }
}

function createbutton(element) {
  var delete_button = document.createElement("button");
  var button_text = document.createElement("span");
  delete_button.setAttribute("class", "delete_button");
  delete_button.setAttribute("onclick", "opendialog(this)");
  button_text.setAttribute("id", "boot-icon");
  button_text.setAttribute("class", "bi bi-trash");
  delete_button.appendChild(button_text);
  element.appendChild(delete_button);
}

function opendialog(element) {
  var dialog = document.querySelector("dialog");
  var res_id = element.parentNode.parentNode.lastElementChild.innerHTML;
  dialog.showModal();
  document.querySelector("#no").onclick = function () {
    dialog.close();
  };
  document.querySelector("#yes").onclick = function () {
    post_info(res_id)
      .then(() => {
        dialog.close();
        window.location.reload();
      })
      .catch((error) => {
        console.log(error);
        alert(
          "Во время удаления возникла ошибка. Обратитесь к администратору по адресу mail@lib.com"
        );
      });
  };
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

function post_info(res_id) {
  var post_body = JSON.stringify({
    id: res_id,
  });
  return fetch("/profile/", {
    method: "POST",
    body: post_body,
    headers: {
      "X-CSRFTOKEN": csrftoken,
      Accept: "text/html",
      "Content-Type": "application/json",
    },
  });
}
