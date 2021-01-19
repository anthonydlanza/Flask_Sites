$(document).ready(function(){

	var button_element = ""
	var count = 0
	var job = "";

	const nameInput = document.querySelector('#system-name-input');
	const nameDisplay = document.querySelector('#system-name');
	const jobInput = document.querySelector('#job-number-input');
	const jobDisplay = document.querySelector('#job-number');

	nameInput.addEventListener('input',letter =>{
		let nameDisplayTemp = letter.target.value;
		nameDisplayTemp = nameDisplayTemp.split(" ").join("");
		nameDisplayTemp = nameDisplayTemp.split(".").join("");
		nameDisplay.textContent = nameDisplayTemp;
	});

	jobInput.addEventListener('input',letter =>{
		let jobDisplayTemp = letter.target.value;
		jobDisplayTemp = jobDisplayTemp.split(" ").join("");
		jobDisplayTemp = jobDisplayTemp.split(".").join("");
		jobDisplay.textContent = jobDisplayTemp;
	});

	$(".cmd").click(function(){

		// Declare html to send
		$('#ftp-container').css('font-family','');
		$('nav').hide();
		$('.app-container').hide();
		$('.cmd').hide();
		$('.append').hide();
		$('.custom-buttons').hide();
		$('.job-inputs').hide();
		// modify list elements
		$('li').each(function(){
			if(this.id){
				var sys = $("#system-name").text()
				var job = $("#job-number").text()
				this.id= sys + "-" + job + "-" + this.id;
			}
		});
		$('ul').each(function(){
			if(this.id){
				var sys = $("#system-name").text()
				var job = $("#job-number").text()
				this.id= sys + "-" + job + "-" + this.id;
			}
		});
		$('button').each(function(){
			if(this.id){
				var sys = $("#system-name").text()
				var job = $("#job-number").text()
				this.id= sys + "-" + job + "-" + this.id;
			}
		});
		$('div').each(function(){
			if(this.id){
				var sys = $("#system-name").text()
				var job = $("#job-number").text()
				this.id= sys + "-" + job + "-" + this.id;
			}
		});
		$('input').each(function(){
			if(this.id){
				var sys = $("#system-name").text()
				var job = $("#job-number").text()
				this.id= sys + "-" + job + "-" + this.id;
			}
		});
		$('input').each(function(){
			if(this.name){
				var sys = $("#system-name").text()
				var job = $("#job-number").text()
				this.name = sys + "-" + job + "-" + this.name;
			}
		});
		var job_number = $(".job-number-input").val();
		console.log(job_number);
		document.querySelector('#system-name').textContent = "System Name: " + $("#system-name").text();
		document.querySelector('#job-number').textContent = "";
		document.querySelector('#job-number').textContent = "Job Number_440P-" + job_number;
		let html = $('html').html();
		var dataToSend = JSON.stringify({'num':html})
		$.post({
	        type: 'POST',
	        url: '/custom_soo',
	        data: { stuff:html },
	        cache: false,
	        dataType: 'json'
		})
		.done(function(data) {
			// $.get("custom_fpt.html");
		});
		$('.app-container').show();
		$('#ftp-container').css('font-family','Roboto');
		$('nav').show();
		$('.cmd').show();
		$('.custom-buttons').show();
		$('.job-inputs').show();
	});

	$("input").click(function() {

		function display_test_independent(input_1,target){
			$(input_1).each(function(){
				if($(this).prop("checked") == true){
					  $(target).show();
					}
				else if($(this).prop("checked")==false){
				  $(target).hide();
				}
				else{
				  $(this).prop('checked', false);
				}
			});
		}

		function display_test_dependent(input_1,input_2,target){
			$(input_1).each(function(){
				if($(this).prop("checked") == true && $(input_2).prop("checked") == true){
					  $(target).show();
					}
				else if($(this).prop("checked")==false){
				  $(target).hide();
				}
				else{
				  $(this).prop('checked', false);
				}
			});
		}

		function display_test_main(input,target_1,target_2,target_3,target_4,target_5,target_6,target_7){
			$(input).each(function(){
				if($(this).prop("checked") == true){
					  $(target_1).show();
					}
				else if($(this).prop("checked")==false){
				  $(target_1).hide();
				  $(target_2).prop("checked", false);
				  $(target_3).prop("checked", false);
				  $(target_4).prop("checked", false);
				  $(target_5).prop("checked", false);
				  $(target_6).prop("checked", false);
				  $(target_7).prop("checked", false);
				}
				else{
				  $(this).prop('checked', false);
				}
			});
		}

		function display_test_toggle(input_1,input_2,target_1,target_2,target_3,target_4){
			$(input_1).click(function(){
				if($(this).prop("checked") == true){
					  $(input_2).prop("checked", false);
					  $(target_1).hide();
					}
				else if($(input_2).prop("checked")==true){
				  $(input_1).prop("checked", false);
				}
			});
		}
		display_test_independent('input[id="24 Hour Operation"]',"#airsys-process1-div-1000")
		display_test_independent('input[id="24 Hour Operation w Reduced Demand"]',"#airsys-process1-div-2000")
		display_test_independent('input[id="24 Hour Operation w occupied/unoccupied"]',"#airsys-process1-div-3000")
	});
});
