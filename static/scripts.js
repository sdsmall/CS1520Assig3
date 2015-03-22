function saveTitle() {
	var inputTitle = document.getElementById("title");
	var xmlHttp = createXmlHttp();
	var text = "";
	if(inputTitle) {
		text = inputTitle.value;
		
		var noteID = document.getElementById("note_id").value;
		var paramString = 'title=' + escape(text);
		paramString += '&';
		paramString += 'id=' + noteID;

		xmlHttp.open("POST", '/savetitle', true);
		xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xmlHttp.send(paramString);
	}

	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			var response = xmlHttp.responseText;
			var splitResponse = response.split("|");

			document.getElementById("titleheader").innerHTML = " " + splitResponse[0];
			document.getElementById("dateheader").innerHTML = " " + splitResponse[1];
			document.getElementById("datesaved").innerHTML = " " + splitResponse[1];
			document.getElementById("timesaved").innerHTML = " " + splitResponse[2];
			document.getElementById("displaytitle").style.display = 'block';
			document.getElementById("edittitle").style.display = 'none';
		}
	}
	
	
}

function editTitle() {
	document.getElementById("displaytitle").style.display = 'none';
	document.getElementById("edittitle").style.display = 'block';
}

function saveBodyRedirect() {
	var note_body = "";
	note_body = document.getElementById("notebody").value;
	var noteID = document.getElementById("note_id").value;

	var xmlHttp = createXmlHttp();

	var paramString = 'body=' + escape(note_body);
	paramString += '&';
	paramString += 'id=' + noteID;

	xmlHttp.open("POST", '/manualsave', true);
	xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xmlHttp.send(paramString);

	window.location.assign("../mynotes");
}

function createXmlHttp() {
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	} else {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	if(!(xmlhttp)) {
		alert("Your browser does not support AJAX!");
	}
	return xmlhttp;
}