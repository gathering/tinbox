var current = 0;
var current_slide = 0;

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
            slideContainer = document.getElementById("slide-b").innerHTML = "";
        } else {
            slideContainer = document.getElementById("slide-b").innerHTML = data;
            document.getElementById("slide-b").style.display = "block";
            document.getElementById("slide-a").style.display = "none";
            current = 1;
            slideContainer = document.getElementById("slide-a").innerHTML = "";
        }
    });
}

function timeout(s) {
    return new Promise(resolve => setTimeout(resolve, (s * 1000)));
}

var first = True

async function run(screen_id) {
    fetch_screen(screen_id).then(async (data) => {
        for(let i = 0; i < data['slides'].length; i++) {
            // Render slide
            if (current_slide != data['slides'][i]['id'] && Number(data['slides'][i]['duration']) !== 0 || first) {
                first = False
                render_slide(data['slides'][i]['id']);
            } else {
                console.log("Infinite slide, not changing slide.")
            }
            console.log("Playing slide " + data['slides'][i]['id'] + "(" + data['slides'][i]['title'] + ") for " + data['slides'][i]['duration'] + " seconds.");

            current_slide = data['slides'][i]['id'];

            // Trigger timeout for the duration of the slide.
            if (Number(data['slides'][i]['duration']) === 0) {
                await timeout(60);
            } else {
                await timeout(data['slides'][i]['duration']);
            }
            
        }
        if (data['slides'].length == 0) {
            await timeout(1);
            document.getElementById("slide-b").style.display = "none";
            document.getElementById("slide-a").style.display = "none";
        }
        run(screen_id);
    });
}
