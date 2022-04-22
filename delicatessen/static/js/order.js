
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
				document.getElementById(`cart-row-${i}`).remove()
			}catch(err){
			}

			var item = `
				<div id="cart-row-${i}" class="cart-row task-wrapper flex-wrapper">
					<div style="flex:2"><p>${data[i].product_name}</p></div>
					<div style="flex:1"><p>$ ${data[i].price_total}</p></div>
					<div style="flex:1">
						<p class="quantity">${data[i].quantity}</p>
						<div class="quantity">
						<img data-product="${data[i].product_id}" data-action="add" class="add-item chg-quantity update-cart" src="/static/images/arrow-up.png">
						<img data-product="${data[i].product_id}" data-action="remove" class="remove-item chg-quantity update-cart" src="/static/images/arrow-down.png">
						</div>
					</div>
				</div>
				`
			wrapper.insertAdjacentHTML('beforeend', item)
		}

		//remove extra item when an item is removed
		if (list_snapshot.length > data.length){
			for (var i = data.length; i < list_snapshot.length; i++){
				document.getElementById(`cart-row-${i}`).remove()
			}
		}
		list_snapshot = data

		//add listeners to arros
		for (let i in data) {
			let arrowUpBtn = document.getElementsByClassName('add-item')[i]
			let arrowDownBtn = document.getElementsByClassName('remove-item')[i]

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