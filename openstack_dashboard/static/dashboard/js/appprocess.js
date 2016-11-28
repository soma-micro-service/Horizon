/**
 * Created by yuhogyun on 2016. 11. 25..
 */

var processStatus = -1;

setInterval(function(){
    $.getJSON( "/project/appprocess/json", {jenkinsUrl: ""} ,function(data) {
        console.log(data.phase);
        spinIcon(data.phase);
    });
}, 1000);

function spinIcon(index){
    processStatus = index;
    switch (index) {
        case 1:
            console.log(document.getElementById('code'));
            document.getElementById('code').classList.add('fa-spin');
            document.getElementById('build').classList.remove('fa-spin');
            document.getElementById('build').classList.remove('fa-spin');
            document.getElementById('provisioning').classList.remove('fa-spin');
            document.getElementById('running').classList.remove('fa-spin');
            document.getElementById('result').innerText = "";
            break;
        case 2:
            document.getElementById('code').classList.remove('fa-spin');
            document.getElementById('build').classList.add('fa-spin');
            document.getElementById('test').classList.remove('fa-spin');
            document.getElementById('provisioning').classList.remove('fa-spin');
            document.getElementById('running').classList.remove('fa-spin');
            document.getElementById('result').innerText = "";
            break;
        case 3:
            document.getElementById('code').classList.remove('fa-spin');
            document.getElementById('build').classList.remove('fa-spin');
            document.getElementById('test').classList.add('fa-spin');
            document.getElementById('provisioning').classList.remove('fa-spin');
            document.getElementById('running').classList.remove('fa-spin');
            document.getElementById('result').innerText = "";
            break;
        case 4:
            document.getElementById('code').classList.remove('fa-spin');
            document.getElementById('build').classList.remove('fa-spin');
            document.getElementById('test').classList.remove('fa-spin');
            document.getElementById('provisioning').classList.add('fa-spin');
            document.getElementById('running').classList.remove('fa-spin');
            document.getElementById('result').innerText = "";
            break;
        case 5:
            document.getElementById('code').classList.remove('fa-spin');
            document.getElementById('build').classList.remove('fa-spin');
            document.getElementById('test').classList.remove('fa-spin');
            document.getElementById('provisioning').classList.remove('fa-spin');
            document.getElementById('running').classList.add('fa-spin');
            document.getElementById('result').innerText = "";
            break;
        case 6:
            document.getElementById('code').classList.remove('fa-spin');
            document.getElementById('build').classList.remove('fa-spin');
            document.getElementById('test').classList.remove('fa-spin');
            document.getElementById('provisioning').classList.remove('fa-spin');
            document.getElementById('running').classList.remove('fa-spin');
            document.getElementById('result').innerText = "Build FAILURE";
    }
}



//code
//document.getElementById('code').classList.add('fa-spin');
//document.getElementById('code').classList.remove('fa-spin');


//build
//document.getElementById('build').classList.add('fa-spin');
//document.getElementById('build').classList.remove('fa-spin');

//test
//document.getElementById('test').classList.add('fa-spin');
//document.getElementById('test').classList.remove('fa-spin');

//provision
//document.getElementById('provisioning').classList.add('fa-spin');
//document.getElementById('provisioning').classList.remove('fa-spin');

//running
//document.getElementById('running').classList.add('fa-spin');
//document.getElementById('running').classList.remove('fa-spin');