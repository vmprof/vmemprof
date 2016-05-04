function zoom_out()
{
    $.getJSON("/get_json", plot_data);
    clicks = [];
}

function plothover(event, pos, item)
{
    var x = Math.ceil(pos);
    if (item) {
        $("#stacktrace").html(glob_data.mem[item.dataIndex][2]);
    }
}

function format_y_axis(val, axis)
{
    if (val > 1024) {
        return (val / 1024).toFixed() + " MiB";
    }
    return val + " KiB";
}

var lastWindow = {};
function resample(render, plot)
{
    var xAxis = plot.getXAxes()[0];
    var newWindow = {
        x0: Math.floor(xAxis.min),
        x1: Math.ceil(xAxis.max)
    };
    if (newWindow.x0 != lastWindow.x0 || newWindow.x1 != lastWindow.x1) {
        $.getJSON("/get_json?x0=" + newWindow.x0 + "&x1=" + newWindow.x1, render);
        lastWindow = newWindow;
    }
}

function plot_data(data)
{
    glob_data = data;
    var axesMax = {
        x: Math.ceil(data.mem[data.mem.length-1][0]),
        y: Math.max.apply(null, data.mem.map(function (x) { return x[1]; }))
    };
    var axesMargin = {
        x: 0.05 * axesMax.x,
        y: 0.05 * axesMax.y
    }
    var maxAxesWindows = {
        x: [-axesMargin.x, axesMax.x + axesMargin.x],
        y: [-axesMargin.y, axesMax.y + axesMargin.y],
    };

    var plotOpts = {
        grid: {hoverable: true, clickable: true},
        xaxis: {panRange: maxAxesWindows.x},
        yaxis: {panRange: maxAxesWindows.y, tickFormatter: format_y_axis},
        zoom: {interactive: true},
        pan: {interactive: true}
    };
    function render(data) {
        $.plot("#chart", [data.mem], plotOpts);
    }

    render(data);

    $("#chart").bind("plothover", plothover);
    var resampleZoom = $.debounce(10, resample);
    var resamplePan = $.debounce(100, resample);
    $("#chart").on("plotzoom", function (event, plot) { resampleZoom(render, plot); });
    $("#chart").on("plotpan", function (event, plot) { resamplePan(render, plot); });
}

$(function() {
    $.getJSON("/get_json", plot_data);
})
