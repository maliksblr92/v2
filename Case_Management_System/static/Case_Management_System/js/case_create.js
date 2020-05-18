document.addEventListener("DOMContentLoaded", () => {
    // case creation form
    let cc_form = "#case-creation-form";
    $(cc_form).submit((event) => {
        let form_data = $(cc_form).serializeArray();
        console.log(form_data);
        $.ajax({
            url: "/cms/create/",
            method: "POST",
            data: form_data,
            success: (result) => {
                console.log(result);
                $(cc_form).trigger("reset");
            },
        });
        event.preventDefault();
    });
    // location information form
    //evidence form
    //person of interest form
});
