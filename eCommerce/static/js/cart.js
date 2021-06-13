const button = document.getElementsByClassName('update-cart')

for (var i = 0;i<button.length;i++){
    button[i].addEventListener('click',function(){
       const productId = this.dataset.product;
       const action = this.dataset.action;
    //    console.log(productId,action)  
       if(user === 'AnonymousUser'){
        addCookieItem(productId,action)
       }else{
        updateUserOrder(productId,action)
       }
    })
}


function addCookieItem(productId, action){
	// console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			// console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}


function updateUserOrder(pId,action){
    // console.log("user is authenticated , sending data ....")
    const url = '/itemAdd/'
    fetch(url,{
        method:'POST',
        headers:{
            'content-Type':'application/json' ,
            'x-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'pId':pId,'action':action})
    })
    .then((responce)=>{
        return responce.json()
    })
    .then((data)=>{
        console.log(data)
        // alert(`Item `+ action)
        location.reload()
    })
}