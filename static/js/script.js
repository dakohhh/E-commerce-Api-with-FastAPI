
const buttons = document.querySelectorAll('#_form-btn');


buttons.forEach(button => {

    button.addEventListener("click", async (event)=>{
            event.preventDefault();
    
            const form = button.closest('.__form');

            const url = form.action;

           
            const input_dert = form.elements["dert"];

            const cart_lenght = document.getElementById("cart_lenght")

            const icon = document.createElement("i");

            icon.classList.add("fa", "fa-trash");

            
            if (input_dert.value === "add"){

                const response = await fetch(url, {
                    method: 'POST',
                });

                const icon = document.createElement("i");
                
                input_dert.value = "remove"

                button.className = "btn btn-outline-danger";                

                button.innerHTML = '<i class="fa fa-trash"></i> Remove from cart';

                cart_lenght.textContent = +cart_lenght.textContent + 1;
                


            }
            else if (input_dert.value === "remove"){

                const response = await fetch(url, {
                    method: 'DELETE',
                });

                input_dert.value = "add";

                button.className = "btn btn-primary";
                
                button.innerHTML = "Add to cart";

                cart_lenght.textContent = +cart_lenght.textContent -1;
                
            }

            else if (input_dert.value === "save"){

                

                const response = await fetch(url, {
                    method: 'POST',
                });
                
                input_dert.value = "saved";

                button.className = "btn btn-outline-primary";

                button.innerHTML = '<i class="fa fa-check"></i> Saved';

            }

            else if (input_dert.value === "saved"){


                const response = await fetch(url, {
                    method: 'DELETE',
                });

                input_dert.value = "save";

                button.className = "btn btn-outline-success";

                button.innerHTML = '<i class="fa fa-heart"></i> Save';
            
            }
            else if(input_dert.value === "rmvc"){


                const response = await fetch(url, {
                    method: 'DELETE',
                });

                const item = button.closest('#Item');

                const price_list = document.getElementsByClassName("price")
                const cost_of_item = item.querySelector(".cost")
                const check_out_price =  document.querySelector(".check-price")
                const total_price =  document.getElementById("total_price");
                

                let new_price;

                price_list.forEach(price => {
                    new_price = parseFloat(`${parseFloat(price.textContent.replace("$", "")) - parseFloat(cost_of_item.textContent.replace("$", ""))}`).toFixed(2)

                    price.textContent = new_price
                })

                check_out_price.textContent =  ` Checkout: $${new_price}`
                cart_lenght.textContent = +cart_lenght.textContent -1;

                total_price.value = new_price;
                
                item.remove()


                const all_items = document.querySelectorAll("#Item")

                if (all_items.length == 0){
                    const item_container = document.querySelector(".__items");
                    const nothing_elem = document.createElement("h3")

                    nothing_elem.textContent = "Nothing in your cart...."
                    nothing_elem.style = "text-align: center;"
                    item_container.prepend(nothing_elem);


                    const check_btn = document.getElementById("check-btn")
                    const apply_btn = document.getElementById("app-btn")

                    check_btn.disabled = true;
                    apply_btn.disabled = true;


                }


            }


        })
});


function alert_close(){
    const alert = document.getElementById("__alert")
    alert.remove()
}










