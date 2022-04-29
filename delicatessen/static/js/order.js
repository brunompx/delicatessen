
//Add listeners to update order items
var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		updateOrderItem(this.dataset.product, this.dataset.action)
	})
}

var list_snapshot = []

//Call list function on page load
listItemsInOrder()

//Function for the add and remove arrows
function addItem(item){
	updateOrderItem(item.product_id, "add")
}
function removeItem(item){
	updateOrderItem(item.product_id, "remove")
}

//Add or remove item from Order
function updateOrderItem(productId, action) {
	var url = '/order_update_item/'
	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'productId':productId, 'action':action})
	})
	.then((resp) => { return resp.json(); })
	.then((data) => {
		// location.reload()
		listItemsInOrder()
	});
}

//List order items in right panel
function listItemsInOrder() {
	var wrapper = document.getElementById('summary')
	// wrapper.innerHTML = ''
	
	var url = '/order_item_list/'
	fetch(url, {
		method:'GET',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}
	})
	.then((resp) => resp.json())
	.then(function (data) {
		for (var i in data) {

			//remove the item to re-render
			try{
				document.getElementById(`oi-row-${i}`).remove()
			}catch(err){
			}

			var item = `
				<div id="oi-row-${i}" class="d-flex w-100 justify-content-between mb-1 small">
					<div class="d-flex w-50 justify-content-left">
						<span>${data[i].product_name}</span>
					</div>
					<div class="d-flex w-50 justify-content-between">
						<span>$${data[i].price_total}</span>
						<span>${data[i].quantity} </span>
						<div class="d-flex justify-content-rigth">
							<span class="fa fa-caret-up fa-2x add-item" aria-hidden="true" data-product="${data[i].product_id}" id="add-item${data[i].product_id}"></span>
							<span class="fa fa-caret-down fa-2x remove-item" aria-hidden="true" data-product="${data[i].product_id}" id="remove-item${data[i].product_id}"></span>
						</div>
					</div>
				</div>
				`
			wrapper.insertAdjacentHTML('beforeend', item)
		}

		//remove extra item when an item is removed
		if (list_snapshot.length > data.length){
			for (var i = data.length; i < list_snapshot.length; i++){
				document.getElementById(`oi-row-${i}`).remove()
			}
		}
		list_snapshot = data

		//add listeners to arros
		for (let i in data) {
			let arrowUpBtn = document.getElementById('add-item'+data[i].product_id)
			let arrowDownBtn = document.getElementById('remove-item'+data[i].product_id)

			arrowUpBtn.addEventListener('click', function(){
				addItem(data[i])
			})

			arrowDownBtn.addEventListener('click', function(){
				removeItem(data[i])
			})
		}
	});
}

var orderCheckbox = document.getElementsByClassName('order-check-input')
for (i = 0; i < orderCheckbox.length; i++) {
	orderCheckbox[i].addEventListener('change', e => {
		var checked = false;
		if(e.target.checked){
			checked = true;
		}
		console.log("checkeado-"+e.target.id+e.target.value)
		updateOrderChecks(e.target.value, e.target.id, checked)
	})
}

//Updaye Order paid/delivered boolean fields
function updateOrderChecks(orderId, field, checked) {
	// console.log('-----updateOrder-----')
	var url = '/order_update_checkbox/'
	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'orderId':orderId, 'field':field, 'checked':checked})
	})
	.then((resp) => { return resp.json() })
	.then((data) => {
		location.reload()
	});
}