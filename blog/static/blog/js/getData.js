async function renderKarya(){
    const karya = await getDataKarya()
    updateUI(karya)
}
renderKarya()
// filter karya
const btnFilter = document.querySelectorAll(".kategori")
btnFilter.forEach( btn => {
    btn.addEventListener("click", async function(){
        try {
            // ubah style ke filter yang aktif
            btnFilter.forEach( btn => btn.classList.remove("filter-active") )
            this.classList.add("filter-active")
    
            const karya = await getDataKarya()
            const strKategori = this.innerText.toLowerCase()
            filterKarya(karya, strKategori)
        }
        catch(error){
            displayError(error)
        }
    })
})

function getDataKarya(){
    return fetch('./asset/resource/karya.json')
            .then(response => {
                if( !response.ok ){
                    throw new Error("Upss sepertinya web kami bermasalah, mohon tunggu")
                }
                return response.json()
            })
            .then(response => response.karya)
}

function updateUI(dataKarya){
    let cards = ""
    dataKarya.forEach(karya => cards += cardComponent(karya))
    const containerCard = document.querySelector('.container-karya')
    containerCard.innerHTML = cards
}

function filterKarya(dataKarya, filterText){
    
    const filtered = dataKarya.filter(data => data.category.toLowerCase() == filterText)
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
        <img src="/asset/img/404.svg" class="mt-5" alt="error ${error}" width="100%">
        <h1 class="text-center">${error}</h1>
    </div>`
}

document.addEventListener('click', async e => {
    if(e.target.classList.contains('btn-detail')){
        const indexKarya = e.target.dataset.idcard;
        let karya = await getDataKarya();
        karya = karya[e.target.dataset.idcard - 1];

        const modalBody = document.querySelector('.modal-detail');
        modalBody.innerHTML = modalComp(karya);
    }
})

// === COMPONENT === //
function cardComponent({title, creator, category, image, id}){
    return `<div class="col-lg-4 col-md-6 my-4 card-karya-wrapper">
    <div class=" border rounded-xl px-3 py-4 ">
        <div class="img-cover">
            <div class="img-karya">
                <img src="${image}" class="rounded-xl " alt="">
            </div>
        </div>
        <div class=" card-content">
            <h3 class="fs-5 fw-bold mt-4">${title}</h3>
            <p class="paragraf fs-6 mb-2">${category}</p>

            <div class="d-flex justify-content-between my-3">
                <p class="fw-bold">By. ${creator}</p>
                <div>
                    <a href="https://instagram.com"><img src="asset/img/icon/ig.svg" class="sosmed-icon mx-1" alt=""></a>
                </div>
            </div>
            <button data-bs-toggle="modal" data-bs-target="#detailModal" data-idcard="${id}" class="btn btn-red btn-detail">Lihat Selengkapnya</button>
        </div>
    </div>
</div>`
}

function modalComp({title, creator, category, image}){
    return `<div class="col-lg-7 col-md-10">
        <img src="${image}" class="img-fluid rounded-xl" alt="">
    </div>

    <div class="col-lg-5 col-md-10 mt-4 mt-lg-0">
        <h1>${title}</h1>
        <span class="text-muted">${category}</span>
        <div class="d-flex  my-4">
            <p class="fw-bold me-4">${creator}</p>
            <a href="https://instagram.com"><img src="asset/img/icon/ig.svg" class="sosmed-icon mx-1" alt=""></a>
            
        </div>
        
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto amet nam at neque adipisci dicta sed sit laboriosam, quaerat incidunt maxime ea possimus enim explicabo? Amet alias soluta, provident nihil asperiores impedit dicta officia, voluptatibus distinctio eum delectus aperiam, deserunt minus quasi dolor voluptate autem maxime officiis nisi repellendus quos voluptas earum at beatae! Cupiditate quasi cum ratione pariatur excepturi tempore animi, ea vel in, dolore rerum fugiat iste? Assumenda, ratione inventore! Fuga, alias a nobis sapiente sint.</p>
    </div>`
}