var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		updateUserOrder(productId, action)

	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

	var wrapper = document.getElementById('summary')

	var url = '/order_update_item/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'productId':productId, 'action':action})
	})
	.then((resp) => resp.json())
	.then(function (data) {

		console.log('llego', data)

		var list = data
		for (var i in list) {
			console.log('item-name: ', i.product_name)
			var item = `
				<div class="cart-row">
					<div style="flex:2"><p>${i.product_name}</p></div>
					<div style="flex:1"><p>${i.price_total}</p></div>
					<div style="flex:1">
						<p class="quantity">${i.quantity}</p>

					</div>
				</div>
				`
			wrapper.innerHTML += item
		}
		
	});
}