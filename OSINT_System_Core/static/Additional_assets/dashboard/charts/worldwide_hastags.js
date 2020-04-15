$(document).ready(function () {
  const chatSocket = new WebSocket(
    // 'ws://'+ window.location.host+ '/ws/chat/'+ roomName+ '/'
    "ws://" + window.location.host + "/ws/dashboard_hastags_worldwide/"
  );

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log("recived worldwide hastags from Django channels");
    console.log(data);
    console.log(data.message[0]);
    len = data.message.length;
    console.log(len);
    // $('#recent_trends_worldwide').empty() ;
    for (var x = 0; x < len; x++) {
      if (data.message[x].count == "count unavalible") {
        data.message[x].count = "N/A";
      }
      var html =
        ' <div class="col-md-12 mt-1"><div class="row"><div class="col-md-2  m-0 p-0 custom_center"><span class="bg-dark text-white custom_center border border-warning font-weight-bold "style="border-radius:50%;height:40px;width:100%;font-size:12px;">' +
        data.message[x].count +
        '</span></div><div class="col-md-10 border border-warning m-0  social_posts_post custom_center"style="overflow: hidden;"><a class="text-white font-weight-bold nav-link" href=' +
        data.message[x].href +
        ">" +
        data.message[x].name +
        "</a></div></div></div>";
      // var html='<div class="col-md-6"><div class="row"><div class="col-md-3  m-0 p-0 custom_center"><img src="/static/assets/dashboard_app_assets/images/profile woman (3).svg"  class="m-0 p-0 recent_trends_img" style="" alt="" /></div><div class="col-md-9 border border-warning text-white m-0 recent_trends_post p-0 m-0"><div class="w-100 h-50 d-flex flex-row  justify-content-start align-items-center  "style ="font-size:10px;overflow:hidden;"><a href="'+data.message[x].href+'">'+data.message[x].name+'</a></div><div class="text-white w-80 h-50 d-flex flex-row justify-content-start align-items-center " style ="font-size:10px;"> Count :'+data.message[x].count+'</div></div></div></div>'
      $("#recent_trends_worldwide").append(html);
    }
    var today = new Date();
    var date =
      today.getFullYear() +
      "-" +
      (today.getMonth() + 1) +
      "-" +
      today.getDate();
    var time =
      today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = date + " " + time;
    $("#trends_update_time")
      .empty()
      .append("Last updated : " + dateTime);

    //show notification
    toastr["success"]("World wide hashtags refreshed");

    toastr.options = {
      closeButton: true,
      debug: false,
      newestOnTop: true,
      progressBar: true,
      positionClass: "toast-top-right",
      preventDuplicates: false,
      showDuration: "300",
      hideDuration: "1000",
      timeOut: "5000",
      extendedTimeOut: "1000",
      showEasing: "swing",
      hideEasing: "linear",
      showMethod: "fadeIn",
      hideMethod: "fadeOut",
    };
  };

  chatSocket.onopen = () =>
    chatSocket.send(
      "**************world wide hastags  == First load  **************"
    );

  $("#refesh_world_wide_trends_btn").on("click", function () {
    console.log("refesh_world_wide_trends_btn == clicked");

    chatSocket.send(
      JSON.stringify({
        message: "**************world wide hastags  == Refresh  **************",
      })
    );
    toastr["info"]("Requestfor refreshing world wide hastags");

    toastr.options = {
      closeButton: false,
      debug: false,
      newestOnTop: true,
      progressBar: true,
      positionClass: "toast-top-right",
      preventDuplicates: false,
      onclick: null,
      showDuration: "300",
      hideDuration: "1000",
      timeOut: "5000",
      extendedTimeOut: "1000",
      showEasing: "swing",
      hideEasing: "linear",
      showMethod: "fadeIn",
      hideMethod: "fadeOut",
    };
  });
});


