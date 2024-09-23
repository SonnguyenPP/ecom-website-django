
$("#commentForm").submit(function(e){

    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("comment saved to DB");

            if(res.bool == true){
                $("#review-res").html("Review added successfullty")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30"></div>'
                            _html +='<div class="user justify-content-between d-flex">'
                            _html +='<div class="thumb text-center">'
                            _html +='<img src="{% static assets/imgs/blog/author-2.png %}" alt="" />'
                            _html +='<a href="#" class="font-heading text-brand">'+ res.context.user +'</a>'
                            _html +='</div>'
                            _html +='<div class="desc">'
                            _html +='<div class="d-flex justify-content-between mb-10">'
                            _html +='<div class="d-flex align-items-center">'
                            _html +='<span class="font-xs text-muted">{{r.date|date:"d M, Y"}} </span>'
                            _html +='</div>'
                           for(let i = 1; i < res.context.rating;i++){
                            _html += '<i class="fas fa-star text-warning">'
                           }
                            _html += '</div>'
                            _html +='<p class="mb-10">'+ res.context.review +'</p>'
                            _html +='</div>'
                            _html +='</div>'
                            _html +='</div>'

            }
            $(".comment-list").prepend(_html)
        }
    })
  
})


// $("#add-to-cart-btn").on("click",function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $(".current-product-price").text()
//     let this_val = $(this)


//     console.log("Quantily:", quantity)
//     console.log("Title:", product_title)
//     console.log("Price:", product_price)
//     console.log("ID:", product_id)
//     console.log("Current Element:", this_val)

//     $.ajax({
//         url: '/add-to-cart',
//         data:{
//             'id' : product_id,
//             'qty': quantity,
//             'title':product_title,
//             'price':product_price,
//         },
//         dataType:'json',
//         beforeSend: function(){
//             console.log("adding product to cart");

//         },
//         success: function(response){
//             this_val.html("item added to cart")
//             console.log("added product to cart");
//             $(".cart-items-count").text(response.totalcartitems)
//             this_val.attr('disable',false)
//         }
//     })

// }) 
$(".add-to-cart-btn").on("click",function(){
    let this_val = $(this)
    let index = this_val.attr("data-index")
    let quantity = $(".product-quantity-"+ index).val()
    let product_title = $(".product-title-"+ index).val()
    let product_id = $(".product-id-"+ index).val()
    let product_price = $(".current-product-price-"+index).text()

    let product_pid = $(".product-pid-"+index).val()
    let product_image = $(".product-image-"+index).val()

    


    console.log("Quantily:", quantity)
    console.log("Title:", product_title)
    console.log("Price:", product_price)
    console.log("ID:", product_id)
    console.log("PID:", product_pid)
    console.log("Image:", product_image)
    console.log("index:", index)
    console.log("Current Element:", this_val)

    $.ajax({
        url: '/add-to-cart',
        data:{
            'id' : product_id,
            'pid' : product_pid,
            'image' : product_image,


            'qty': quantity,
            'title':product_title,
            'price':product_price,
        },
        dataType:'json',
        beforeSend: function(){
            console.log("adding product to cart");

        },
        success: function(response){
            this_val.html("ok")
            console.log("added product to cart");
            $(".cart-items-count").text(response.totalcartitems)
            this_val.attr('disable',false)
        }
    })

}) 



$(document).ready(function() {

    $(".loader").hide();

    $(".filter-checkbox , #price-filter-btn").on("click", function() {

        let filter_object = {};

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;


        $(".filter-checkbox").each(function(index) {

            let filter_value = $(this).val();
            let filter_key = $(this).data("filter");


            console.log(filter_value, filter_key);
            filter_object[filter_key] = Array.from(document.querySelectorAll("input[data-filter='" + filter_key + "']:checked"))
                .map(function(element) {
                    return element.value;
                });

        });
        console.log(filter_object);
        $.ajax({
            url : '/filter-products',
            data: filter_object,
            dataType:'json',
            beforeSend:function(){
                console.log("try data");
            },
            success: function(response){
                console.log(response);
                console.log("data filter success");
                $("#filtered-product").html(response.data)

            }
        
        })
        
    })

 
    $("#max_price").on("blur", function() {
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();
        console.log("Current Price is:", current_price);
        console.log("Max Price is:", max_price);
        console.log("Min Price is:", min_price);


        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
           


            minPrice = Math.round(min_price * 100) / 100;
            maxPrice = Math.round(max_price * 100) / 100;
            //  console.log("-----------");
             
            //  console.log("Max Price is:", max_price);
             
            //  console.log("Min Price is:", min_price);

            alert("Price must be between " + min_price + ' and ' + max_price);
            $(this).val(min_price);
            $('#range').val(min_price);
            $(this).focus();
            return false;


        }
        
    });


    $(".delete-product").on("click", function() {

        let product_id = $(this).attr("data-product");
        let this_val = $(this);

        console.log(product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: 'json',
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                // console.log(response);
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems);
                
                $("#cart-list").html(response.data);
            }
        });
    });

    $(".update-product").on("click", function() {

        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $(".product-qty-"+product_id).val()

        console.log(product_id);
        console.log(product_quantity);


        
        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: 'json',
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                // console.log(response);
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems);
                
                $("#cart-list").html(response.data);
            }
        });
    });


    $(document).on("click", ".make-default-address", function() {
        let id = $(this).attr("data-address-id");
        let this_val = $(this);
        console.log("ID is:", id);
        console.log("Element is:", this_val);
        $.ajax({
            url: "/make-default-address",
            data: {
                "id": id
            },
            dataType: "json",
            success: function(response) {
                console.log("Address Made Default .... ");
                if (response.boolean == true) {
                    
                    $(".check").hide();
                    $(".action_btn").show();


                    $(".check" + id).show();
                    $(".button" + id).hide();
                }
                
            }
        });
    });

    $(document).on("click", ".add-to-wishlist", function() {
        let product_id = $(this).attr("data-product-item");
        let this_val = $(this);
        console.log("Product ID:", product_id);
        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function() {
                console.log("added to wishlist");
            },
            success: function(response) {
                this_val.html("ok");
                if (response === true){
                     console.log("added tto wishlist");
                }
               
            }
        });
    });
    $(document).on("click", ".delete-wishlist-product", function() {
        let wishlist_id = $(this).attr("data-wishlist-product");
        let this_val = $(this);
    
        console.log("wishlist id is:", wishlist_id);
    
        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function() {
                console.log("Deleting product from wishlist...");
            },
            success: function(response) {
                this_val.html("ok");
                $("#wishlist-list").html(response.data);
            }
        });
    });

    $(document).on("submit", "#contact-form-ajax", function(e){
        e.preventDefault();
        console.log("Submitted ... ");
        let full_name = $("#full_name").val();
        let email = $("#email").val();
        let phone = $("#phone").val();
        let subject = $("#subject").val();
        let message = $("#message").val();
        console.log("Name:", full_name);
        console.log("Email:", email);
        console.log("Phone:", phone);
        console.log("Subject:", subject);
        console.log("Message:", message);
        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Sending Data to Server ... ");
            },
            success: function(res){
                console.log("Sent Data to server!");
                $("#contact-form-ajax").hide()
                $("#message-response").html("Sent Success")
                $(".contact_us_p").hide()
            }
        });
    });
    
    // Remove from wishlist


    
    
    
});




