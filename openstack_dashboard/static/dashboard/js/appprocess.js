/**
 * Created by yuhogyun on 2016. 11. 25..
 */
setInterval(function(){
    $.getJSON( "/project/appprocess/json", function( data ) {
        console.log(data);
        if(data.)
    });
    // document.getElementById('build').classList.add('fa-spin');
    // console.log(document.getElementById('build'));
    // document.getElementById('code').classList.remove('fa-spin');
}, 1000);



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