document.getElementById("start-camera").addEventListener("click", function () {
    let videoFeed = document.getElementById("video-feed");
    let stopButton = document.getElementById("stop-camera");

    videoFeed.src = "/video_feed"; 
    videoFeed.style.display = "block"; 
    this.style.display = "none"; 
    stopButton.style.display = "inline-block"; 
});

// Stop Camera
document.getElementById("stop-camera").addEventListener("click", function () {
    let videoFeed = document.getElementById("video-feed");
    let startButton = document.getElementById("start-camera");

    videoFeed.src = "";  // Stop streaming
    videoFeed.style.display = "none";  
    this.style.display = "none";  
    startButton.style.display = "inline-block";  
});

document.getElementById("upload-form").addEventListener("submit", function (event) {
    event.preventDefault();
    let formData = new FormData();
    let imageFile = document.getElementById("image-input").files[0];

    if (!imageFile) {
        alert("Please select an image first!");
        return;
    }

    formData.append("file", imageFile);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        let resultDiv = document.getElementById("prediction-result");
        let imageUrl = `/uploads/${data.image}`; // ✅ Correct image URL
        resultDiv.innerHTML = `
            <h3>Predicted Image:</h3>
            <img src="${imageUrl}" style="max-width: 100%;">
            <h3>Detected Objects:</h3>
            <p>${data.result}</p>
        `;
    })
    .catch(error => console.error("Error:", error));
});
