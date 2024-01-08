
var update_cart = document.getElementsByClassName("update_cart")

for(var i=0; i<update_cart.length; i++){

    update_cart[i].addEventListener('click',function(){
        
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log("Product id:", productID, "action: ",action)

        console.log("User: ", user)

        if (user == "AnonymousUser") {
            addCookieItem(productID, action)
        }
        else
        {
           update_order(productID, action)
        }
        
    })
}

function addCookieItem(productID, action){
    console.log("user is not unauthorized")
    if(action == 'add'){
        if (cart[productID] == undefined){
            cart[productID] = {'quantity':1}
        } else {
            cart[productID]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productID]['quantity'] -= 1
    }
    if(cart[productID]['quantity'] <=0){
        console.log("remove item")
        delete cart[productID]
    }
    console.log('cart: ',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function update_order(productID, action) {
    console.log("sending data....")

    var url = '/update_item/'

    fetch(url,{
        method: 'POST',
        headers:{
            'content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },

        body:JSON.stringify({'productID':productID, 'action':action})
    })

    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('Data', data)
        location.reload()
    })
    
}