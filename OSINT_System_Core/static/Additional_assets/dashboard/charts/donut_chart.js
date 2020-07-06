$(document).ready(function() {
  const chatSocket = new WebSocket(
    // 'ws://'+ window.location.host+ '/ws/chat/'+ roomName+ '/'
    "ws://" + window.location.host + "/ws/chat/"
  );

  setInterval(function() {
    chatSocket.send(
      JSON.stringify({
        message: "Dear Django channels update Donutchart data "
      })
    );
  }, 20000);


  chatSocket.onopen = () =>
  chatSocket.send(
    "**************Donut chart   == First load  **************"
  );




  am4core.ready(function() {
    am4core.useTheme(am4themes_animated);
    var chart = am4core.create("donut", am4charts.PieChart);
    chart.paddingBottom = 0;
    chart.paddingTop = 0;
    chart.paddingRight = 0;
    chart.paddingLeft = 0;

    // chart.data = [ {
    // "platform": "TWITTER",
    // "values": "{{list1.0}}",
    // // "color": am4core.color("#fde7f9")
    // }, {
    // "platform": "LINKEDIN",
    // "values": "{{list1.1}}",
    // // "color": am4core.color("#fde7f4")
    // }, {
    // "platform": "FACEBOOK",
    // "values":  "{{list1.2}}",
    // // "color": am4core.color("#aee3e0")
    // }, {
    // "platform": "INSTAGRAM",
    // "values":  "{{list1.3}}",
    // // "color": am4core.color("#72cec9")
    // },
    // ];

    chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      console.log("recived from Django channels");
      console.log(data);
      console.log(data.message[0]);

      chart.data = [
        {
          platform: "TWITTER",
          values: data.message[0]
          // "color": am4core.color("#fde7f9")
        },
        {
          platform: "LINKEDIN",
          values: data.message[1]
          // "color": am4core.color("#fde7f4")
        },
        {
          platform: "FACEBOOK",
          values: data.message[2]
          // "color": am4core.color("#aee3e0")
        },
        {
          platform: "INSTAGRAM",
          values: data.message[3]
          // "color": am4core.color("#72cec9")
        }
      ];

      //show notification
  toastr["success"]("Scoal Media Donu Chart Updated");

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

    // Set inner radius
    chart.innerRadius = am4core.percent(60);

    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "values";
    pieSeries.dataFields.category = "platform";
    pieSeries.slices.template.stroke = am4core.color("#000");
    pieSeries.slices.template.strokeWidth = 2;
    pieSeries.slices.template.strokeOpacity = 1;
    pieSeries.slices.template.propertyFields.fill = "color";
    pieSeries.labels.template.fontSize = 10;
    pieSeries.labels.template.fontColor = "black";

    pieSeries.ticks.template.disabled = true;
    pieSeries.alignLabels = false;
    pieSeries.labels.template.text = "{value.percent.formatNumber('#.0')}%";
    pieSeries.labels.template.radius = am4core.percent(-40);
    pieSeries.labels.template.fill = am4core.color("white");

    // pieSeries.labels.template.disabled = true;
    // pieSeries.ticks.template.disabled = true;
    // This creates initial animation
    pieSeries.hiddenState.properties.opacity = 1;
    pieSeries.hiddenState.properties.endAngle = -90;
    pieSeries.hiddenState.properties.startAngle = -90;
    let rgm = new am4core.RadialGradientModifier();
    rgm.brightnesses.push(-0.8, -0.8, -0.5, 0, -0.5);
    pieSeries.slices.template.fillModifier = rgm;
    pieSeries.slices.template.strokeModifier = rgm;
    pieSeries.slices.template.strokeOpacity = 0.4;
    pieSeries.slices.template.strokeWidth = 0;
  }); // end am4core.ready()
});


















