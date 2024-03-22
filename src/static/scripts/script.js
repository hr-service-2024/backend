document.addEventListener('DOMContentLoaded', () => {
    const but1 = document.querySelector(".send_button");
    const but2 = document.querySelector(".regen");

    if (but1 != null && but2 != null) {
        but1.onclick = function(){
            var text = document.querySelector(".description").value;
            document.querySelector("#in1").value = text;
            document.querySelector("#in2").value = text;
        }
        but2.onclick = function(){
            var text = document.querySelector(".description").value;
            document.querySelector("#in1").value = text;
            document.querySelector("#in2").value = text;
        }
    }
});