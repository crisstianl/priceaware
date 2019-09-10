// global variables

window.onload = function() {
	console.log("base page load...");
}

function on_history_selected(value) {
	return true;
}

function showSpinner() {
	const spinner = document.getElementById("spinner");
	spinner.style.display = "block";
}

function showToast(msg) {
	const toast = document.getElementById("toast");
	// attach close action
	const toast_close = toast.querySelector(".close");
	if(!toast_close.onclick) {
		toast_close.onclick = function() {
			toast.classList.remove("show");
			toast.classList.add("hide");
		};
	}

	// attach message
	const toast_body = toast.querySelector(".toast-body");
	if(!toast_body.clear) {
		toast_body.clear = function() {
			while(this.firstChild) {
				this.removeChild(this.firstChild);
			}
		};
	}
	let ul = document.createElement('ul');
	if(Array.isArray(msg)) {
		for (let i = 0; i < msg.length; i++) {
			let li = document.createElement('li');
			li.appendChild(document.createTextNode(String(msg[i])));
			ul.appendChild(li);
		}
	} else {
		let li = document.createElement('li');
		li.appendChild(document.createTextNode(String(msg)));
		ul.appendChild(li);
	}
	toast_body.clear();
	toast_body.appendChild(ul);

	// toggle visibility
	toast.classList.remove("hide");
	toast.classList.add("show");
	setTimeout(function() { 
		toast.classList.remove("show");
		toast.classList.add("hide");
		toast_body.clear();
	}, 5000);	
}

function showDialog(msg, on_confirm, on_cancel) {
	const dialog = document.getElementById("modal");
	// attach close action
	const dialog_close = dialog.querySelector(".close");
	if(!dialog_close.onclick) {
		dialog_close.onclick = function() {
			dialog.classList.remove("show");
			dialog.style.display = "none";
		};
	}

	// attach confirm action
	const dialog_confirm = dialog.querySelector(".btn-primary");
	dialog_confirm.onclick = function() {
		dialog.classList.remove("show");
		dialog.style.display = "none";
		if(on_confirm) {
			on_confirm();
		}
	};

	// attach cancel action
	const dialog_cancel = dialog.querySelector(".btn-secondary");
	dialog_cancel.onclick = function() {
		dialog.classList.remove("show");
		dialog.style.display = "none";
		if(on_cancel) {
			on_cancel();
		}
	};

	// attach message
	const dialog_body = dialog.querySelector(".modal-body");
	dialog_body.innerHTML = msg;

	// show
	dialog.style.display = "block";
	dialog.classList.add("show");
}