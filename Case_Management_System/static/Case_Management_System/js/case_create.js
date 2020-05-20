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
    //virtual evidence form
    let ve_form = "#virtual-evidence-form";
    $(ve_form).submit((event) => {
        let form_data = $(ve_form).serializeArray();
        console.log(form_data);
        $.ajax({
            url: "/cms/virtualevidence/",
            method: "POST",
            data: form_data,
            success: (result) => {
                console.log(result);
                $(ve_form).trigger("reset");
            },
        });
        event.preventDefault();
    });

    //physical evidence form
    let pe_form = "#physical-evidence-form";
    $(pe_form).submit((event) => {
        let form_data = $(pe_form).serializeArray();
        console.log(form_data);
        $.ajax({
            url: "/cms/physicalevidence/",
            method: "POST",
            data: form_data,
            success: (result) => {
                console.log(result);
                $(pe_form).trigger("reset");
            },
        });
        event.preventDefault();
    });

    // person of interest form
    let poi_form = "#poi-form";
    $(poi_form).submit((event) => {
        let form_data = $(poi_form).serializeArray();
        console.log(form_data);
        $.ajax({
            url: "/cms/poi/",
            method: "POST",
            data: form_data,
            success: (result) => {
                console.log(result);
                $(poi_form).trigger("reset");
            },
        });
        event.preventDefault();
    });
});
