/*! SLIDE BY BILLAL FAUZAN
 Reference: 
*/

$(document).ready(function(){
	$(".slide > div: gt(0)").hide();
	setInterval(function(){
		$(".slide > div: first")
		.fadeOut(100).next().fadeIn(900).end().appendTo(".slide");
	}, 2000);
});
