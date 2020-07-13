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
    delbtn.click((event) => {
        const docIdVar = $(".pill-selected > input[type=hidden]").val();
        if (docIdVar) {
            const propToDeleteVar = $(".pill-selected > .keybaseLabel").text();
            console.log(propToDeleteVar);
            $.ajax({
                url: "/kms/delprop/",
                method: "POST",
                dataType: "json",
                data: {
                    csrfmiddlewaretoken: $(
                        "input[name=csrfmiddlewaretoken]"
                    ).val(),
                    docId: docIdVar,
                    propToDelete: propToDeleteVar,
                },
                success: (result) => {
                    console.log(result);
                    $(".pill-selected").parent().remove();
                },
            });
        }
    });
    editbtn.click((event) => {
        const docId = $(".pill-selected > input[type=hidden]").val();
        console.log(docId);
        if (docId) {
            window.location.replace(`/kms/edit/?docId=${docId}`);
        }
    });
});
