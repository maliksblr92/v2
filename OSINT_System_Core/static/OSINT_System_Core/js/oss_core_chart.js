// am4core.ready(function() {
//     // Themes begin
//     am4core.useTheme(am4themes_dark);
//     am4core.useTheme(am4themes_animated);
//     // Themes end

//     // Create chart instance
//     var chart = am4core.create("chart_3", am4charts.RadarChart);

//     // Add data
//     chart.data = [
//         {
//             category: "Research",
//             value: 80,
//             full: 100
//         },
//         {
//             category: "Marketing",
//             value: 35,
//             full: 100
//         },
//         {
//             category: "Distribution",
//             value: 92,
//             full: 100
//         },
//         {
//             category: "Human Resources",
//             value: 68,
//             full: 100
//         }
//     ];

//     // Make chart not full circle
//     chart.startAngle = -90;
//     chart.endAngle = 180;
//     chart.innerRadius = am4core.percent(50);

//     // Set number format
//     chart.numberFormatter.numberFormat = "#.#'%'";

//     // Create axes
//     var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
//     categoryAxis.dataFields.category = "category";
//     categoryAxis.renderer.grid.template.location = 0;
//     categoryAxis.renderer.grid.template.strokeOpacity = 0;
//     categoryAxis.renderer.labels.template.horizontalCenter = "right";
//     categoryAxis.renderer.labels.template.fontWeight = 500;
//     categoryAxis.renderer.labels.template.fontSize = 12;

//     categoryAxis.renderer.labels.template.adapter.add("fill", function(
//         fill,
//         target
//     ) {
//         return target.dataItem.index >= 0
//             ? chart.colors.getIndex(target.dataItem.index)
//             : fill;
//     });
//     categoryAxis.renderer.minGridDistance = 10;

//     var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
//     valueAxis.renderer.grid.template.strokeOpacity = 0;
//     valueAxis.min = 0;
//     valueAxis.max = 100;
//     valueAxis.strictMinMax = true;

//     // Create series
//     var series1 = chart.series.push(new am4charts.RadarColumnSeries());
//     series1.dataFields.valueX = "full";
//     series1.dataFields.categoryY = "category";
//     series1.clustered = false;
//     series1.columns.template.fill = new am4core.InterfaceColorSet().getFor(
//         "alternativeBackground"
//     );
//     series1.columns.template.fillOpacity = 0.08;
//     series1.columns.template.cornerRadiusTopLeft = 20;
//     series1.columns.template.strokeWidth = 0;
//     series1.columns.template.radarColumn.cornerRadius = 20;

//     var series2 = chart.series.push(new am4charts.RadarColumnSeries());
//     series2.dataFields.valueX = "value";
//     series2.dataFields.categoryY = "category";
//     series2.clustered = false;
//     series2.columns.template.strokeWidth = 0;
//     series2.columns.template.tooltipText = "{category}: [bold]{value}[/]";
//     series2.columns.template.radarColumn.cornerRadius = 20;

//     series2.columns.template.adapter.add("fill", function(fill, target) {
//         return chart.colors.getIndex(target.dataItem.index);
//     });

//     // Add cursor
//     chart.cursor = new am4charts.RadarCursor();
// }); // end am4core.ready()

// am4core.ready(function() {
//     // Themes begin
//     am4core.useTheme(am4themes_animated);
//     // Themes end

//     var chart = am4core.create("chart_4", am4charts.XYChart);
//     chart.hiddenState.properties.opacity = 0;

//     chart.padding(0, 0, 0, 0);

//     chart.zoomOutButton.disabled = true;

//     var data = [];
//     var visits = 10;
//     var i = 0;

//     for (i = 0; i <= 30; i++) {
//         visits -= Math.round(
//             (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
//         );
//         data.push({
//             date: new Date().setSeconds(i - 30),
//             value: visits
//         });
//     }

//     chart.data = data;

//     var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
//     dateAxis.renderer.grid.template.location = 0;
//     dateAxis.renderer.minGridDistance = 30;
//     dateAxis.dateFormats.setKey("second", "ss");
//     dateAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
//     dateAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
//     dateAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
//     dateAxis.renderer.inside = true;
//     dateAxis.renderer.axisFills.template.disabled = true;
//     dateAxis.renderer.ticks.template.disabled = true;

