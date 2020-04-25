document.addEventListener("DOMContentLoaded", function () {
    //personal-info ajax form submit
    $("#personal-info-form").submit((event) => {
        fdata = {};
        $.each($("#personal-info-form input"), (index, el) => {
            // console.log(el);
            // console.log(el.val());
            fdata[$(el).attr("name")] = $(el).val();
        });
        fdata["pinfo-gender"] = $(
            "#personal-info-form select[name=pinfo-gender] option:selected"
        ).val();
        console.log(fdata);
        $.ajax({
            method: "POST",
            url: "/amu/avatar/",
            data: fdata,
            success: (result) => {
                console.log(result);
            },
        });
        $("#personal-info-form").trigger("reset");
        event.preventDefault();
    });

    //personal details form clear
    $("#pinfo-clear-btn").click(() => {
        $("personal-info-form").trigger("reset");
    });

    //work details form submit
    $("#work-details-form").submit((event) => {
        fdata = {};
        $.each($("#work-details-form input"), (index, el) => {
            fdata[$(el).attr("name")] = $(el).val();
        });
        fdata["wd-avatar"] = $(
            "#work-details-form select[name=wd-avatar] option:selected"
        ).val();
        fdata["wd-current-job"] = $(
            "#work-details-form input[name=wd-current-job]"
        ).is(":checked");
        console.log(fdata);
        $.ajax({
            method: "POST",
            url: "/amu/addwork/",
            data: fdata,
            success: (result) => {
                console.log(result);
            },
        });
        $("#work-details-form").trigger("reset");
        event.preventDefault();
    });

    // work details form clear
    $("wd-clear-btn").click(() => {
        $("#work-details-form").trigger("reset");
    });
});
