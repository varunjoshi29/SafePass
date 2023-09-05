function findpath(){
    console.log("findpath!");
    transport = document.getElementsByName('transport')[0].value
    sex = document.getElementsByName('sex')[0].value
    descent = document.getElementsByName('descent')[0].value
    age = document.getElementsByName('age')[0].value
    time = getActualTime()

    console.log(sex,descent,age,time)

    $.ajax({
        url: "/getpath",
        type: 'POST',
        data : {
            transport : transport,
            sex : sex,
            descent : descent,
            age : age,
            time : time
        },
        success: function (response) {
            console.log(response)
            callmap()
            jsonresp = JSON.stringify(response)
        },
        error: function (response) {
            console.log('fail')
        }
    });
}

function getActualTime ()
{var today = new Date()
var h = today.getHours()
if(h < 10){
    h = "0" + h
}
var min = today.getMinutes()
if(min < 10){
    min = "0" + min
}

final = h.toString() +min.toString()
return final
}

function callmap(){
    $.ajax({
        url: "/map",
        type: 'GET',
        success: function (response) {
            document.getElementsByName('mapframe')[0].src = '/map'
        },
        error: function (response) {
            console.log('fail')
        }
    });
}

function searchstart(){
    console.log("searchstart!");
    start = document.getElementsByName('start')[0].value
    $.ajax({
        url: "/searchstart",
        type: 'POST',
        data: {
            startname: start
        },
        success: function (response) {
            console.log(response)
            document.getElementsByName('start')[0].value = response.data
        },
        error: function (response) {
            console.log('fail')
        }
    });
}

function searchdest(){
    console.log("searchdest!");
    dest = document.getElementsByName('destination')[0].value
    $.ajax({
        url: "/searchdest",
        type: 'POST',
        data: {
            destname: dest
        },
        success: function (response) {
            console.log(response)
            document.getElementsByName('destination')[0].value = response.data
        },
        error: function (response) {
            console.log('fail')
        }
    });
}