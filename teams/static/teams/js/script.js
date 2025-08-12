

window.onload = insertDateTime;


function insertDateTime() {
  now = new Date();
  DateTime = now.toLocaleString();
  document.getElementById('output').innerHTML = DateTime


}
let count=0;
function newCount(){
  count++;

}






