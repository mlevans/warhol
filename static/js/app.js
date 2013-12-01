function take_photos() {
	var url = '/_take_pictures';

	$.ajax({
		url: url,
		success: function(data) {
			handlePhotoList(data);
		},
		dataType: "json",
		error: function(xhr, ts, err) {
			console.log('Error: ', err);
		}
	});
}

function handlePhotoList(data) {
	var url = '/handle_photo_list';

	var requestIntervalID = setInterval(function() {
		console.log('Requesting');
		var xhr = $.ajax({
			url: url,
			data: {timestamp: data['timestamp']},
			success: function(data) {
				if (data['status'] == 0) {
					display_data(data);
					clearInterval(requestIntervalID);
					console.log('No more requesting');
				}
			},
			dataType: "json",
			error: function(xhr, ts, err) {
				console.log('Error: ', err);
			}
		});
	}, 2000);

	////
	//xhr.abort();
	////
}

function display_data(data) {
	if (data) {
		$("#content #status-container").css({height: "380px", "margin-top":"-190px"});
		$("#status-container").html('<h1>All done!</h2><div id="pictures"></div>');
		for (var i=0, len=data.pictures.length; i < len; i++) {
			$('#pictures').append(
			  '<img class="photos" src=' + $SCRIPT_ROOT + '/' + data.pictures[i] + '/>'
			);
		}

		$("#status-container").append('<h1 id="reset">Take some more photos!</h1>');

		$('#reset').bind('click', reset);
	}
}