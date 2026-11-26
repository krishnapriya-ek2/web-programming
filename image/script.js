
let images = [
    "https://picsum.photos/id/10/800/500",
    "https://picsum.photos/id/20/800/500",
    "https://picsum.photos/id/30/800/500",
    "https://picsum.photos/id/40/800/500",
    "https://picsum.photos/id/50/800/500",
    "https://picsum.photos/id/60/800/500",
    "https://picsum.photos/id/70/800/500",
    "https://picsum.photos/id/80/800/500"
];

let index = 0;
let timer = null;

let gallery = document.getElementById("gallery");

// Display images in grid
images.forEach((src, i) => {
    let img = document.createElement("img");
    img.src = src;
    img.onclick = () => openGallery(i);
    gallery.appendChild(img);
});

function openGallery(i) {
    index = i;
    document.getElementById("modal").style.display = "flex";
    showImage();
}

function closeGallery() {
    document.getElementById("modal").style.display = "none";
    clearInterval(timer);
    timer = null;
    document.getElementById("playBtn").innerText =
        "▶ Play Slideshow";
}

function showImage() {
    document.getElementById("bigImage").src = images[index];

    document.getElementById("counter").innerText =
        (index + 1) + " / " + images.length;
}

function changeImage(step) {
    index = (index + step + images.length) % images.length;
    showImage();
}

function togglePlay() {
    if (timer) {
        clearInterval(timer);
        timer = null;
        document.getElementById("playBtn").innerText =
            "▶ Play Slideshow";
    } else {
        timer = setInterval(() => changeImage(1), 2000);
        document.getElementById("playBtn").innerText =
            "⏸ Pause Slideshow";
    }
}

