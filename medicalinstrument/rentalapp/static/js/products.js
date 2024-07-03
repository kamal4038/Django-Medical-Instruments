


document.addEventListener("DOMContentLoaded",function(event){
    const btnPlus=document.getElementById("btnPlus");
    const btnMinus=document.getElementById("btnMinus");
    const txtQty=document.getElementById("txtQty");
    const pid=document.getElementById("pid");
    const tkn=document.querySelector('[name="csrfmiddlewaretoken"]')
    const btnCart=document.getElementById("btnCart")
   
   
    
      btnPlus.addEventListener("click",function(){
      let Qty=parseInt(txtQty.value,10);

      Qty=isNaN(Qty)?0:Qty;
      
      if (Qty<10){
        Qty++;
        txtQty.value=Qty;
      }
    });
      btnMinus.addEventListener("click",function(){
      let Qty=parseInt(txtQty.value,10);

      Qty=isNaN(Qty)?0:Qty;
      
      if (Qty>0){
        Qty--;
        txtQty.value=Qty;
      }
      
    });
    
    btnCart.addEventListener("click",function(){
        let Qty=parseInt(txtQty.value,10);
        Qty=isNaN(Qty)?0:Qty;

        if(Qty>0){
            let postObj = {
                product_qty:Qty,
                pid:pid.value,
                token:tkn
            }
            console.log(postObj);
            fetch("/addtocart",{
                method:'POST',
                credentials:'same-origin',
            headers:{
                'Accept':'Application/json',
                'X-Requested-with':'XMLHttpRequest',
                'X-CSRFToken':'{{ csrf_token }}',
            },
            body:JSON.stringify(postObj),
        }).then(response => {
            return response.json();
        }).then(data=>{
            console.log(data);
        })
        }
        else{
            aleryt("Please Enter The Quantity");
          }
    });

  });
