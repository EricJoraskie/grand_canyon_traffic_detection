from skimage import io
from keras.models import load_model
from tensorflow import image as tfi
from numpy import expand_dims, argmax
from flask import Flask, render_template

app = Flask(__name__)


def load_traffic_model():
    '''Loads the model as a global variable'''
    global model
    model = load_model('checkpoint/88/best_traffic.h5')


def get_answer(pred):
    '''Converts the model output to the prediction string and color'''
    if pred == 4:
        return 'YES, very', 'red'
    elif pred == 3:
        return 'Yes', 'orangered'
    elif pred == 2:
        return 'kinda', 'yellow'
    elif pred == 1:
        return 'Nope', 'greenyellow'
    elif pred == 0:
        return 'Straight ghost town', 'green'


@app.route('/')
def home():
    '''Gets the image, resizes, and predicts, then displays output'''
    im_path = 'https://www.nps.gov/webcams-grca/camera0.jpg'
    im = io.imread(im_path)
    model_im = tfi.resize(im, size=(96, 128))
    model_im = expand_dims(model_im, axis=0)
    pred = argmax(model.predict(model_im))
    answer, color = get_answer(pred)
    return render_template('home.html', answer=answer, color=color, im=im_path)


if __name__ == "__main__":
    load_traffic_model()
    # Run app
    app.run(host="0.0.0.0", port=5000)