//     var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
//     valueAxis.tooltip.disabled = true;
//     valueAxis.interpolationDuration = 500;
//     valueAxis.rangeChangeDuration = 500;
//     valueAxis.renderer.inside = true;
//     valueAxis.renderer.minLabelPosition = 0.05;
//     valueAxis.renderer.maxLabelPosition = 0.95;
//     valueAxis.renderer.axisFills.template.disabled = true;
//     valueAxis.renderer.ticks.template.disabled = true;

//     var series = chart.series.push(new am4charts.LineSeries());
//     series.dataFields.dateX = "date";
//     series.dataFields.valueY = "value";
//     series.interpolationDuration = 500;
//     series.defaultState.transitionDuration = 0;
//     series.tensionX = 0.8;

//     chart.events.on("datavalidated", function() {
//         dateAxis.zoom(
//             {
//                 start: 1 / 15,
//                 end: 1.2
//             },
//             false,
//             true
//         );
//     });

//     dateAxis.interpolationDuration = 500;
//     dateAxis.rangeChangeDuration = 500;

//     document.addEventListener(
//         "visibilitychange",
//         function() {
//             if (document.hidden) {
//                 if (interval) {
//                     clearInterval(interval);
//                 }
//             } else {
//                 startInterval();
//             }
//         },
//         false
//     );

//     // add data
//     var interval;

//     function startInterval() {
//         interval = setInterval(function() {
//             visits =
//                 visits +
//                 Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
//             var lastdataItem = series.dataItems.getIndex(
//                 series.dataItems.length - 1
//             );
//             chart.addData(
//                 {
//                     date: new Date(lastdataItem.dateX.getTime() + 1000),
//                     value: visits
//                 },
//                 1
//             );
//         }, 1000);
//     }

//     startInterval();

//     // all the below is optional, makes some fancy effects
//     // gradient fill of the series
//     series.fillOpacity = 1;
//     var gradient = new am4core.LinearGradient();
//     gradient.addColor(chart.colors.getIndex(0), 0.2);
//     gradient.addColor(chart.colors.getIndex(0), 0);
//     series.fill = gradient;

//     // this makes date axis labels to fade out
//     dateAxis.renderer.labels.template.adapter.add("fillOpacity", function(
//         fillOpacity,
//         target
//     ) {
//         var dataItem = target.dataItem;
//         return dataItem.position;
//     });

//     // need to set this, otherwise fillOpacity is not changed and not set
//     dateAxis.events.on("validated", function() {
//         am4core.iter.each(dateAxis.renderer.labels.iterator(), function(label) {
//             label.fillOpacity = label.fillOpacity;
//         });
//     });

//     // this makes date axis labels which are at equal minutes to be rotated
//     dateAxis.renderer.labels.template.adapter.add("rotation", function(
//         rotation,
//         target
//     ) {
//         var dataItem = target.dataItem;
//         if (
//             dataItem.date &&
//             dataItem.date.getTime() ==
//                 am4core.time
//                     .round(new Date(dataItem.date.getTime()), "minute")
//                     .getTime()
//         ) {
//             target.verticalCenter = "middle";
//             target.horizontalCenter = "left";
//             return -90;
//         } else {
//             target.verticalCenter = "bottom";
//             target.horizontalCenter = "middle";
//             return 0;
//         }
//     });

//     // bullet at the front of the line
//     var bullet = series.createChild(am4charts.CircleBullet);
//     bullet.circle.radius = 5;
//     bullet.fillOpacity = 1;
//     bullet.fill = chart.colors.getIndex(0);
//     bullet.isMeasured = false;

//     series.events.on("validated", function() {
//         bullet.moveTo(series.dataItems.last.point);
//         bullet.validatePosition();
//     });
// }); // end am4core.ready()

