



let stripe = Stripe('pk_test_51MiUdoGx7WvS8Y8QPsM7IImIhobagdxQe9Nrq2M2sl6Bmdjoxwqxgxparnu6nrCOaLYZ5ccMyAEk94zgdtkqjmhO00JSEqWL8D');

document.getElementById('check-btn').addEventListener('click', async function() {

    try {
        const total_price = +document.getElementById("total_price").value;

        const order_no = document.getElementById("order_no").value;

        const url = `http://127.0.0.1:8000/create-payment-session?amount=${total_price}&currency=USD&order_no=${order_no}`;
        const response = await fetch(url, {
            method: 'POST'
        });
        

        const result = await response.json();

        if (result.success === true){
            stripe.redirectToCheckout({ sessionId: result.data.session_id.id });
        }
        else{
        const payment_error_alert = document.createElement("div");
        const error_alert_text = document.createElement("strong");
        const error_btn = document.createElement("button");  
        payment_error_alert.id = "__alert"
        payment_error_alert.className = "alert alert-danger alert-dismissible fade show";
        error_alert_text.textContent = "We could'nt process you payment reqeust check your network connection";
        error_btn.id = "__alertbtn";
        error_btn.type = "button";
        error_btn.className = "btn-close";
        error_btn.onclick = ()=>{payment_error_alert.remove()}
        payment_error_alert.appendChild(error_alert_text)
        payment_error_alert.appendChild(error_btn)
        const __contain = document.getElementById("__contain");
        const ___checkout = document.getElementById("___checkout");
        __contain.insertBefore(payment_error_alert, ___checkout)
                

        }


        
    }
    
    catch (error) {
        console.error(error);
        const payment_error_alert = document.createElement("div");
        const error_alert_text = document.createElement("strong");
        const error_btn = document.createElement("button");  
        payment_error_alert.id = "__alert"
        payment_error_alert.className = "alert alert-danger alert-dismissible fade show";
        error_alert_text.textContent = "We could'nt process you payment reqeust check your network connection";
        error_btn.id = "__alertbtn";
        error_btn.type = "button";
        error_btn.className = "btn-close";
        error_btn.onclick = ()=>{payment_error_alert.remove()}
        payment_error_alert.appendChild(error_alert_text)
        payment_error_alert.appendChild(error_btn)
        const __contain = document.getElementById("__contain");
        const ___checkout = document.getElementById("___checkout");
        __contain.insertBefore(payment_error_alert, ___checkout)
                
    }
});


