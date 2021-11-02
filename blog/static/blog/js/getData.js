// filter karya
const btnFilter = document.querySelectorAll(".kategori")
btnFilter.forEach( btn => {
    btn.addEventListener("click", async function(){
        try {
            // ubah style ke filter yang aktif
            btnFilter.forEach( btn => btn.classList.remove("filter-active") )
            this.classList.add("filter-active")
    
            const karya = await getDataKarya(btn.getAttribute('data-filter'))
            const strKategori = this.innerText.toLowerCase()
            filterKarya(karya, strKategori)
        }
        catch(error){
            displayError(error)
        }
    })
})

function getDataKarya(category){
    return fetch(`${window.location.origin}/post-category/${category}`)
            .then(response => {
                if( !response.ok ){
                    throw new Error("Upss sepertinya web kami bermasalah, mohon tunggu")
                }
                return response.json()
            })
            .then(response => response.post)
}

function updateUI(dataKarya){
    let cards = ""
    dataKarya.forEach(karya => cards += cardComponent(karya))
    const containerCard = document.querySelector('.container-karya')
    containerCard.innerHTML = cards
}

function filterKarya(dataKarya, filterText){
    
    const filtered = dataKarya.filter(data => data.category__category.toLowerCase() == filterText)
    if( filterText == "semua" ){
        updateUI(dataKarya)
        return
    }
    else if( filtered.length == 0 ){
        throw "404 not found"
    }
    updateUI(filtered)
}

function displayError(error){
    const containerCard = document.querySelector('.container-karya')
    containerCard.innerHTML = `<div class="col-md-6 mx-auto error-img">
        <img src="${window.location.origin}/static/blog/img/404.svg" class="mt-5" alt="error ${error}" width="100%">
        <h1 class="text-center">${error}</h1>
    </div>`
}

// === COMPONENT === //
function cardComponent({title, author, category__category, image, ig_account, slug}){
    return `<div class="col-lg-4 col-md-6 my-4 card-karya-wrapper">
    <div class=" border rounded-xl px-3 py-4 ">
        <div class="img-cover">
            <div class="img-karya">
                <img src="${window.location.origin}/media/${image}" class="rounded-xl " alt="">
            </div>
        </div>
        <div class=" card-content">
            <h3 class="fs-5 fw-bold mt-4">${title}</h3>
            <p class="paragraf fs-6 mb-2">${category__category}</p>

            <div class="d-flex justify-content-between my-3">
                <p class="fw-bold">By. ${author}</p>
                <div>
                    <a href="${ig_account}"><img src="${window.location.origin}/static/blog/img/icon/ig.svg" class="sosmed-icon mx-1" alt=""></a>
                </div>
            </div>
            <a href="/post/p/${slug}/" class="btn btn-red btn-detail">Lihat Selengkapnya</a>
        </div>
    </div>
</div>`
}
