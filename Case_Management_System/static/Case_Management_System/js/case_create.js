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
    // location details form
    let ld_form = "#location-details-form";
    $(ld_form).submit((event) => {
        let form_data = $(ld_form).serializeArray();
        console.log(form_data);
        $.ajax({
            url: "/cms/location/",
            method: "POST",
            data: form_data,
            success: (result) => {
                console.log(result);
                $(ld_form).trigger("reset");
            },
        });
        event.preventDefault();
    });
    //evidence form
    //person of interest form
});