//chart_5
am4core.ready(function() {
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
        visits -= Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
        );
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

    chart.events.on("datavalidated", function() {
        dateAxis.zoom(
            {
                start: 1 / 15,
                end: 1.2
            },
            false,
            true
        );
    });

    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;

    document.addEventListener(
        "visibilitychange",
        function() {
            if (document.hidden) {
                if (interval) {
                    clearInterval(interval);
                }
            } else {
                startInterval();
            }
        },
        false
    );

    // add data
    var interval;

    function startInterval() {
        interval = setInterval(function() {
            visits =
                visits +
                Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
            var lastdataItem = series.dataItems.getIndex(
                series.dataItems.length - 1
            );
            chart.addData(
                {
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
    dateAxis.renderer.labels.template.adapter.add("fillOpacity", function(
        fillOpacity,
        target
    ) {
        var dataItem = target.dataItem;
        return dataItem.position;
    });

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on("validated", function() {
        am4core.iter.each(dateAxis.renderer.labels.iterator(), function(label) {
            label.fillOpacity = label.fillOpacity;
        });
    });

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add("rotation", function(
        rotation,
        target
    ) {
        var dataItem = target.dataItem;
        if (
            dataItem.date &&
            dataItem.date.getTime() ==
                am4core.time
                    .round(new Date(dataItem.date.getTime()), "minute")
                    .getTime()
        ) {
            target.verticalCenter = "middle";
            target.horizontalCenter = "left";
            return -90;
        } else {
            target.verticalCenter = "bottom";
            target.horizontalCenter = "middle";
            return 0;
        }
    });

    // bullet at the front of the line
    var bullet = series.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 5;
    bullet.fillOpacity = 1;
    bullet.fill = chart.colors.getIndex(0);
    bullet.isMeasured = false;

    series.events.on("validated", function() {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });
}); // end am4core.ready()

//chart_6
am4core.ready(function() {
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
        visits -= Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
        );
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

    chart.events.on("datavalidated", function() {
        dateAxis.zoom(
            {
                start: 1 / 15,
                end: 1.2
            },
            false,
            true
        );
    });

    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;

    document.addEventListener(
        "visibilitychange",
        function() {
            if (document.hidden) {
                if (interval) {
                    clearInterval(interval);
                }
            } else {
                startInterval();
            }
        },
        false
    );

    // add data
    var interval;

    function startInterval() {
        interval = setInterval(function() {
            visits =
                visits +
                Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
            var lastdataItem = series.dataItems.getIndex(
                series.dataItems.length - 1
            );
            chart.addData(
                {
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
    dateAxis.renderer.labels.template.adapter.add("fillOpacity", function(
        fillOpacity,
        target
    ) {
        var dataItem = target.dataItem;
        return dataItem.position;
    });

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on("validated", function() {
        am4core.iter.each(dateAxis.renderer.labels.iterator(), function(label) {
            label.fillOpacity = label.fillOpacity;
        });
    });

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add("rotation", function(
        rotation,
        target
    ) {
        var dataItem = target.dataItem;
        if (
            dataItem.date &&
            dataItem.date.getTime() ==
                am4core.time
                    .round(new Date(dataItem.date.getTime()), "minute")
                    .getTime()
        ) {
            target.verticalCenter = "middle";
            target.horizontalCenter = "left";
            return -90;
        } else {
            target.verticalCenter = "bottom";
            target.horizontalCenter = "middle";
            return 0;
        }
    });

    // bullet at the front of the line
    var bullet = series.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 5;
    bullet.fillOpacity = 1;
    bullet.fill = chart.colors.getIndex(0);
    bullet.isMeasured = false;

    series.events.on("validated", function() {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });
}); // end am4core.ready()

//chart_7
am4core.ready(function() {
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
        visits -= Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
        );
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

    chart.events.on("datavalidated", function() {
        dateAxis.zoom(
            {
                start: 1 / 15,
                end: 1.2
            },
            false,
            true
        );
    });

    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;

    document.addEventListener(
        "visibilitychange",
        function() {
            if (document.hidden) {
                if (interval) {
                    clearInterval(interval);
                }
            } else {
                startInterval();
            }
        },
        false
    );

    // add data
    var interval;

    function startInterval() {
        interval = setInterval(function() {
            visits =
                visits +
                Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
            var lastdataItem = series.dataItems.getIndex(
                series.dataItems.length - 1
            );
            chart.addData(
                {
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
    dateAxis.renderer.labels.template.adapter.add("fillOpacity", function(
        fillOpacity,
        target
    ) {
        var dataItem = target.dataItem;
        return dataItem.position;
    });

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on("validated", function() {
        am4core.iter.each(dateAxis.renderer.labels.iterator(), function(label) {
            label.fillOpacity = label.fillOpacity;
        });
    });

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add("rotation", function(
        rotation,
        target
    ) {
        var dataItem = target.dataItem;
        if (
            dataItem.date &&
            dataItem.date.getTime() ==
                am4core.time
                    .round(new Date(dataItem.date.getTime()), "minute")
                    .getTime()
        ) {
            target.verticalCenter = "middle";
            target.horizontalCenter = "left";
            return -90;
        } else {
            target.verticalCenter = "bottom";
            target.horizontalCenter = "middle";
            return 0;
        }
    });

    // bullet at the front of the line
    var bullet = series.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 5;
    bullet.fillOpacity = 1;
    bullet.fill = chart.colors.getIndex(0);
    bullet.isMeasured = false;

    series.events.on("validated", function() {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });
}); // end am4core.ready()

//chart_8
am4core.ready(function() {
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
        visits -= Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
        );
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

    chart.events.on("datavalidated", function() {
        dateAxis.zoom(
            {
                start: 1 / 15,
                end: 1.2
            },
            false,
            true
        );
    });

    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;

    document.addEventListener(
        "visibilitychange",
        function() {
            if (document.hidden) {
                if (interval) {
                    clearInterval(interval);
                }
            } else {
                startInterval();
            }
        },
        false
    );

    // add data
    var interval;

    function startInterval() {
        interval = setInterval(function() {
            visits =
                visits +
                Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
            var lastdataItem = series.dataItems.getIndex(
                series.dataItems.length - 1
            );
            chart.addData(
                {
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
    dateAxis.renderer.labels.template.adapter.add("fillOpacity", function(
        fillOpacity,
        target
    ) {
        var dataItem = target.dataItem;
        return dataItem.position;
    });

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on("validated", function() {
        am4core.iter.each(dateAxis.renderer.labels.iterator(), function(label) {
            label.fillOpacity = label.fillOpacity;
        });
    });

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add("rotation", function(
        rotation,
        target
    ) {
        var dataItem = target.dataItem;
        if (
            dataItem.date &&
            dataItem.date.getTime() ==
                am4core.time
                    .round(new Date(dataItem.date.getTime()), "minute")
                    .getTime()
        ) {
            target.verticalCenter = "middle";
            target.horizontalCenter = "left";
            return -90;
        } else {
            target.verticalCenter = "bottom";
            target.horizontalCenter = "middle";
            return 0;
        }
    });

    // bullet at the front of the line
    var bullet = series.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 5;
    bullet.fillOpacity = 1;
    bullet.fill = chart.colors.getIndex(0);
    bullet.isMeasured = false;

    series.events.on("validated", function() {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });
}); // end am4core.ready()

// am4core.ready(function() {
//     // Themes begin
//     am4core.useTheme(am4themes_animated);
//     // Themes end

//     // Create chart instance
//     var chart = am4core.create("chart_1", am4charts.PieChart);

//     // Add data
//     chart.data = [
//         {
//             source: "Twitter",
//             value: 501.9
//         },
//         {
//             source: "Linkedin",
//             value: 301.9
//         },
//         {
//             source: "Facebook",
//             value: 201.1
//         },
//         {
//             source: "Instagram",
//             value: 165.8
//         }
//     ];

//     // Responsive
//     chart.responsive.enabled = true;
//     chart.responsive.rules.push({
//         relevant: function(target) {
//             if (target.pixelWidth <= 400) {
//                 return true;
//             }
//             return false;
//         },
//         state: function(target, stateId) {
//             if (target instanceof am4charts.PieSeries) {
//                 var state = target.states.create(stateId);

//                 var labelState = target.labels.template.states.create(stateId);
//                 labelState.properties.disabled = true;

//                 var tickState = target.ticks.template.states.create(stateId);
//                 tickState.properties.disabled = true;
//                 return state;
//             }

//             return null;
//         }
//     });
//     // Set inner radius
//     chart.innerRadius = am4core.percent(50);

//     // Add and configure Series
//     var pieSeries = chart.series.push(new am4charts.PieSeries());
//     pieSeries.dataFields.value = "value";
//     pieSeries.dataFields.category = "source";
//     pieSeries.slices.template.stroke = am4core.color("#fff");
//     pieSeries.slices.template.strokeWidth = 2;
//     pieSeries.slices.template.strokeOpacity = 1;
//     pieSeries.labels.template.fill = am4core.color("white");
//     pieSeries.slices.template.tooltipText = "{source}: {value.value}";
//     pieSeries.labels.template.fontSize = 12;

//     var rgm = new am4core.RadialGradientModifier();
//     rgm.brightnesses.push(-0.8, -0.8, -0.5, 0, -0.5);
//     pieSeries.slices.template.fillModifier = rgm;
//     pieSeries.slices.template.strokeModifier = rgm;
//     pieSeries.slices.template.strokeOpacity = 0.4;
//     pieSeries.slices.template.strokeWidth = 0;
//     // This creates initial animation
//     pieSeries.hiddenState.properties.opacity = 1;
//     pieSeries.hiddenState.properties.endAngle = -90;
//     pieSeries.hiddenState.properties.startAngle = -90;

//     pieSeries.colors.list = [
//         am4core.color("#845EC2"),
//         am4core.color("#D65DB1"),
//         am4core.color("#FF6F91"),
//         am4core.color("#FF9671"),
//         am4core.color("#FFC75F"),
//         am4core.color("#F9F871")
//     ];
// }); // end am4core.ready()

// am4core.ready(function() {
//     // Themes begin
//     am4core.useTheme(am4themes_animated);
//     // Themes end

//     var chart = am4core.create("chart_2", am4charts.XYChart);

//     var data = [];
//     var value = 120;

//     var names = [
//         "Raina",
//         "Demarcus",
//         "Carlo",
//         "Jacinda",
//         "Richie",
//         "Antony",
//         "Amada",
//         "Idalia",
//         "Janella",
//         "Marla",
//         "Curtis",
//         "Shellie",
//         "Meggan",
//         "Nathanael",
//         "Jannette",
//         "Tyrell",
//         "Sheena",
//         "Maranda",
//         "Briana",
//         "Rosa",
//         "Rosanne",
//         "Herman",
//         "Wayne",
//         "Shamika",
//         "Suk",
//         "Clair",
//         "Olivia",
//         "Hans",
//         "Glennie"
//     ];

//     for (var i = 0; i < names.length; i++) {
//         value += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
//         data.push({
//             category: names[i],
//             value: value
//         });
//     }

//     chart.data = data;
//     var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
//     categoryAxis.renderer.grid.template.location = 0;
//     categoryAxis.dataFields.category = "category";
//     categoryAxis.renderer.minGridDistance = 15;
//     categoryAxis.renderer.grid.template.location = 0.5;
//     categoryAxis.renderer.grid.template.strokeDasharray = "1,3";
//     categoryAxis.renderer.labels.template.rotation = -90;
//     categoryAxis.renderer.labels.template.horizontalCenter = "left";
//     categoryAxis.renderer.labels.template.location = 0.5;
//     categoryAxis.renderer.labels.template.fontSize = 12;
//     categoryAxis.renderer.labels.template.fill = am4core.color("white");

//     categoryAxis.renderer.labels.template.adapter.add("dx", function(
//         dx,
//         target
//     ) {
//         return -target.maxRight / 2;
//     });

//     var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
//     valueAxis.tooltip.disabled = true;
//     valueAxis.renderer.ticks.template.disabled = true;
//     valueAxis.renderer.axisFills.template.disabled = true;
//     valueAxis.renderer.labels.template.fontSize = 12;
//     valueAxis.renderer.labels.template.fill = am4core.color("white");

//     var series = chart.series.push(new am4charts.ColumnSeries());
//     series.dataFields.categoryX = "category";
//     series.dataFields.valueY = "value";
//     series.tooltipText = "{valueY.value}";
//     series.sequencedInterpolation = true;
//     series.fillOpacity = 0;
//     series.strokeOpacity = 1;
//     series.strokeDashArray = "1,3";
//     series.columns.template.width = 0.01;
//     series.tooltip.pointerOrientation = "horizontal";

//     var bullet = series.bullets.create(am4charts.CircleBullet);

//     chart.cursor = new am4charts.XYCursor();

//     chart.scrollbarX = new am4core.Scrollbar();
//     chart.scrollbarY = new am4core.Scrollbar();
// }); // end am4core.ready()

//$('#asd').hide();
