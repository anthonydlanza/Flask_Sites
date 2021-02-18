window.onload=function(){
    document.getElementById('contributeData').addEventListener('submit', contributeData);
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
async function contributeData(event){
  event.preventDefault(); //prevents page refresh
  var postJSON = {}; //create json object
  var allElements = document.getElementsByTagName("*"); //get all form elements
  var program_file_name = document.getElementById('contribute-pcl').value // get name so we can get extenstion on back end
  var soo_file_name = document.getElementById('contribute-soo').value // get name so we can get extenstion on back end
  // get the file data
  const program_file = document.querySelector('#contribute-pcl').files[0]
  const soo_file = document.querySelector('#contribute-soo').files[0]
  // convert the file to base64
  const b64File_program = await getBase64(program_file);
  const b64File_soo = await getBase64(soo_file);
  for(var i=0; i < allElements.length; i++){  //build out json object
     if(allElements[i].id == 'contribute-pcl'){
       postJSON[allElements[i].id] = b64File_program;
       postJSON['program_file_name'] = program_file_name;
     }
     else if(allElements[i].id == 'contribute-soo'){
       postJSON[allElements[i].id] = b64File_soo;
       postJSON['soo_file_name'] = soo_file_name;
     }
     else {
       postJSON[allElements[i].id] = allElements[i].value; //creates member of json object
     }
  }
  fetch('/save_code', {  //post object to backend for saving to db
     method: 'POST',
     headers : {'content-type': 'application/json'},
     body:JSON.stringify(postJSON)
  }).catch((err)=>console.log(err))
}