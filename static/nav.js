const si = document.getElementById("si")
const w = document.getElementById("w")
const h = document.getElementById("h")
const m = document.getElementById("m")
const s = document.getElementById("s")
const b = document.getElementById("b")

if (si != null) {
    si.addEventListener("click", () => {
        location.href="/sign-in"
    })    
}

h.addEventListener("click", () => {
    location.href = "/"
})

m.addEventListener("click", () => {
    location.href="/market"
})

s.addEventListener("click", () => {
    location.href="/sell"
})

b.addEventListener("click", () => {
    location.href="/cart"
})