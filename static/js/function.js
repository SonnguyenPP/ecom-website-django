console.log("ajax-add-review");

$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log("comment")
        }
    })
  
})


$("#add-to-cart-btn").on("click",function(){
    let quantity = $("#product-quantity").val()
    let product_title = $(".product-title").val()
    let product_id = $(".product-id").val()
    let product_price = $(".current-product-price").text()
    let this_val = $(this)


    console.log("Quantily:", quantity)
    console.log("Title:", product_title)
    console.log("Price:", product_price)
    console.log("ID:", product_id)
    console.log("Current Element:", this_val)

    $.ajax({
        url: '/add-to-cart',
        data:{
            'id' : product_id,
            'qty': quantity,
            'title':product_title,
            'price':product_price,
        },
        dataType:'json',
        beforeSend: function(){
            console.log("adding product to cart");

        },
        success: function(response){
            this_val.html("item added to cart")
            console.log("added product to cart");
            $(".cart-items-count").text(response.totalcartitems)
            this_val.attr('disable',false)
        }
    })

}) 