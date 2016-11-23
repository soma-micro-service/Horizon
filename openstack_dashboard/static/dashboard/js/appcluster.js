/**
 * Created by yuhogyun on 2016. 11. 23..
 */

var status = true;


function changeStats(inputStats){
    var boolStats = (inputStats === "true");
    console.log("click bool is" + boolStats);
    if(boolStats){
        document.getElementById('onoffBtn').innerHTML =
            "<span class='fa fa-power-off'></span> Show App Cluster";
    }else{
        document.getElementById('onoffBtn').innerHTML =
            "<span class='fa fa-power-off'></span> Hide App Cluster";
    }

    status = !boolStats;
}