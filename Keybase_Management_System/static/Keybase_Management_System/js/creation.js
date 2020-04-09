document.addEventListener("DOMContentLoaded", function() {
    //Adding

    $("#keywords").keypress(function(event) {
        //13 is ASCII Code for enter
        if (event.which === 13) {
            var task = $("input[name=keywords]").val();

            //append
            $("#forkeywords").append(
                "<span class='eachtag'>" +
                    task +
                    "<i class='delspan fas fa-trash-alt fa-1x tegicon'></i>"
            );
            $("#keywords").val("");
        }
        event.stopPropagation();
    });

    // for mentions
    $("#mentions").keypress(function(event) {
        //13 is ASCII Code for enter
        if (event.which === 13) {
            var task = $("input[name=mentions]").val();

            //append
            $("#formentions").append(
                "<span class='eachtag'>" +
                    task +
                    "<i class='delspan fas fa-trash-alt fa-1x tegicon'></i>"
            );
            $("#mentions").val("");
        }
        event.stopPropagation();
    });

    // for tags
    $("#tags").keypress(function(event) {
        //13 is ASCII Code for enter
        if (event.which === 13) {
            var task = $("input[name=tags]").val();

            //append
            $("#fortags").append(
                "<span class='eachtag'>" +
                    task +
                    "<i class='delspan fas fa-trash-alt fa-1x tegicon'></i>"
            );
            $("#tags").val("");
        }
        event.stopPropagation();
    });

    // for tags
    $("#phrase").keypress(function(event) {
        //13 is ASCII Code for enter
        if (event.which === 13) {
            var task = $("input[name=phrases]").val();

            //append
            $("#forphrase").append(
                "<span class='eachtag'>" +
                    task +
                    "<i class='delspan fas fa-trash-alt fa-1x tegicon'></i>"
            );
            $("#phrase").val("");
        }
        event.stopPropagation();
    });

    // INITIALIZE DATEPICKER PLUGIN
    $(".datepicker").datepicker({
        clearBtn: true,
        format: "dd/mm/yyyy"
    });

    //deleting tags

    $(".delspan").click(event => {
        itemToRemove = event.target.parentNode;
        event.target.parentNode.parentNode.removeChild(itemToRemove);
        // $(this).remove();
    });

    // form submit
    $("#kms-create-form").submit(event => {
        event.preventDefault();
    });

    $("#kms-form-submit").click(event => {
        let kmsCreateFormData = {};
        kmsCreateFormData["title"] = $("input[name=title]").val();
        kmsCreateFormData["topic"] = $("input[name=topic]").val();
        kmsCreateFormData["date"] = $("input[name=date]").val();
        kmsCreateFormData["csrfmiddlewaretoken"] = $(
            "input[name=csrfmiddlewaretoken]"
        ).val();
        let keywords = [];
        $.each($("#forkeywords").children(), function(index, el) {
            keywords.push(el.textContent.trim());
        });
        kmsCreateFormData["keywords"] = keywords;
        let mentions = [];
        $.each($("#formentions").children(), function(index, el) {
            mentions.push(el.textContent.trim());
        });
        kmsCreateFormData["mentions"] = mentions;
        let tags = [];
        $.each($("#fortags").children(), function(index, el) {
            tags.push(el.textContent.trim());
        });
        kmsCreateFormData["tags"] = tags;
        let phrases = [];
        $.each($("#forphrases").children(), function(index, el) {
            phrases.push(el.textContent.trim());
        });
        kmsCreateFormData["phrases"] = phrases;
        console.log(kmsCreateFormData);
        $.ajax({
            url: "/kms/create/",
            type: "POST",
            dataType: "json",
            data: {
                ...kmsCreateFormData
            },
            success: result => {
                console.log(result);
            }
        });
        $("#kms-create-form").trigger("reset");
        // event.preventDefault();
    });
});
