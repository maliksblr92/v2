document.addEventListener("DOMContentLoaded", function () {
    let pills = $(".pilleditdel");
    pills.click((event) => {
        $(".pill-selected").removeClass("pill-selected");
        if (event.target.parentElement.classList.contains("pilleditdel")) {
            event.target.parentElement.classList.add("pill-selected");
        }
    });
    let delbtn = $(".deletebutton");
    let editbtn = $(".editbutton");
    delbtn.click((event) => {});
    editbtn.click((event) => {
        const docId = $(".pill-selected > input[type=hidden]").val();
        console.log(docId);
        if (docId) {
            window.location.replace(`/kms/edit/?docId=${docId}`);
        }
    });
});
