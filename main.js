var clicks = [];
var bind = false;

function plotclick(event, pos, item)
{
    if (!item)
        return;
    clicks.push(item);
    if (clicks.length == 2) {
        if (clicks[0].datapoint[0] > clicks[1].datapoint[0]) {
            // swap
            var tmp = clicks[0];
            clicks[0] = clicks[1];
            clicks[1] = tmp;
        }
        $.getJSON("/get_json?x0=" + clicks[0].datapoint[0] + "&x1=" + clicks[1].datapoint[0],
                  plot_data);
        return;
    }
    $("#start").css({left: pos.pageX});
    $("#start").show();
}

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

function plot_data(data)
{
    glob_data = data;
    $.plot("#chart", [data['mem']], {
            grid: {hoverable: true, clickable: true},
                yaxis: {tickFormatter: format_y_axis}
                });
    if (!bind) {
        $("#chart").bind("plothover", plothover);
        $("#chart").bind("plotclick", plotclick);
        bind = true;
    }
    clicks = [];
    $("#start").hide();
}

$(function() {
        $.getJSON("/get_json", plot_data);
        $("#start").hide();
})