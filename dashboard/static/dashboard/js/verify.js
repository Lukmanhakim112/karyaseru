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
                    let verify = $(`#verify-${idPost}`); 
                    let verifyButton = $(`#button-verify-${idPost}`); 

			if (verify.val() == "True") {
                    		badge.removeClass('badge-gradient-success');
				badge.addClass('badge-gradient-dark');
				badge.text("TIDAK TERVERIFIKASI");
				verifyButton.text("Verifikasi")

				verify.val("False")
			} else {
                    		badge.removeClass('badge-gradient-dark');
				badge.addClass('badge-gradient-success');
				badge.text("TERVERIFIKASI");
				verifyButton.text("Batal Verifikasi")

				verify.val("True")
			}



                },
                error: (response) => {
                    alert(`Error, tidak bisa menemukan post: ${response}`)
                },
            });
            return false;
        });

    }

});
