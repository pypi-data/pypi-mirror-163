function getBaseUrl() {
    return window.location.origin;
}

function getTorrentCountUrl() {
    return getBaseUrl() + "/api/torrent/count";
}

function getTorrentMetricsUrl(secondsFromNow, count, timeAxisFormat) {
    return getBaseUrl() + "/api/torrent/metrics" + "?SecondsFromNow=" + secondsFromNow + "&Count=" + count + "&TimeAxisFormat=" + timeAxisFormat;
}

function getTorrentCategoriesUrl() {
    return getBaseUrl() + "/api/torrent/categories";
}

function LiveTorrentChart(container, label, timeDelta, count, timeAxisFormat, refresh_rate, height = 64) {
    let canvas = document.createElement("canvas");
    canvas.id = container + "_" + label
    canvas.height = height

    const chart = new Chart(canvas.getContext("2d"), {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: label,
                    data: [],
                    fill: false,
                    tension: 0.42
                }
            ],
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    x: {
                        beginAtZero: true
                    }
                },
                borderColor: 'rgba(38, 166, 91, 128)'
            }
        }
    });

    document.getElementById(container).appendChild(canvas);

    function onResponse(data) {
        chart.data.labels = data["labels"];
        chart.data.datasets[0].data = data["values"];
        chart.update();
    }

    function reload() {
        fetch(getTorrentMetricsUrl(timeDelta, count, timeAxisFormat)).then((rsp) => rsp.json()).then((data) => onResponse(data));
    }

    reload();

    let timer = setInterval(reload, refresh_rate);

    this.stop = function() {
        if(timer) {
            clearInterval(timer);
            timer = null;
        }
        return this;
    }

    this.start = function () {
        if(!timer) {
            this.stop();
            timer = setInterval(reload, refresh_rate);
        }
        return this;
    }
}

function TorrentCategoryChart(container, label, height = 32) {
    let canvas = document.createElement("canvas");
    canvas.id = container + "_" + label
    canvas.height = height

    const chart = new Chart(canvas.getContext("2d"), {
        type: "doughnut",
        data: {
            labels: [],
            datasets: [
                {
                    label: label,
                    data: [],
                    fill: false,
                    tension: 0.42
                }
            ],
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    x: {
                        beginAtZero: true
                    }
                },
                borderColor: 'rgba(38, 166, 91, 128)'
            }
        }
    });

    document.getElementById(container).appendChild(canvas);

    function onResponse(data) {
        chart.data.labels = data["labels"];
        chart.data.datasets[0].data = data["values"];
        chart.update();
    }

    function reload() {
        fetch(getTorrentCategoriesUrl()).then((rsp) => rsp.json()).then((data) => onResponse(data));
    }

    reload();
}