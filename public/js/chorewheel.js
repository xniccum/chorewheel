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
};

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
	//Init sortable
	rh.chorewheel.sortableInit();
	
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
		var key = $(this).closest(".mdl-list__item").find(".chore-key").html();
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
	
	$(".mark-for-approval").click(function() {
		var choreKey = $(this).closest(".mdl-list__item").find(".chore-key").html();
		$.ajax({
			url: "/mark-chore",
			method: "POST",
			data: {
				chorekey: choreKey
			},
			success: function() {
				window.location.reload();
			}
		});
	});
	
	$(".mark-approved").click(function() {
		var choreKey = $(this).closest(".mdl-list__item").find(".chore-key").html();
		$.ajax({
			url: "/mark-chore",
			method: "POST",
			data: {
				chorekey: choreKey
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
	$(".members-delete-button").click(function() {
		var key = $(this).closest(".mdl-card").find(".user-key").html();
		$("#members-delete-key").val(key);

		document.querySelector("#members-delete-dialog").showModal();
	});

	$(".members-edit-button").click(function() {
		var key = $(this).closest(".mdl-card").find(".user-key").html();
		$("#members-edit-key").val(key);

		document.querySelector("#members-edit-dialog").showModal();
	});
};

rh.chorewheel.sortableInit = function() {
	var stop = function(el, li) {
		$this = $(li.item);
		var sorter = $(this);
		var choreKey = $this.find(".chore-key").html();
		console.log($this.closest(".mdl-card"));
		if ($this.closest(".mdl-card").length > 0) {
			var userKey = $this.closest(".mdl-card").find(".user-key").html();
			console.log("userKey: " + userKey);
			$.ajax({
				url: "/assign-chore",
				method: "POST",
				data: {
					chorekey: choreKey,
					assignto: userKey
				},
				success: function() {
					window.location.reload();
				},
				error: function() {
					sorter.sortable("cancel");
				}
			});
		} else {
			$.ajax({
				url: "/unassign-chore",
				method: "POST",
				data: {
					chorekey: choreKey
				},
				success: function() {
					window.location.reload();
				},
				error: function() {
					sorter.sortable("cancel");
				}
			});
		}
	}
	
	var sortable = $(".chores-list, .assigned-chores").sortable({
		appendTo: document.body,
		helper: "clone",
		connectWith: ".assigned-chores, .chores-list",
		items: "> li",
		stop: stop,
		scroll: true
	});
};

// Keep at end of file. Call init functions
$(document).ready(function() {
	rh.chorewheel.sharedInit();
	rh.chorewheel.groupsInit();
	rh.chorewheel.choresInit();
	rh.chorewheel.choreInsertInit();
	rh.chorewheel.membersInit();
});