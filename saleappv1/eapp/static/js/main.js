function addToCart(id, name, price) {
    fetch('/api/carts', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let eles = document.getElementsByClassName("cart-counter");
        for (let e of eles)
            e.innerText = data.total_quantity;
    })
}

function updateCart(id, obj) {
    fetch(`/api/carts/${id}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let eles = document.getElementsByClassName("cart-counter");
        for (let e of eles)
            e.innerText = data.total_quantity;
    })
}