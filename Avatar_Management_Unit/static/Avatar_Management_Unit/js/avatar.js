// document.addEventListener("DOMContentLoaded", function () {
//     //personal-info ajax form submit
//     $("#personal-info-form").submit((event) => {
//         fdata = {};
//         $.each($("#personal-info-form input"), (index, el) => {
//             // console.log(el);
//             // console.log(el.val());
//             fdata[$(el).attr("name")] = $(el).val();
//         });
//         fdata["pinfo-gender"] = $(
//             "#personal-info-form select[name=pinfo-gender] option:selected"
//         ).val();
//         console.log(fdata);
//         $.ajax({
//             method: "POST",
//             url: "/amu/avatar/",
//             data: fdata,
//             success: (result) => {
//                 console.log(result);
//             },
//         });
//         $("#personal-info-form").trigger("reset");
//         event.preventDefault();
//     });

//     //work details form submit
//     $("#work-details-form").submit((event) => {
//         fdata = {};
//         $.each($("#work-details-form input"), (index, el) => {
//             fdata[$(el).attr("name")] = $(el).val();
//         });
//         fdata["wd-avatar"] = $(
//             "#work-details-form select[name=wd-avatar] option:selected"
//         ).val();
//         fdata["wd-current-job"] = $(
//             "#work-details-form input[name=wd-current-job]"
//         ).is(":checked");
//         console.log(fdata);
//         $.ajax({
//             method: "POST",
//             url: "/amu/addwork/",
//             data: fdata,
//             success: (result) => {
//                 console.log(result);
//             },
//         });
//         $("#work-details-form").trigger("reset");
//         event.preventDefault();
//     });

//     //interest tab handling
//     //insert values from input box to containers
//     $("#i-hobbies, #i-movies, #i-songs").keypress((event) => {
//         // 13 is ASCII code for enter
//         if (event.which === 13) {
//             switch ($(event.target).attr("id")) {
//                 case "i-hobbies":
//                     $("#i-hobbies-container").append(
//                         "<span class='eachtag'>" +
//                             $(event.target).val() +
//                             "<i style='color:white; opacity:0.8;' class='i-cross-icon fas fa-times fa-1x tegicon'></i></span>"
//                     );
//                     break;
//                 case "i-movies":
//                     $("#i-movies-container").append(
//                         "<span class='eachtag'>" +
//                             $(event.target).val() +
//                             "<i style='color:white; opacity:0.8;' class='i-cross-icon fas fa-times fa-1x tegicon'></i></span>"
//                     );
//                     break;
//                 case "i-songs":
//                     $("#i-songs-container").append(
//                         "<span class='eachtag'>" +
//                             $(event.target).val() +
//                             "<i style='color:white; opacity:0.8;' class='i-cross-icon fas fa-times fa-1x tegicon'></i></span>"
//                     );
//                     break;
//                 default:
//                     console.log("error no switch found");
//                     break;
//             }
//             $(event.target).val("");
//         }
//     });

//     //delete a hobby, movie or a song
//     $(".i-cross-icon").click((event) => {
//         console.log(event.target);
//         itemToRemove = event.target.parentNode;
//         event.target.parentNode.parentNode.removeChild(itemToRemove);
//     });

//     //handle submit button for interest
//     $("#i-submit-btn").click((event) => {
//         let hobbies = [],
//             movies = [],
//             songs = [];

//         //get the values out of containers to arrays
//         $.each($("#i-hobbies-container").children(), (index, el) => {
//             hobbies.push(el.textContent.trim());
//         });
//         $.each($("#i-movies-container").children(), (index, el) => {
//             movies.push(el.textContent.trim());
//         });
//         $.each($("#i-songs-container").children(), (index, el) => {
//             songs.push(el.textContent.trim());
//         });

//         //join arrays together to a dictionary
//         interests = {
//             hobbies: hobbies,
//             movies: movies,
//             songs: songs,
//             csrfmiddlewaretoken: $(
//                 "#interests-form > input[name=csrfmiddlewaretoken]"
//             ).val(),
//         };
//         interests["i-avatar"] = $(
//             "#interests-form select[name=i-avatar] option:selected"
//         ).val();

//         // debug log
//         console.log(interests);

//         // submit the data to a django view
//         $.ajax({
//             url: "/amu/addinterest/",
//             method: "POST",
//             data: interests,
//             success: (result) => {
//                 console.log(result);
//             },
//         });

//         //simulate the clear button click
//         $("#i-clear-btn").trigger("click");
//     });

