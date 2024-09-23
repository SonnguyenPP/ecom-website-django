console.log("ajax-add-review");

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


$(document).ready(function() {

    $(".loader").hide();

    $(".filter-checkbox").on("click", function() {

        let filter_value = $(this).val();
        let filter_key = $(this).data("filter");
        // console.log(filter_value, filter_key);
        // filter_object[filter_key] = Array.from(document.querySelectorAll("input[data-filter='" + filter_key + "']:checked"))
        //     .map(function(element) {
        //         return element.value;
        //     });
        console.log("filer value:",filter_value)
        console.log("filer ley:",filter_key)
    });
});
