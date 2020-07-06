am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create("chart_3", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
    
    var data = [];
    var open = 100;
    var close = 250;
    
    for (var i = 1; i < 120; i++) {
      open += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 4);
      close = Math.round(open + Math.random() * 5 + i / 5 - (Math.random() < 0.5 ? 1 : -1) * Math.random() * 2);
      data.push({ date: new Date(2018, 0, i), open: open, close: close });
    }
    
    chart.data = data;
    
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.openValueY = "open";
    series.dataFields.valueY = "close";
    series.tooltipText = "open: {openValueY.value} close: {valueY.value}";
    series.sequencedInterpolation = true;
    series.fillOpacity = 0.3;
    series.defaultState.transitionDuration = 1000;
    series.tensionX = 0.8;
    
    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "open";
    series2.sequencedInterpolation = true;
    series2.defaultState.transitionDuration = 1500;
    series2.stroke = chart.colors.getIndex(6);
    series2.tensionX = 0.8;
    
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();
    
    }); // end am4core.ready()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
        am4core.ready(function () {
    
          // Themes begin
          am4core.useTheme(am4themes_animated);
          // Themes end
    
          var chart = am4core.create("chart_5", am4charts.XYChart);
          chart.hiddenState.properties.opacity = 0;
    
          chart.padding(0, 0, 0, 0);
    
          chart.zoomOutButton.disabled = true;
    
          var data = [];
          var visits = 10;
          var i = 0;
    
          for (i = 0; i <= 30; i++) {
            visits -= Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
            data.push({
              date: new Date().setSeconds(i - 30),
              value: visits
            });
          }
    
          chart.data = data;
    
          var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
          dateAxis.renderer.grid.template.location = 0;
          dateAxis.renderer.minGridDistance = 30;
          dateAxis.dateFormats.setKey("second", "ss");
          dateAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
          dateAxis.renderer.inside = true;
          dateAxis.renderer.axisFills.template.disabled = true;
          dateAxis.renderer.ticks.template.disabled = true;
          dateAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          dateAxis.renderer.labels.template.fontSize = 10;
    
          var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
          valueAxis.tooltip.disabled = true;
          valueAxis.interpolationDuration = 500;
          valueAxis.rangeChangeDuration = 500;
          valueAxis.renderer.inside = true;
          valueAxis.renderer.minLabelPosition = 0.05;
          valueAxis.renderer.maxLabelPosition = 0.95;
          valueAxis.renderer.axisFills.template.disabled = true;
          valueAxis.renderer.ticks.template.disabled = true;
          valueAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          valueAxis.renderer.labels.template.fontSize = 10;
    
          var series = chart.series.push(new am4charts.LineSeries());
          series.dataFields.dateX = "date";
          series.dataFields.valueY = "value";
          series.interpolationDuration = 500;
          series.defaultState.transitionDuration = 0;
          series.tensionX = 0.8;
    
          chart.events.on("datavalidated", function () {
            dateAxis.zoom({
              start: 1 / 15,
              end: 1.2
            }, false, true);
          });
    
          dateAxis.interpolationDuration = 500;
          dateAxis.rangeChangeDuration = 500;
    
          document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
              if (interval) {
                clearInterval(interval);
              }
            } else {
              startInterval();
            }
          }, false);
    
          // add data
          var interval;
    
          function startInterval() {
            interval = setInterval(function () {
              visits =
                visits + Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
              var lastdataItem = series.dataItems.getIndex(series.dataItems.length - 1);
              chart.addData({
                  date: new Date(lastdataItem.dateX.getTime() + 1000),
                  value: visits
                },
                1
              );
            }, 1000);
          }
    
          startInterval();
    
          // all the below is optional, makes some fancy effects
          // gradient fill of the series
          series.fillOpacity = 1;
          var gradient = new am4core.LinearGradient();
          gradient.addColor(chart.colors.getIndex(0), 0.2);
          gradient.addColor(chart.colors.getIndex(0), 0);
          series.fill = gradient;
    
          // this makes date axis labels to fade out
          dateAxis.renderer.labels.template.adapter.add("fillOpacity", function (fillOpacity, target) {
            var dataItem = target.dataItem;
            return dataItem.position;
          })
    
          // need to set this, otherwise fillOpacity is not changed and not set
          dateAxis.events.on("validated", function () {
            am4core.iter.each(dateAxis.renderer.labels.iterator(), function (label) {
              label.fillOpacity = label.fillOpacity;
            })
          })
    
          // this makes date axis labels which are at equal minutes to be rotated
          dateAxis.renderer.labels.template.adapter.add("rotation", function (rotation, target) {
            var dataItem = target.dataItem;
            if (dataItem.date && dataItem.date.getTime() == am4core.time.round(new Date(dataItem.date.getTime()),
                "minute").getTime()) {
              target.verticalCenter = "middle";
              target.horizontalCenter = "left";
              return -90;
            } else {
              target.verticalCenter = "bottom";
              target.horizontalCenter = "middle";
              return 0;
            }
          })
    
          // bullet at the front of the line
          var bullet = series.createChild(am4charts.CircleBullet);
          bullet.circle.radius = 5;
          bullet.fillOpacity = 1;
          bullet.fill = chart.colors.getIndex(0);
          bullet.isMeasured = false;
    
          series.events.on("validated", function () {
            bullet.moveTo(series.dataItems.last.point);
            bullet.validatePosition();
          });
    
        }); // end am4core.ready()
    
    
    
    
    
     
        am4core.ready(function () {
    
          // Themes begin
          am4core.useTheme(am4themes_animated);
          // Themes end
    
          var chart = am4core.create("chart_6", am4charts.XYChart);
          chart.hiddenState.properties.opacity = 0;
    
          chart.padding(0, 0, 0, 0);
    
          chart.zoomOutButton.disabled = true;
    
          var data = [];
          var visits = 10;
          var i = 0;
    
          for (i = 0; i <= 30; i++) {
            visits -= Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
            data.push({
              date: new Date().setSeconds(i - 30),
              value: visits
            });
          }
    
          chart.data = data;
    
          var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
          dateAxis.renderer.grid.template.location = 0;
          dateAxis.renderer.minGridDistance = 30;
          dateAxis.dateFormats.setKey("second", "ss");
          dateAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
          dateAxis.renderer.inside = true;
          dateAxis.renderer.axisFills.template.disabled = true;
          dateAxis.renderer.ticks.template.disabled = true;
          dateAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          dateAxis.renderer.labels.template.fontSize = 10;
    
          var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
          valueAxis.tooltip.disabled = true;
          valueAxis.interpolationDuration = 500;
          valueAxis.rangeChangeDuration = 500;
          valueAxis.renderer.inside = true;
          valueAxis.renderer.minLabelPosition = 0.05;
          valueAxis.renderer.maxLabelPosition = 0.95;
          valueAxis.renderer.axisFills.template.disabled = true;
          valueAxis.renderer.ticks.template.disabled = true;
          valueAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          valueAxis.renderer.labels.template.fontSize = 10;
    
          var series = chart.series.push(new am4charts.LineSeries());
          series.dataFields.dateX = "date";
          series.dataFields.valueY = "value";
          series.interpolationDuration = 500;
          series.defaultState.transitionDuration = 0;
          series.tensionX = 0.8;
    
          chart.events.on("datavalidated", function () {
            dateAxis.zoom({
              start: 1 / 15,
              end: 1.2
            }, false, true);
          });
    
          dateAxis.interpolationDuration = 500;
          dateAxis.rangeChangeDuration = 500;
    
          document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
              if (interval) {
                clearInterval(interval);
              }
            } else {
              startInterval();
            }
          }, false);
    
          // add data
          var interval;
    
          function startInterval() {
            interval = setInterval(function () {
              visits =
                visits + Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
              var lastdataItem = series.dataItems.getIndex(series.dataItems.length - 1);
              chart.addData({
                  date: new Date(lastdataItem.dateX.getTime() + 1000),
                  value: visits
                },
                1
              );
            }, 1000);
          }
    
          startInterval();
    
          // all the below is optional, makes some fancy effects
          // gradient fill of the series
          series.fillOpacity = 1;
          var gradient = new am4core.LinearGradient();
          gradient.addColor(chart.colors.getIndex(0), 0.2);
          gradient.addColor(chart.colors.getIndex(0), 0);
          series.fill = gradient;
    
          // this makes date axis labels to fade out
          dateAxis.renderer.labels.template.adapter.add("fillOpacity", function (fillOpacity, target) {
            var dataItem = target.dataItem;
            return dataItem.position;
          })
    
          // need to set this, otherwise fillOpacity is not changed and not set
          dateAxis.events.on("validated", function () {
            am4core.iter.each(dateAxis.renderer.labels.iterator(), function (label) {
              label.fillOpacity = label.fillOpacity;
            })
          })
    
          // this makes date axis labels which are at equal minutes to be rotated
          dateAxis.renderer.labels.template.adapter.add("rotation", function (rotation, target) {
            var dataItem = target.dataItem;
            if (dataItem.date && dataItem.date.getTime() == am4core.time.round(new Date(dataItem.date.getTime()),
                "minute").getTime()) {
              target.verticalCenter = "middle";
              target.horizontalCenter = "left";
              return -90;
            } else {
              target.verticalCenter = "bottom";
              target.horizontalCenter = "middle";
              return 0;
            }
          })
    
          // bullet at the front of the line
          var bullet = series.createChild(am4charts.CircleBullet);
          bullet.circle.radius = 5;
          bullet.fillOpacity = 1;
          bullet.fill = chart.colors.getIndex(0);
          bullet.isMeasured = false;
    
          series.events.on("validated", function () {
            bullet.moveTo(series.dataItems.last.point);
            bullet.validatePosition();
          });
    
        }); // end am4core.ready()
    
    
    
     
        am4core.ready(function () {
    
          // Themes begin
          am4core.useTheme(am4themes_animated);
          // Themes end
    
          var chart = am4core.create("chart_7", am4charts.XYChart);
          chart.hiddenState.properties.opacity = 0;
    
          chart.padding(0, 0, 0, 0);
    
          chart.zoomOutButton.disabled = true;
    
          var data = [];
          var visits = 10;
          var i = 0;
    
          for (i = 0; i <= 30; i++) {
            visits -= Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
            data.push({
              date: new Date().setSeconds(i - 30),
              value: visits
            });
          }
    
          chart.data = data;
    
          var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
          dateAxis.renderer.grid.template.location = 0;
          dateAxis.renderer.minGridDistance = 30;
          dateAxis.dateFormats.setKey("second", "ss");
          dateAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
          dateAxis.renderer.inside = true;
          dateAxis.renderer.axisFills.template.disabled = true;
          dateAxis.renderer.ticks.template.disabled = true;
          dateAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          dateAxis.renderer.labels.template.fontSize = 10;
    
          var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
          valueAxis.tooltip.disabled = true;
          valueAxis.interpolationDuration = 500;
          valueAxis.rangeChangeDuration = 500;
          valueAxis.renderer.inside = true;
          valueAxis.renderer.minLabelPosition = 0.05;
          valueAxis.renderer.maxLabelPosition = 0.95;
          valueAxis.renderer.axisFills.template.disabled = true;
          valueAxis.renderer.ticks.template.disabled = true;
          valueAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          valueAxis.renderer.labels.template.fontSize = 10;
    
          var series = chart.series.push(new am4charts.LineSeries());
          series.dataFields.dateX = "date";
          series.dataFields.valueY = "value";
          series.interpolationDuration = 500;
          series.defaultState.transitionDuration = 0;
          series.tensionX = 0.8;
    
          chart.events.on("datavalidated", function () {
            dateAxis.zoom({
              start: 1 / 15,
              end: 1.2
            }, false, true);
          });
    
          dateAxis.interpolationDuration = 500;
          dateAxis.rangeChangeDuration = 500;
    
          document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
              if (interval) {
                clearInterval(interval);
              }
            } else {
              startInterval();
            }
          }, false);
    
          // add data
          var interval;
    
          function startInterval() {
            interval = setInterval(function () {
              visits =
                visits + Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
              var lastdataItem = series.dataItems.getIndex(series.dataItems.length - 1);
              chart.addData({
                  date: new Date(lastdataItem.dateX.getTime() + 1000),
                  value: visits
                },
                1
              );
            }, 1000);
          }
    
          startInterval();
    
          // all the below is optional, makes some fancy effects
          // gradient fill of the series
          series.fillOpacity = 1;
          var gradient = new am4core.LinearGradient();
          gradient.addColor(chart.colors.getIndex(0), 0.2);
          gradient.addColor(chart.colors.getIndex(0), 0);
          series.fill = gradient;
    
          // this makes date axis labels to fade out
          dateAxis.renderer.labels.template.adapter.add("fillOpacity", function (fillOpacity, target) {
            var dataItem = target.dataItem;
            return dataItem.position;
          })
    
          // need to set this, otherwise fillOpacity is not changed and not set
          dateAxis.events.on("validated", function () {
            am4core.iter.each(dateAxis.renderer.labels.iterator(), function (label) {
              label.fillOpacity = label.fillOpacity;
            })
          })
    
          // this makes date axis labels which are at equal minutes to be rotated
          dateAxis.renderer.labels.template.adapter.add("rotation", function (rotation, target) {
            var dataItem = target.dataItem;
            if (dataItem.date && dataItem.date.getTime() == am4core.time.round(new Date(dataItem.date.getTime()),
                "minute").getTime()) {
              target.verticalCenter = "middle";
              target.horizontalCenter = "left";
              return -90;
            } else {
              target.verticalCenter = "bottom";
              target.horizontalCenter = "middle";
              return 0;
            }
          })
    
          // bullet at the front of the line
          var bullet = series.createChild(am4charts.CircleBullet);
          bullet.circle.radius = 5;
          bullet.fillOpacity = 1;
          bullet.fill = chart.colors.getIndex(0);
          bullet.isMeasured = false;
    
          series.events.on("validated", function () {
            bullet.moveTo(series.dataItems.last.point);
            bullet.validatePosition();
          });
    
        }); // end am4core.ready()
    
    
    
     
        am4core.ready(function () {
    
          // Themes begin
          am4core.useTheme(am4themes_animated);
          // Themes end
    
          var chart = am4core.create("chart_8", am4charts.XYChart);
          chart.hiddenState.properties.opacity = 0;
    
          chart.padding(0, 0, 0, 0);
    
          chart.zoomOutButton.disabled = true;
    
          var data = [];
          var visits = 10;
          var i = 0;
    
          for (i = 0; i <= 30; i++) {
            visits -= Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
            data.push({
              date: new Date().setSeconds(i - 30),
              value: visits
            });
          }
    
          chart.data = data;
    
          var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
          dateAxis.renderer.grid.template.location = 0;
          dateAxis.renderer.minGridDistance = 30;
          dateAxis.dateFormats.setKey("second", "ss");
          dateAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
          dateAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
          dateAxis.renderer.inside = true;
          dateAxis.renderer.axisFills.template.disabled = true;
          dateAxis.renderer.ticks.template.disabled = true;
          dateAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          dateAxis.renderer.labels.template.fontSize = 10;
    
          var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
          valueAxis.tooltip.disabled = true;
          valueAxis.interpolationDuration = 500;
          valueAxis.rangeChangeDuration = 500;
          valueAxis.renderer.inside = true;
          valueAxis.renderer.minLabelPosition = 0.05;
          valueAxis.renderer.maxLabelPosition = 0.95;
          valueAxis.renderer.axisFills.template.disabled = true;
          valueAxis.renderer.ticks.template.disabled = true;
          valueAxis.renderer.labels.template.fill = am4core.color("#f0ad4e");
          valueAxis.renderer.labels.template.fontSize = 10;
    
          var series = chart.series.push(new am4charts.LineSeries());
          series.dataFields.dateX = "date";
          series.dataFields.valueY = "value";
          series.interpolationDuration = 500;
          series.defaultState.transitionDuration = 0;
          series.tensionX = 0.8;
    
          chart.events.on("datavalidated", function () {
            dateAxis.zoom({
              start: 1 / 15,
              end: 1.2
            }, false, true);
          });
    
          dateAxis.interpolationDuration = 500;
          dateAxis.rangeChangeDuration = 500;
    
          document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
              if (interval) {
                clearInterval(interval);
              }
            } else {
              startInterval();
            }
          }, false);
    
          // add data
          var interval;
    
          function startInterval() {
            interval = setInterval(function () {
              visits =
                visits + Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
              var lastdataItem = series.dataItems.getIndex(series.dataItems.length - 1);
              chart.addData({
                  date: new Date(lastdataItem.dateX.getTime() + 1000),
                  value: visits
                },
                1
              );
            }, 1000);
          }
    
          startInterval();
    
          // all the below is optional, makes some fancy effects
          // gradient fill of the series
          series.fillOpacity = 1;
          var gradient = new am4core.LinearGradient();
          gradient.addColor(chart.colors.getIndex(0), 0.2);
          gradient.addColor(chart.colors.getIndex(0), 0);
          series.fill = gradient;
    
          // this makes date axis labels to fade out
          dateAxis.renderer.labels.template.adapter.add("fillOpacity", function (fillOpacity, target) {
            var dataItem = target.dataItem;
            return dataItem.position;
          })
    
          // need to set this, otherwise fillOpacity is not changed and not set
          dateAxis.events.on("validated", function () {
            am4core.iter.each(dateAxis.renderer.labels.iterator(), function (label) {
              label.fillOpacity = label.fillOpacity;
            })
          })
    
          // this makes date axis labels which are at equal minutes to be rotated
          dateAxis.renderer.labels.template.adapter.add("rotation", function (rotation, target) {
            var dataItem = target.dataItem;
            if (dataItem.date && dataItem.date.getTime() == am4core.time.round(new Date(dataItem.date.getTime()),
                "minute").getTime()) {
              target.verticalCenter = "middle";
              target.horizontalCenter = "left";
              return -90;
            } else {
              target.verticalCenter = "bottom";
              target.horizontalCenter = "middle";
              return 0;
            }
          })
    
          // bullet at the front of the line
          var bullet = series.createChild(am4charts.CircleBullet);
          bullet.circle.radius = 5;
          bullet.fillOpacity = 1;
          bullet.fill = chart.colors.getIndex(0);
          bullet.isMeasured = false;
    
          series.events.on("validated", function () {
            bullet.moveTo(series.dataItems.last.point);
            bullet.validatePosition();
          });
    
        }); // end am4core.ready()
    
    
    
    
    
    
    
    
    
    
    
    
    
     am4core.ready(function() {
      
      // Themes begin
      am4core.useTheme(am4themes_dark);
      // Themes end
      
      // Create map instance
      var chart = am4core.create("globe", am4maps.MapChart);
      var interfaceColors = new am4core.InterfaceColorSet();
      
      try {
          chart.geodata = am4geodata_worldLow;
      }
      catch (e) {
          chart.raiseCriticalError(new Error("Map geodata could not be loaded. Please download the latest <a href=\"https://www.amcharts.com/download/download-v4/\">amcharts geodata</a> and extract its contents into the same directory as your amCharts files."));
      }
      
      
      var label = chart.createChild(am4core.Label)
      label.text = "";
      label.fontSize = 12;
      label.align = "left";
      label.valign = "bottom"
      label.fill = am4core.color("#927459");
      label.background = new am4core.RoundedRectangle()
      label.background.cornerRadius(10,10,10,10);
      label.padding(10,10,10,10);
      label.marginLeft = 30;
      label.marginBottom = 30;
      label.background.strokeOpacity = 0.3;
      label.background.stroke =am4core.color("#927459");
      label.background.fill = am4core.color("#f9e3ce");
      label.background.fillOpacity = 0.6;
      
      var dataSource = chart.createChild(am4core.TextLink)
      dataSource.text = "";
      dataSource.fontSize = 12;
      dataSource.align = "left";
      dataSource.valign = "top"
      dataSource.url = "https://www.who.int/immunization/monitoring_surveillance/burden/vpd/surveillance_type/active/measles_monthlydata/en/"
      dataSource.urlTarget = "_blank";
      dataSource.fill = am4core.color("#927459");
      dataSource.padding(10,10,10,10);
      dataSource.marginLeft = 30;
      dataSource.marginTop = 30;
      
      // Set projection
      chart.projection = new am4maps.projections.Orthographic();
      chart.panBehavior = "rotateLongLat";
      chart.padding(20,20,20,20);
      
      // Add zoom control
      chart.zoomControl = new am4maps.ZoomControl();
      
      var homeButton = new am4core.Button();
      homeButton.events.on("hit", function(){
        chart.goHome();
      });
      
      homeButton.icon = new am4core.Sprite();
      homeButton.padding(7, 5, 7, 5);
      homeButton.width = 30;
      homeButton.icon.path = "M16,8 L14,8 L14,16 L10,16 L10,10 L6,10 L6,16 L2,16 L2,8 L0,8 L8,0 L16,8 Z M16,8";
      homeButton.marginBottom = 10;
      homeButton.parent = chart.zoomControl;
      homeButton.insertBefore(chart.zoomControl.plusButton);
      
      chart.backgroundSeries.mapPolygons.template.polygon.fill = am4core.color("#bfa58d");
      chart.backgroundSeries.mapPolygons.template.polygon.fillOpacity = 1;
      chart.deltaLongitude = 20;
      chart.deltaLatitude = -20;
      
      // limits vertical rotation
      chart.adapter.add("deltaLatitude", function(delatLatitude){
          return am4core.math.fitToRange(delatLatitude, -90, 90);
      })
      
      // Create map polygon series
      
      var shadowPolygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
      shadowPolygonSeries.geodata = am4geodata_continentsLow;
      
      try {
          shadowPolygonSeries.geodata = am4geodata_continentsLow;
      }
      catch (e) {
          shadowPolygonSeries.raiseCriticalError(new Error("Map geodata could not be loaded. Please download the latest <a href=\"https://www.amcharts.com/download/download-v4/\">amcharts geodata</a> and extract its contents into the same directory as your amCharts files."));
      }
      
      shadowPolygonSeries.useGeodata = true;
      shadowPolygonSeries.dx = 2;
      shadowPolygonSeries.dy = 2;
      shadowPolygonSeries.mapPolygons.template.fill = am4core.color("#000");
      shadowPolygonSeries.mapPolygons.template.fillOpacity = 0.2;
      shadowPolygonSeries.mapPolygons.template.strokeOpacity = 0;
      shadowPolygonSeries.fillOpacity = 0.1;
      shadowPolygonSeries.fill = am4core.color("#000");
      
      
      // Create map polygon series
      var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
      polygonSeries.useGeodata = true;
      
      polygonSeries.calculateVisualCenter = true;
      polygonSeries.tooltip.background.fillOpacity = 0.2;
      polygonSeries.tooltip.background.cornerRadius = 20;
      
      var template = polygonSeries.mapPolygons.template;
      template.nonScalingStroke = true;
      template.fill = am4core.color("#f9e3ce");
      template.stroke = am4core.color("#e2c9b0");
      
      polygonSeries.calculateVisualCenter = true;
      template.propertyFields.id = "id";
      template.tooltipPosition = "fixed";
      template.fillOpacity = 1;
      
      template.events.on("over", function (event) {
        if (event.target.dummyData) {
          event.target.dummyData.isHover = true;
        }
      })
      template.events.on("out", function (event) {
        if (event.target.dummyData) {
          event.target.dummyData.isHover = false;
        }
      })
      
      var hs = polygonSeries.mapPolygons.template.states.create("hover");
      hs.properties.fillOpacity = 1;
      hs.properties.fill = am4core.color("#deb7ad");
      
      
      var graticuleSeries = chart.series.push(new am4maps.GraticuleSeries());
      graticuleSeries.mapLines.template.stroke = am4core.color("#fff");
      graticuleSeries.fitExtent = false;
      graticuleSeries.mapLines.template.strokeOpacity = 0.2;
      graticuleSeries.mapLines.template.stroke = am4core.color("#fff");
      
      
      var measelsSeries = chart.series.push(new am4maps.MapPolygonSeries())
      measelsSeries.tooltip.background.fillOpacity = 0;
      measelsSeries.tooltip.background.cornerRadius = 20;
      measelsSeries.tooltip.autoTextColor = false;
      measelsSeries.tooltip.label.fill = am4core.color("#000");
      measelsSeries.tooltip.dy = -5;
      
      var measelTemplate = measelsSeries.mapPolygons.template;
      measelTemplate.fill = am4core.color("#bf7569");
      measelTemplate.strokeOpacity = 0;
      measelTemplate.fillOpacity = 0.75;
      measelTemplate.tooltipPosition = "fixed";
      
      
      
      var hs2 = measelsSeries.mapPolygons.template.states.create("hover");
      hs2.properties.fillOpacity = 1;
      hs2.properties.fill = am4core.color("#86240c");
      
      polygonSeries.events.on("inited", function () {
        polygonSeries.mapPolygons.each(function (mapPolygon) {
          var count = data[mapPolygon.id];
      
          if (count > 0) {
            var polygon = measelsSeries.mapPolygons.create();
            polygon.multiPolygon = am4maps.getCircle(mapPolygon.visualLongitude, mapPolygon.visualLatitude, Math.max(0.2, Math.log(count) * Math.LN10 / 10));
            polygon.tooltipText = mapPolygon.dataItem.dataContext.name + ": " + count;
            mapPolygon.dummyData = polygon;
            polygon.events.on("over", function () {
              mapPolygon.isHover = true;
            })
            polygon.events.on("out", function () {
              mapPolygon.isHover = false;
            })
          }
          else {
            mapPolygon.tooltipText = mapPolygon.dataItem.dataContext.name + ": no data";
            mapPolygon.fillOpacity = 0.9;
          }
      
        })
      })
      
      
      var data = {
        "AL": 504.38,
        "AM": 6.5,
        "AO": 2.98,
        "AR": 0.32,
        "AT": 10.9,
        "AU": 5.02,
        "AZ": 17.38,
        "BA": 24.45,
        "BD": 13.4,
        "BE": 12.06,
        "BF": 93.37,
        "BG": 1.68,
        "BI": 0.95,
        "BJ": 93.36,
        "BR": 49.42,
        "BT": 10.03,
        "BY": 26.16,
        "CA": 0.96,
        "CD": 69.71,
        "CF": 4.57,
        "CG": 19.7,
        "CH": 6.19,
        "CI": 14.1,
        "CL": 1.4,
        "CM": 41.26,
        "CN": 2.6,
        "CO": 4.48,
        "CY": 7.69,
        "CZ": 23.09,
        "DK": 1.58,
        "EE": 9.91,
        "EG": 0.63,
        "ES": 4.96,
        "FI": 3.27,
        "FR": 43.26,
        "GA": 3.03,
        "GB": 14.3,
        "GE": 809.09,
        "GH": 39.78,
        "GM": 2.45,
        "GN": 45.98,
        "GQ": 23.74,
        "GR": 154.42,
        "HR": 5.46,
        "HU": 1.44,
        "ID": 16.87,
        "IE": 17.56,
        "IL": 412.24,
        "IN": 47.85,
        "IQ": 12.96,
        "IR": 1.13,
        "IT": 44.29,
        "JP": 3.27,
        "KE": 16.8,
        "KG": 253.37,
        "KH": 0.44,
        "KM": 1.26,
        "KZ": 116.3,
        "LA": 1.33,
        "LK": 0.53,
        "LR": 692.27,
        "LS": 5.9,
        "LT": 14.44,
        "LU": 6.95,
        "LV": 6.09,
        "MA": 0.2,
        "MD": 83.75,
        "ME": 319.75,
        "MG": 2386.35,
        "MK": 28.83,
        "ML": 48.68,
        "MM": 40.31,
        "MN": 0.66,
        "MR": 14.65,
        "MT": 11.65,
        "MV": 9.35,
        "MX": 0.04,
        "MY": 86.41,
        "MZ": 13.49,
        "NA": 12.9,
        "NE": 80.88,
        "NG": 31.44,
        "NL": 1.47,
        "NO": 2.47,
        "NP": 10.8,
        "NZ": 9.23,
        "PE": 1.29,
        "PK": 159.14,
        "PL": 8.24,
        "PT": 16.68,
        "RO": 63.05,
        "RS": 473.46,
        "RU": 14.24,
        "RW": 5.45,
        "SE": 2.64,
        "SG": 8.18,
        "SI": 3.37,
        "SK": 112.78,
        "SN": 3.37,
        "SO": 8.03,
        "SS": 19.3,
        "TD": 75.63,
        "TG": 34.84,
        "TH": 81.02,
        "TL": 9.46,
        "TN": 7.8,
        "TR": 7.08,
        "UA": 1439.02,
        "UG": 62.55,
        "US": 1.32,
        "UZ": 0.99,
        "VE": 179.55,
        "ZA": 3.09,
        "ZM": 9.82,
        "ZW": 0.06
      }
      
      }); // end am4core.ready()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     am4core.ready(function() {
      
      // Themes begin
      am4core.useTheme(am4themes_dark);
      am4core.useTheme(am4themes_animated);
      // Themes end
      
      // Create map instance
      var chart = am4core.create("globe_2", am4maps.MapChart);
      
      // Set map definition
      chart.geodata = am4geodata_worldLow;
      
      // Set projection
      chart.projection = new am4maps.projections.Miller();
      
      // Create map polygon series
      var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
      
      // Exclude Antartica
      polygonSeries.exclude = ["AQ"];
      
      // Make map load polygon (like country names) data from GeoJSON
      polygonSeries.useGeodata = true;
      
      // Configure series
      var polygonTemplate = polygonSeries.mapPolygons.template;
      polygonTemplate.tooltipText = "{name}";
      polygonTemplate.fill = chart.colors.getIndex(0).lighten(0.5);
      
      // Create hover state and set alternative fill color
      var hs = polygonTemplate.states.create("hover");
      hs.properties.fill = chart.colors.getIndex(0);
      
      // Add image series
      var imageSeries = chart.series.push(new am4maps.MapImageSeries());
      imageSeries.mapImages.template.propertyFields.longitude = "longitude";
      imageSeries.mapImages.template.propertyFields.latitude = "latitude";
      imageSeries.data = [ {
        "title": "Brussels",
        "latitude": 50.8371,
        "longitude": 4.3676
      }, {
        "title": "Copenhagen",
        "latitude": 55.6763,
        "longitude": 12.5681
      }, {
        "title": "Paris",
        "latitude": 48.8567,
        "longitude": 2.3510
      }, {
        "title": "Reykjavik",
        "latitude": 64.1353,
        "longitude": -21.8952
      }, {
        "title": "Moscow",
        "latitude": 55.7558,
        "longitude": 37.6176
      }, {
        "title": "Madrid",
        "latitude": 40.4167,
        "longitude": -3.7033
      }, {
        "title": "London",
        "latitude": 51.5002,
        "longitude": -0.1262,
        "url": "http://www.google.co.uk"
      }, {
        "title": "Peking",
        "latitude": 39.9056,
        "longitude": 116.3958
      }, {
        "title": "New Delhi",
        "latitude": 28.6353,
        "longitude": 77.2250
      }, {
        "title": "Tokyo",
        "latitude": 35.6785,
        "longitude": 139.6823,
        "url": "http://www.google.co.jp"
      }, {
        "title": "Ankara",
        "latitude": 39.9439,
        "longitude": 32.8560
      }, {
        "title": "Buenos Aires",
        "latitude": -34.6118,
        "longitude": -58.4173
      }, {
        "title": "Brasilia",
        "latitude": -15.7801,
        "longitude": -47.9292
      }, {
        "title": "Ottawa",
        "latitude": 45.4235,
        "longitude": -75.6979
      }, {
        "title": "Washington",
        "latitude": 38.8921,
        "longitude": -77.0241
      }, {
        "title": "Kinshasa",
        "latitude": -4.3369,
        "longitude": 15.3271
      }, {
        "title": "Cairo",
        "latitude": 30.0571,
        "longitude": 31.2272
      }, {
        "title": "Pretoria",
        "latitude": -25.7463,
        "longitude": 28.1876
      } ];
      
      // add events to recalculate map position when the map is moved or zoomed
      chart.events.on( "ready", updateCustomMarkers );
      chart.events.on( "mappositionchanged", updateCustomMarkers );
      
      // this function will take current images on the map and create HTML elements for them
      function updateCustomMarkers( event ) {
        
        // go through all of the images
        imageSeries.mapImages.each(function(image) {
          // check if it has corresponding HTML element
          if (!image.dummyData || !image.dummyData.externalElement) {
            // create onex
            image.dummyData = {
              externalElement: createCustomMarker(image)
            };
          }
      
          // reposition the element accoridng to coordinates
          var xy = chart.geoPointToSVG( { longitude: image.longitude, latitude: image.latitude } );
          image.dummyData.externalElement.style.top = xy.y + 'px';
          image.dummyData.externalElement.style.left = xy.x + 'px';
        });
      
      }
      
      // this function creates and returns a new marker element
      function createCustomMarker( image ) {
        
        var chart = image.dataItem.component.chart;
      
        // create holder
        var holder = document.createElement( 'div' );
        holder.className = 'map-marker';
        holder.title = image.dataItem.dataContext.title;
        holder.style.position = 'absolute';
      
        // maybe add a link to it?
        if ( undefined != image.url ) {
          holder.onclick = function() {
            window.location.href = image.url;
          };
          holder.className += ' map-clickable';
        }
      
        // create dot
        var dot = document.createElement( 'div' );
        dot.className = 'dot';
        holder.appendChild( dot );
      
        // create pulse
        var pulse = document.createElement( 'div' );
        pulse.className = 'pulse';
        holder.appendChild( pulse );
      
        // append the marker to the map container
        chart.svgContainer.htmlElement.appendChild( holder );
      
        return holder;
      }
      
      }); // end am4core.ready()