//     //handle clear button for interest
//     $("#i-clear-btn").click(() => {
//         $("#i-hobbies, #i-movies, #i-songs").val("");
//         $(
//             "#i-hobbies-container, #i-movies-container, #i-songs-container"
//         ).empty();
//         event.preventDefault();
//     });

//     //education form submit
//     $("#education-form").submit((event) => {
//         console.log("education form submit");
//         fdata = {};
//         $.each($("#education-form input"), (index, el) => {
//             fdata[$(el).attr("name")] = $(el).val();
//         });
//         fdata["le-ef-avatar"] = $(
//             "select[name=le-avatar] option:selected"
//         ).val();
//         console.log(fdata);
//         $("education-form").trigger("reset");
//         event.preventDefault();
//         $.ajax({
//             url: "/amu/addeducation/",
//             method: "POST",
//             data: fdata,
//             success: (result) => {
//                 console.log(result);
//             },
//         });
//     });

//     //marriage form submit
//     $("#marriage-form").submit((event) => {
//         console.log("marriage form submitted");
//         fdata = {};
//         $.each($("#marriage-form input"), (index, el) => {
//             fdata[$(el).attr("name")] = $(el).val();
//         });
//         fdata["le-m-avatar"] = $(
//             "select[name=le-avatar] option:selected"
//         ).val();
//         console.log(fdata);
//         $("#marriage-form").trigger("reset");
//         event.preventDefault();
//         $.ajax({
//             url: "/amu/addmarriage/",
//             method: "POST",
//             data: fdata,
//             success: (result) => {
//                 console.log(result);
//             },
//         });
//     });

//     //biography form submit
//     $("#biography-form").submit((event) => {
//         console.log("biography form submitted");
//         fdata = {};
//         $.each($("#biography-form input"), (index, el) => {
//             fdata[$(el).attr("name")] = $(el).val();
//         });
//         fdata["b-biography"] = $(
//             "#biography-form textarea[name=b-biography]"
//         ).val();
//         fdata["b-avatar"] = $(
//             "#biography-form select[name=b-avatar] option:selected"
//         ).val();
//         console.log(fdata);
//         $("#biography-form").trigger("reset");
//         event.preventDefault();
//         $.ajax({
//             url: "/amu/addbiography/",
//             method: "POST",
//             data: fdata,
//             success: (result) => {
//                 console.log(result);
//             },
//         });
//     });

//     //social media account form submit
//     $("#socialaccount-form").submit((event) => {
//         console.log("social account form submitted");
//         fdata = {};
//         $.each(
//             $(
//                 `#socialaccount-form input[type=text],
//                 #socialaccount-form input[type=email],
//                 #socialaccount-form input[name=csrfmiddlewaretoken]`
//             ),
//             (index, el) => {
//                 fdata[$(el).attr("name")] = $(el).val();
//             }
//         );
//         fdata["sma-avatar"] = $(
//             "#socialaccount-form select[name=sma-avatar] option:selected"
//         ).val();
//         fdata["sma-gender"] = $(
//             "#socialaccount-form select[name=sma-gender] option:selected"
//         ).val();
//         fdata["sma-platform"] = $(
//             "#socialaccount-form input[name=sma-platform]:checked"
//         ).val();
//         console.log(fdata);
//         event.preventDefault();
//         $.ajax({
//             url: "/amu/addsocialaccount/",
//             method: "POST",
//             data: fdata,
//         })
//             .then((result) => {
//                 console.log(result);
//                 // $("#socialaccount-form").trigger("reset");
//             })
//             .catch((error) => {
//                 console.log(error);
//             });
//     });

//     //posts form submit
//     $("#socialpost-form").submit((event) => {
//         console.log("social post form submitted");
//         fdata = {};
//         fdata["csrfmiddlewaretoken"] = $(
//             "#socialpost-form input[name=csrfmiddlewaretoken]"
//         ).val();
//         fdata["smp-platform"] = $(
//             "#socialpost-form input[name=smp-platform]:checked"
//         ).val();
//         fdata["smp-avatar"] = $(
//             "#socialpost-form select[name=smp-avatar] option:selected"
//         ).val();
//         fdata["smp-text"] = $("#socialpost-form textarea[name=smp-text]").val();
//         fdata["smp-date"] = $("#socialpost-form input[name=smp-date]").val();
//         console.log(fdata);
//         event.preventDefault();
//         $.ajax({
//             url: "/amu/addsocialpost/",
//             method: "POST",
//             data: fdata,
//         })
//             .then((result) => {
//                 console.log(result);
//                 $("#socialpost-form").trigger("reset");
//             })
//             .catch((error) => {
//                 console.log(error);
//             });
//     });
// });
