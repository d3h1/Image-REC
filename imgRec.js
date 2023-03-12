// Define the class names that the model can recognize
const IMAGENET_CLASSES = [
    "bikini, two-piece",
    "bathrobe",
    "coat",
    "fur coat",
    "jeans, blue jeans, denim",
    "miniskirt, mini",
    "sweater, jumper",
    "trench coat",
    "ball gown, evening gown, gown",
    "jersey, T-shirt, tee shirt",
    // ... and so on
];


// Load the pre-trained model
const modelPromise = tf.loadGraphModel('https://tfhub.dev/google/tfjs-model/imagenet/mobilenet_v2_100_224/classification/4/default/1');

// Preview the selected image and predict its label
async function previewImage(event) {
    const input = event.target;
    const preview = document.getElementById('preview');
    const reader = new FileReader();
    reader.onload = async function() {
        const dataURL = reader.result;
        preview.src = dataURL;
        const model = await modelPromise;
        const img = tf.browser.fromPixels(preview).resizeNearestNeighbor([224, 224]).toFloat().expandDims();
        const predictions = await model.predict(img);
        const topPredictions = Array.from(predictions.dataSync()).map((p, i) => {
            return {
                probability: p,
                className: IMAGENET_CLASSES[i]
            };
        }).sort((a, b) => b.probability - a.probability).slice(0, 5);
        const predictionElement = document.getElementById('prediction');
        predictionElement.innerText = `Prediction: ${topPredictions[0].className}`;
    };
    reader.readAsDataURL(input.files[0]);
}
