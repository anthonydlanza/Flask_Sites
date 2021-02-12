window.onload=function(){
    document.getElementById('compareData').addEventListener('submit', compareData);
}
// changes file to base64 for sending to back end.
function getBase64(file) {
    var result = new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
  return result;
}
// have to make this an async in order to get return from getBase64 function
async function compareData(event){
   let origin = document.getElementById("pageDisplay");
   let li_elements = origin.getElementsByTagName('li');
   for(var i=0;i<li_elements.length;i++){
    console.log(li_elements[i]);
     origin.removeChild(li_elements[i]);
     origin.removeChild(li_elements[i+1]);
   }
   event.preventDefault(); //prevents page refresh
   var postJSON = {}; //create json object
   var allElements = document.getElementsByTagName("*"); //get all form elements
   var file_name = document.getElementById('file').value // get name so we can get extenstion on back end
   // get the file data
   const file = document.querySelector('input[type=file]').files[0]
   // convert the file to base64
   const b64File = await getBase64(file);
   for(var i=0; i < allElements.length; i++){  //build out json object
     if(allElements[i].id == 'file'){
       postJSON[allElements[i].id] = b64File;
       postJSON['file_name'] = file_name;
     }
     else {
       postJSON[allElements[i].id] = allElements[i].value; //creates member of json object
     }
   }
   fetch('/compareSOO', {  //post object to backend for saving to db
       method: 'POST',
       headers : {'content-type': 'application/json'},
       body:JSON.stringify(postJSON)
   }).catch((err)=>console.log(err)).then(function(a) {
      return a.json(); // call the json method on the response to get JSON
  })
  .then(function (json) { // display results
    console.log(json.results.length);
    for(var i=0;i<json.results.length;i++){
        var li_node = document.createElement("li");
        var a = document.createElement("a");
        // var textnode = document.createTextNode(json.results[i].Name);
        a.textContent = json.results[i].Name + ": " + json.results[i].Similarity;
        a.setAttribute('href', "get_code/"+json.results[i].Name);
        li_node.append(a);
        document.getElementById("pageDisplay").append(li_node);
    }
    // console.log(json.results)
  })
}