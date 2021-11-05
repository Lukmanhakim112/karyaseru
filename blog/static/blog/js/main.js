// change navbar color on scroll
const navbar = document.querySelector(".navbar")
document.addEventListener('scroll', ()=> {
    if( pageYOffset > 80 ){
        navbar.classList.add("scroll")
    }else {
        navbar.classList.remove("scroll")
    }
})
// change navbar color when toggler on click
const navToggler = document.querySelector(".navbar-toggler");
navToggler.addEventListener('click', ()=> {
    navbar.classList.add("scroll")
    navToggler.classList.toggle("active")
})

const navLinks = document.querySelectorAll('.nav-link')
const section = navLinks.forEach((target)=> {
    target.addEventListener('click', function(){
        return this.getAttribute("href");
    })
})

// AOS Initialization
AOS.init({
    offset: 120,
    mirror: true,
    duration: 1000,
    easing: 'ease-in-out-back'
});

// Smooth scroll initialization
var scroll = new SmoothScroll('a[href*="#"]', {
    speed: 800,
    easing: 'easeInOutCubic',
    offset: function(){
        if(section == "#home"){
            return 0
        }else {
            return 120
        }
    }
});

// Glide init
new Glide('.glide', {
    type: 'carousel',
    autoplay: 3000,
}).mount()




