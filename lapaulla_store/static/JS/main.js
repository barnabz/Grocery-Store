document.addEventListener("DOMContentLoaded", function () {
    const trigger = document.getElementById("accountTrigger");
    const menu = document.getElementById("accountMenu");

    if (trigger && menu) {
        trigger.addEventListener("click", function (e) {
            e.stopPropagation();
            menu.style.display = menu.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", function () {
            menu.style.display = "none";
        });
    }
});
