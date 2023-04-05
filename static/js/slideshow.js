var current = 0;

async function fetch_screen(id) {
    const response = await fetch("/api/get/screen/" + id);
    return response.json();
}

async function fetch_slide(id) {
    const response = await fetch("/view/slide/" + id);
    return response.text();
}

async function render_slide(id) {
    // A little hack to avoid flashing when changing slide..
    fetch_slide(id).then((data) => {
        if (current == 1) {
            slideContainer = document.getElementById("slide-a").innerHTML = data;
            document.getElementById("slide-a").style.display = "block";
            document.getElementById("slide-b").style.display = "none";
            current = 0;
        } else {
            slideContainer = document.getElementById("slide-b").innerHTML = data;
            document.getElementById("slide-b").style.display = "block";
            document.getElementById("slide-a").style.display = "none";
            current = 1;
        }
    });
}

function timeout(s) {
    return new Promise(resolve => setTimeout(resolve, (s * 1000)));
}

async function run(screen_id) {
    fetch_screen(screen_id).then(async (data) => {
        for(let i = 0; i < data['slides'].length; i++) {
            // Render slide
            render_slide(data['slides'][i]['id']);
            console.log("Playing slide " + data['slides'][i]['id'] + "(" + data['slides'][i]['title'] + ") for " + data['slides'][i]['duration'] + " seconds.");

            // Trigger timeout for the duration of the slide.
            await timeout(data['slides'][i]['duration']);
        }
        run(screen_id);
    });

    // add support for 4k screens
    const width = window.innerWidth;
    document.body.style.zoom = width / 1920;
}
