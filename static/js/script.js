window.addEventListener("scroll", function () {
  const header = document.querySelector("header");
  if (window.scrollY > 50) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
});

// Navbar Section
const bar = document.querySelector(".bar");
const navMobile = document.querySelector(".nav-mobile");

// Toggle and close navigation menu
document.addEventListener("click", (event) => {
  if (bar.contains(event.target)) {
    navMobile.classList.toggle("show");
  } else if (!navMobile.contains(event.target)) {
    navMobile.classList.remove("show");
  }
});
