var json_csv={}

window.onload = get_report();

// send get request to get payroll report
function get_report(){
	$.ajax({
	    url: '/get_current_report/',
	    type: 'GET',
	    contentType: 'application/json; charset=utf-8',
	    success: function(result) {
	    	var table = document.getElementById("report_table_body");
	    	table.innerHTML='';
	    	// create report table
	    	for(var i=0;i<result.length;i++){
	    		var tr = document.createElement('tr');

	    		var eid = document.createElement('td');
	    		eid.innerHTML = result[i].employee_id;
	    		tr.appendChild(eid);

	    		var period = document.createElement('td');
	    		period.innerHTML = result[i].period;
	    		tr.appendChild(period);

	    		var amount = document.createElement('td');
	    		amount.innerHTML = result[i].amount;
	    		tr.appendChild(amount);

	    		table.appendChild(tr);
	    	}
	    }
	});
}

//post csv and get report display
function upload_csv(){
	if(json_csv==[]){
		console.log("no data")
	}
	$.ajax({
	    url: 'upload_csv/'+json_csv['id'],
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    data: JSON.stringify(json_csv['res']),
	    dataType: 'text',
	    success: function(result){
	    	result=JSON.parse(result);
	    	if(result['status']=='success'){
	    		new PNotify({
		        title: "Upload",
		        text: "Upload success",
		        type: "success",
		        delay: 600
		      })
	    		get_report()
	    	}
	    	else if(result['status']=='error'){
	    		new PNotify({
		        title: "Upload",
		        text: "Upload fail:" + result['error_message'],
		        type: "error",
		        delay: 600
		      })
	    	}
	        
	    }
	});
}

//read csv file
function read_csv(files){
    var csv = files[0];
    var name = document.getElementById('local_csv').value.split('\\');
    document.getElementById('select').innerHTML=name[name.length-1];
    
    var fileReader = new FileReader();
    fileReader.onload = function(fileLoadedEvent){
      var textFromFileLoaded = fileLoadedEvent.target.result;
      json_csv=csvJSON(textFromFileLoaded);
  	};
  	
  	try {
	  fileReader.readAsText(csv, "UTF-8");
	}
	catch(error) {
		// if no file selected
		new PNotify({
		        title: "Local File",
		        text: "Please Select a .csv file to upload",
		        type: "error",
		        delay: 600
		})
	} 	
  	
}

//conver csv to json format
function csvJSON(csv){
	var lines=csv.split("\n");
    var result = [];

    var headers=lines[0].replace("\r","").split(",");
    var report_id = lines[lines.length-2].split(",")[1];

    for(var i=1;i<lines.length-2;i++){

	    var obj = {};
	    var currentline=lines[i].replace("\r","");
	    currentline=currentline.split(",");

	    for(var j=0;j<headers.length;j++){
		    obj[headers[j]] = currentline[j];
	    }
	    result.push(obj);
    }
    return {'res':result,'id':report_id};
}