$(document).ready(function(){

	var button_element = ""
	var count = 0

	$("#cmd").click(function(){

		// Declare html to send
		$('#ftp-container').css('font-family','');
		$('nav').hide();
		$('#app-container').hide();
		$('#cmd').hide();
		$('.append').hide();
		$('.custom-buttons').hide();
		let html = $('html').html();
		var dataToSend = JSON.stringify({'num':html})
		$.post({
	        type: 'POST',
	        url: '/custom_fpt',
	        data: { stuff:html },
	        cache: false,
	        dataType: 'json'
		})
		.done(function(data) {
			// $.get("custom_fpt.html");
		});
		$('#ftp-container').css('font-family','Roboto');
		$('nav').show();
		$('#app-container').show();
		$('#cmd').show();
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

		display_test_independent('input[id="Air System Resources"]',".resources")
		display_test_independent('input[id="Field Panel Preparation"]',".field-panel-prep")
		display_test_independent('input[id="Air System Relinquish Default Check"]',".airsys-relinquish")
		display_test_independent('input[id="Air System Basic Hardware Check"]',".airsys-hardware")
		display_test_independent('input[id="Occupied Mode 24 Hour"]',".occupied-24")
		display_test_independent('input[id="Occupied Mode Scheduled"]',".occupied-24")
		display_test_independent('input[id="Occupied Mode Scheduled"]',".airsys-occupied-sched")
		display_test_independent('input[id="Return from Power Loss Reset"]',".airsys-power-return")
		display_test_independent('input[id="Discharge Static Control"]',".sup-static-control")
		display_test_independent('input[id="Discharge Static Reset"]',".sup-static-reset")
		display_test_independent('input[id="Discharge Flow Control"]',".sup-flow-control")
		display_test_independent('input[id="Discharge Flow Reset"]',".sup-flow-reset")
		display_test_independent('input[id="Building Static Control - Exhaust Damper"]',".building-static-control")
		display_test_independent('input[id="Building Static Control - Return Fan"]',".building-static-control")
		display_test_independent('input[id="Return Static Control - Exhaust Damper"]',".return-static-control")
		display_test_independent('input[id="Return Static Control - Return Fan"]',".return-static-control")
		display_test_independent('input[id="Return Flow Control - CFM Offset"]',".return-offset-control")
		display_test_independent('input[id="Exhaust Static Control"]',".exh-static-control")
		display_test_independent('input[id="Exhaust Static Reset"]',".exh-static-reset")
		display_test_independent('input[id="Economizer Control"]',".economizer")
		display_test_independent('input[id="Discharge Temperature Control"]',".temperature-control")
		display_test_independent('input[id="Discharge Temperature Reset"]',".temp-reset")
		display_test_independent('input[id="Discharge Humidity Control"]',".humidity-control")
		display_test_independent('input[id="Dehumidification Control"]',".dehumidification")
		display_test_independent('input[id="Demand Control Ventilation"]',".dcv")
		display_test_independent('input[id="Fan Wall Lead/Lag + Weekly turnover"]',".lead-lag")
		display_test_independent('input[id="Alarm Checking"]',".alarming")

		// Main Schedule
		display_test_main('input[id="Unoccupied Mode"]',".unoccupied",'input[id="Optimum Stop when Heating"]','input[id="Optimum Stop when Cooling"]','input[id="Night Setback Heating"]','input[id="Night Setback Cooling"]','input[id="Optimum Start (Morning Warm-up)"]','input[id="Optimum Start (Morning Cool-down)"]')

		// Scheduled Stuff
		display_test_dependent('input[id="Optimum Stop when Heating"]','input[id="Unoccupied Mode"]',".stopheat")
		display_test_dependent('input[id="Optimum Stop when Cooling"]','input[id="Unoccupied Mode"]',".stopcool")
		display_test_dependent('input[id="Night Setback Heating"]','input[id="Unoccupied Mode"]',".ngtheat")
		display_test_dependent('input[id="Night Setback Cooling"]','input[id="Unoccupied Mode"]',".ngtcool")
		display_test_dependent('input[id="Optimum Start (Morning Warm-up)"]','input[id="Unoccupied Mode"]',".warmup")
		display_test_dependent('input[id="Optimum Start (Morning Cool-down)"]','input[id="Unoccupied Mode"]',".cooldown")
			


	});
});
