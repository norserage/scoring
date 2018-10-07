
function inject_notification(injects) {
    var now = new Date();
    $.each(injects, function (index, item) {
        console.log(item)
        var item_date = new Date(Date.parse(item['when'][0] + "T" + item['when'][1] + "Z"));
        console.log(now);
        console.log(item_date);
        if (now.getFullYear() == item_date.getFullYear() && now.getMonth() == item_date.getMonth() && now.getDate() === item_date.getDate() && now.getHours() === item_date.getHours() && now.getMinutes() === item_date.getMinutes()) {
            send_notification("Lepus ISE - New Inject", item['subject'], "/inject/" + item['id'], "inject")
        }
    })
}

function inject_display(injects) {
    if (injects.length > 0) {
        $("#injects").html("<ol id=\"inject_list\"></ol>");
        $.each(injects, function (index, item) {
            var new_inject = $("<li></li>").html("<a href=\"/inject/"+item['id']+"\">"+item['subject']+"</a>");
            new_inject.appendTo("#inject_list")
        })
    }
    else {
        $("#injects").html("<p>There are no current injects</p>");
    }
}

function inject_check_loop() {
    $.get("/portal/injects/json", function(t) {
        inject_notification(t);
        inject_display(t);
    });
}

function send_notification(title, text, url, tag) {
    if (window.Notification) {
        function isn() {
            var img = '/static/img/bunnyshield_square.png';
            var notification = new Notification(title, {body: text, icon: img, tag: tag})
            notification.onclick = function (ev) {
              ev.preventDefault();
              window.open(url, '_blank');
            };
        }
        if (Notification.permission === "granted") {
            isn();
        }
        else if (Notification.permission !== "denied") {
            Notification.requestPermission(function (permission) {
                if (permission === "granted") {
                    isn();
                }
            });
        }
    }
}

var coolerInterval = function(func, interval, triggerOnceEvery) {

    var startTime = new Date().getTime(),
        nextTick = startTime,
        count = 0;

    triggerOnceEvery = triggerOnceEvery || 1;

    var internalInterval = function() {

        nextTick += interval;
        count++;

        if(count == triggerOnceEvery) {

            func();
            count = 0;
        }

        setTimeout(internalInterval, nextTick - new Date().getTime());
    };

    internalInterval();

};

$(function() {
    coolerInterval(inject_check_loop, 1000, 60)
    inject_check_loop()
    //setInterval(inject_check_loop, 60000);
})