// Namespace
var rh = rh || {};
rh.chorewheel = rh.chorewheel || {};

// Javascript needed on multiple pages
rh.chorewheel.sharedInit = function() {
	// Dialog Polyfill
	var dialogs = document.querySelectorAll("dialog");
	
	for (var i = 0; i < dialogs.length; i++) {
		var dialog = dialogs[i];
		if (!dialog.showModal) {
			dialogPolyfill.registerDialog(dialog);
		}
	}
	
	// Close dialog buttons
	$(".close").click(function() {
		var nearestDialog = $(this).closest("dialog").get(0);
		nearestDialog.close();
	});
}

// Groups page init
rh.chorewheel.groupsInit = function() {
	$("#groups-add-button").click(function() {
		document.querySelector("#groups-add-dialog").showModal();
		$("#groups-add-dialog input[name=name]").val("");
	});
	
	$(".groups-edit-button").click(function() {
		var key = $(this).closest("tr").find(".group-id").html();
		var name = $(this).closest("tr").find(".group-name").html();
		$("#groups-edit-key").val(key);
		
		document.querySelector("#groups-edit-dialog").showModal();
		document.querySelector("#groups-edit-name").MaterialTextfield.change(name);
	});
	
	$(".groups-delete-button").click(function() {
		var key = $(this).closest("tr").find(".group-id").html();
		$("#groups-delete-key").val(key);
		
		document.querySelector("#groups-delete-dialog").showModal();
	});
}

// Keep at end of file. Call init functions
$(document).ready(function() {
	rh.chorewheel.sharedInit();
	rh.chorewheel.groupsInit();
});