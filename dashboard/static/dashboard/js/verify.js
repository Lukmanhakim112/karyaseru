$(document).ready(() => {

    let formsVerify = $(".verify-post")

    for (let i = 0; i < formsVerify.length; i++) {

        $(formsVerify[i]).on("submit", function() {
            $.ajax({
                url: `/d/post/verify/`,
                type: "POST",
                data: $(formsVerify[i]).serialize(),
                dataType: 'json',
                success: (response) => {
                    let idPost = this.getAttribute("id").split("-")[2];
                    let badge = $(`#badge-${idPost}`); 

                    badge.removeClass('badge-gradient-dark');
                    badge.addClass('badge-gradient-success');
                    badge.text("TERVERIFIKASI");
                },
                error: (response) => {
                    alert("Error, tidak bisa menemukan post.")
                },
            });
            return false;
        });

    }

});
