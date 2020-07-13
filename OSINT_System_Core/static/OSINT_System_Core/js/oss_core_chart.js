//chart_7
am4core.ready(function () {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chart_6", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0;

    chart.padding(0, 0, 0, 0);

    chart.zoomOutButton.disabled = true;

    const data = [];
    var visits = 10;
    var i = 0;

    for (i = 0; i <= 30; i++) {
        visits -= Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
        );
        data.push({
            date: new Date().setSeconds(i - 30),
            value: visits,
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
        dateAxis.zoom(
            {
                start: 1 / 15,
                end: 1.2,
            },
            false,
            true
        );
    });

    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;

    document.addEventListener(
        "visibilitychange",
        function () {
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

    var interval;

    function startInterval() {
        interval = setInterval(function () {
            visits =
                visits +
                Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
            var lastdataItem = series.dataItems.getIndex(
                series.dataItems.length - 1
            );
            $.ajax({
                type: "GET",
                dataType: "json",
                url: "http://localhost:8000/core/update_internet_stats",
                success: function (e) {
                    console.log("in interval of upload speed");
                    upload = e.upload / 100000;

                    chart.addData(
                        {
                            date: new Date(lastdataItem.dateX.getTime() + 1000),
                            value: upload,
                        },
                        1
                    );
                },

                error: function (error) {
                    console.log("in error function");
                    console.log(error);
                },
            });
        }, 300000);
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
    dateAxis.renderer.labels.template.adapter.add("fillOpacity", function (
        fillOpacity,
        target
    ) {
        var dataItem = target.dataItem;
        return dataItem.position;
    });

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on("validated", function () {
        am4core.iter.each(dateAxis.renderer.labels.iterator(), function (
            label
        ) {
            label.fillOpacity = label.fillOpacity;
        });
    });

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add("rotation", function (
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

    series.events.on("validated", function () {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });
}); // end am4core.ready()

//chart_7
am4core.ready(function () {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chart_7", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0;

    chart.padding(0, 0, 0, 0);

    chart.zoomOutButton.disabled = true;

    const data = [];
    var visits = 10;
    var i = 0;

    for (i = 0; i <= 30; i++) {
        visits -= Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
        );
        data.push({
            date: new Date().setSeconds(i - 30),
            value: visits,
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
        dateAxis.zoom(
            {
                start: 1 / 15,
                end: 1.2,
            },
            false,
            true
        );
    });

    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;

    document.addEventListener(
        "visibilitychange",
        function () {
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

    var interval;

    function startInterval() {
        interval = setInterval(function () {
            visits =
                visits +
                Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 5);
            var lastdataItem = series.dataItems.getIndex(
                series.dataItems.length - 1
            );
            $.ajax({
                type: "GET",
                dataType: "json",
                url: "http://localhost:8000/core/update_internet_stats",
                success: function (e) {
                    console.log("in interval of download speed");
                    download = e.download / 1000000;

                    chart.addData(
                        {
                            date: new Date(lastdataItem.dateX.getTime() + 1000),
                            value: download,
                        },
                        1
                    );
                },

                error: function (error) {
                    console.log("in error function");
                    console.log(error);
                },
            });
        }, 300000);
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
    dateAxis.renderer.labels.template.adapter.add("fillOpacity", function (
        fillOpacity,
        target
    ) {
        var dataItem = target.dataItem;
        return dataItem.position;
    });

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on("validated", function () {
        am4core.iter.each(dateAxis.renderer.labels.iterator(), function (
            label
        ) {
            label.fillOpacity = label.fillOpacity;
        });
    });

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add("rotation", function (
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

    series.events.on("validated", function () {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });
}); // end am4core.ready()

//chart_8
am4core.ready(function () {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create("chart_8", am4charts.XYChart);

    chart.data = [
        {
            worker: "Uavatar_workerSA",
            tasks: 1,
        },
        {
            worker: "fb_worker",
            tasks: 1,
        },
        {
            worker: "generic_worker",
            tasks: 1,
        },
        {
            worker: "instareddit_worker",
            tasks: 1,
        },
        {
            worker: "linkedin_worker",
            tasks: 1,
        },
        {
            worker: "news_worker",
            tasks: 1,
        },
        {
            worker: "super_worker",
            tasks: 1,
        },
        {
            worker: "twitter_worker",
            tasks: 1,
        },
        {
            worker: "youtube_worker",
            tasks: 1,
        },
    ];

    console.log("ajax request for micro crawler stats");
    setInterval(function () {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "http://localhost:8000/core/update_micro_crawler_stats",
            success: function (data) {
                console.log("Tasks Chart ");
                var celery_worker_avatar_worker =
                    data[0].active_workers["celery@avatar_worker"].length;
                var celery_worker_fb_worker =
                    data[0].active_workers["celery@fb_worker"].length;
                var celery_worker_generic_worker =
                    data[0].active_workers["celery@generic_worker"].length;
                var celery_worker_instareddit_worker =
                    data[0].active_workers["celery@instareddit_worker"].length;
                var celery_worker_linkedin_worker =
                    data[0].active_workers["celery@linkedin_worker"].length;
                var celery_worker_news_worker =
                    data[0].active_workers["celery@news_worker"].length;
                var celery_worker_super_worker =
                    data[0].active_workers["celery@super_worker"].length;
                var celery_worker_twitter_worker =
                    data[0].active_workers["celery@twitter_worker"].length;
                var celery_worker_youtube_worker =
                    data[0].active_workers["celery@youtube_worker"].length;

                workers_task_count = [
                    celery_worker_avatar_worker,
                    celery_worker_fb_worker,
                    celery_worker_generic_worker,
                    celery_worker_instareddit_worker,
                    celery_worker_linkedin_worker,
                    celery_worker_news_worker,
                    celery_worker_super_worker,
                    celery_worker_twitter_worker,
                    celery_worker_youtube_worker,
                ];
                workers_names = [
                    "avatar_worker",
                    "fb_worker",
                    "generic_worker",
                    "instareddit_worker",
                    "linkedin_worker",
                    "news_worker",
                    "super_worker",
                    "twitter_worker",
                    "youtube_worker",
                ];
                console.log(workers_task_count);
                chart_data = [];

                var dict = {};

                for (var z = 0; z <= workers_names.length; z++) {
                    var dict = {
                        worker: "" + workers_names[z],
                        tasks: workers_task_count[z],
                    };
                    chart_data.push(dict);
                }

                console.log(chart_data);
                chart.data = chart_data;
            },

            error: function (error) {
                console.log("in error function");
                console.log(error);
            },
        });
    }, 300000);

    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "worker";
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.minGridDistance = 30;

    categoryAxis.renderer.labels.template.adapter.add("dy", function (
        dy,
        target
    ) {
        if (target.dataItem && target.dataItem.index & (2 == 2)) {
            return dy + 25;
        }
        return dy;
    });
    categoryAxis.renderer.grid.template.disabled = true;
    categoryAxis.renderer.labels.template.disabled = true;
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.renderer.line.disabled = true; //disables axis line
    valueAxis.renderer.labels.template.disabled = true; //disables labels
    valueAxis.renderer.grid.template.disabled = true; //disables grid
    // Create series
    var series = chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = "tasks";
    series.dataFields.categoryX = "worker";
    series.name = "tasks";
    series.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
    series.columns.template.fillOpacity = 0.8;

    var columnTemplate = series.columns.template;
    columnTemplate.strokeWidth = 2;
    columnTemplate.strokeOpacity = 1;
});
