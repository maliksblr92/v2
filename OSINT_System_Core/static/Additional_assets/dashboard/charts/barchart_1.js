


$(document).ready(function() {
  const chatSocket = new WebSocket(
    // 'ws://'+ window.location.host+ '/ws/chat/'+ roomName+ '/'
    "ws://" + window.location.host + "/ws/chat/"
  );

  setInterval(function() {
    chatSocket.send(
      JSON.stringify({
        message: "Dear Django channels update BarChart  data "
      })
    );
  }, 10000);


  chatSocket.onopen = () =>
  chatSocket.send(
    "**************Bar chart   == First load  **************"
  );




  am4core.ready(function() {
    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end
    var chart = am4core.create("barchart", am4charts.XYChart);
    chart.paddingBottom = 0;
    chart.paddingTop = 0;
    chart.paddingRight = 0;
    chart.paddingLeft = 0;


    chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      console.log("recived from Django channels");
      console.log(data);
      console.log(data.message[0]);

      chart.data = [
        {
          category: "TWITTER",
          value: data.message[0]
          // "color": am4core.color("#fde7f9")
        },
        {
          category: "LINKEDIN",
          value: data.message[1]
          // "color": am4core.color("#fde7f4")
        },
        {
          category: "FACEBOOK",
          value: data.message[2]
          // "color": am4core.color("#aee3e0")
        },
        {
          category: "INSTAGRAM",
          value: data.message[3]
          // "color": am4core.color("#72cec9")
        }
      ];
      //show notification
  toastr["success"]("Scoal Media Bar Chart Updated");

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



    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.dataFields.category = "category";
    categoryAxis.renderer.minGridDistance = 15;
    categoryAxis.renderer.grid.template.location = 0.5;
    categoryAxis.renderer.grid.template.strokeDasharray = "1,3";
    categoryAxis.renderer.labels.template.rotation = -90;
    categoryAxis.renderer.labels.template.fontSize = 10;
    categoryAxis.renderer.labels.template.horizontalCenter = "left";
    categoryAxis.renderer.labels.template.location = 0.5;
    categoryAxis.renderer.labels.template.adapter.add("dx", function(dx, target) {
    return -target.maxRight / 2;
    })
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.ticks.template.disabled = true;
    valueAxis.renderer.axisFills.template.disabled = true;
    var series = chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.categoryX = "category";
    series.dataFields.valueY = "value";
    series.tooltipText = "{valueY.value}";
    series.sequencedInterpolation = true;
    series.fillOpacity = 0;
    series.strokeOpacity = 1;
    series.strokeDashArray = "1,3";
    series.columns.template.width = 0.01;
    series.tooltip.pointerOrientation = "horizontal";
    var bullet = series.bullets.create(am4charts.CircleBullet);
    chart.cursor = new am4charts.XYCursor();
    chart.scrollbarX = new am4core.Scrollbar();
    chart.scrollbarY = new am4core.Scrollbar();
    }); // end am4core.ready()

});











