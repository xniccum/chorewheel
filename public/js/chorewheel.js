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
		var name = $(this).closest("tr").find(".group-name").find("a").text();
		$("#group-key").val(key);
		
		document.querySelector("#groups-edit-dialog").showModal();
		document.querySelector("#groups-edit-name").MaterialTextfield.change(name);
	});
	
	$(".groups-delete-button").click(function() {
		var key = $(this).closest("tr").find(".group-id").html();
		$("#groups-delete-key").val(key);
		
		document.querySelector("#groups-delete-dialog").showModal();
	});
};

// Chores page init
rh.chorewheel.choresInit = function() {
	// Initialize the date picker widget.
	$("input[name=due]").bootstrapMaterialDatePicker({
		format : 'MM-DD-YYYY hh:mm A',
		shortTime : true
	});
	
	$("#chores-add-chore").click(function() {
		document.querySelector("#chores-add-dialog").showModal();
		$("#chores-add-dialog input[name=name]").val("");
		$("#chores-add-dialog input[name=due]").val("");
		$("#chores-add-dialog input[name=frequency]").val("");
		$("#chores-add-dialog input[name=points]").val("");
	});
	
	$("#chores-add-member").click(function() {
		document.querySelector("#chores-add-member-dialog").showModal();
		$("#chores-add-member-dialog input[name=email]").val("");
	});
	
	$(".chores-edit-button").click(function() {
		var key = $(this).closest("tr").find(".chore-key").html();
		var name = $(this).closest("tr").find(".chore-name").html();
		var due = $(this).closest("tr").find(".chore-due").html();
		var frequency = $(this).closest("tr").find(".chore-frequency").html();
		var points = $(this).closest("tr").find(".chore-points").html();
		
		document.querySelector("#chores-edit-dialog").showModal();

		$("#chores-edit-key").val(key);
		document.querySelector("#chores-edit-name").MaterialTextfield.change(name);
		document.querySelector("#chores-edit-due").MaterialTextfield.change(due);
		document.querySelector("#chores-edit-points").MaterialTextfield.change(points);
		$("#chores-edit-dialog input[name=frequency]").attr("data-val", frequency);
	});
	
	$(".chores-delete-button").click(function() {
		var key = $(this).closest("tr").find(".chore-key").html();
		$("#chores-delete-key").val(key);
		
		document.querySelector("#chores-delete-dialog").showModal();
	});
	
	$("#assigned-to").on("change", function() {
		var choreKey = $(this).closest("tr").find(".chore-key").html();
		var assignTo = $(this).attr("data-val");
		$.ajax({
			url: "/assign-chore",
			method: "POST",
			data: {
				chorekey: choreKey,
				assignto: assignTo
			},
			success: function() {
				window.location.reload();
			}
		});
	});
};

rh.chorewheel.choreInsertInit = function() {
	$("#insert-chore-form").submit(function() {
		var freq = $("#frequency").attr("data-val");
		$("#frequency").val(freq);
	});
	
	var freq = $("#frequency").attr("data-val")
	if (freq) {
		$("#frequency").val($(".mdl-menu__item[data-val='" + freq + "']").html())
	}
};

rh.chorewheel.membersInit = function() {
	console.log("TODO");
}

// Keep at end of file. Call init functions
$(document).ready(function() {
	rh.chorewheel.sharedInit();
	rh.chorewheel.groupsInit();
	rh.chorewheel.choresInit();
	rh.chorewheel.choreInsertInit();
	rh.chorewheel.membersInit();
});