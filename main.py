import json
import os
import subprocess
from copy import copy

from jinja2 import Template

ANALYZERS_DIR = os.path.join(os.path.dirname(__file__), 'analyzers')
TEMPLATE = Template('''<!DOCTYPE html>
<div>ANALYZER ... {{duration}}</div>
<div id="video-container">
  <!-- Video -->
  <video id="video" width="640" height="365">
    <source src="{{path}}" type="video/{{type}}">
    <p>
      Your browser doesn't support HTML5 video.
    </p>
  </video>
  <!-- Video Controls -->
  <div id="video-controls">
    <input type="range" id="seek-bar" value="0" style="display: block;width: 100%;">
    <button type="button" id="play-pause">Play</button>
    <button type="button" id="mute">Mute</button>
    <input type="range" id="volume-bar" min="0" max="1" step="0.1" value="1">
    <button type="button" id="full-screen">Full-Screen</button>
  </div>
</div>
<script>
// Video
var video = document.getElementById("video");

// Buttons
var playButton = document.getElementById("play-pause");
var muteButton = document.getElementById("mute");
var fullScreenButton = document.getElementById("full-screen");

// Sliders
var seekBar = document.getElementById("seek-bar");
var volumeBar = document.getElementById("volume-bar");

playButton.addEventListener("click", function() {
  if (video.paused == true) {
    // Play the video
    video.play();

    // Update the button text to 'Pause'
    playButton.innerHTML = "Pause";
  } else {
    // Pause the video
    video.pause();

    // Update the button text to 'Play'
    playButton.innerHTML = "Play";
  }
});

// Event listener for the mute button
muteButton.addEventListener("click", function() {
  if (video.muted == false) {
    // Mute the video
    video.muted = true;

    // Update the button text
    muteButton.innerHTML = "Unmute";
  } else {
    // Unmute the video
    video.muted = false;

    // Update the button text
    muteButton.innerHTML = "Mute";
  }
});

// Event listener for the seek bar
seekBar.addEventListener("change", function() {
  // Calculate the new time
  var time = video.duration * (seekBar.value / 100);

  // Update the video time
  video.currentTime = time;
});

// Update the seek bar as the video plays
video.addEventListener("timeupdate", function() {
  // Calculate the slider value
  var value = (100 / video.duration) * video.currentTime;

  // Update the slider value
  seekBar.value = value;
});

// Pause the video when the slider handle is being dragged
seekBar.addEventListener("mousedown", function() {
  video.pause();
});

// Play the video when the slider handle is dropped
seekBar.addEventListener("mouseup", function() {
  video.play();
});

// Event listener for the volume bar
volumeBar.addEventListener("change", function() {
  // Update the video volume
  video.volume = volumeBar.value;
});

</script>
''')


class Analyzer:
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return os.path.basename(self.path)

    def run(self, in_video, in_mata):
        r = subprocess.run(['python3', self.path, in_video, in_mata],
                           stdout=subprocess.PIPE)
        points = []
        for point in r.stdout.decode('utf-8').strip().split('\n'):
            x, f_x = point.split()
            x, f_x = float(x), float(f_x)
            points.append((x, f_x))
        return points

    def __repr__(self):
        return "Analyzer({!r})".format(self.path)


class AnalyzerManager:
    def __init__(self, analyzers):
        self.analyzers = analyzers

    def run(self, in_video, in_mata):
        context = {}
        for analyzer in self.analyzers:
            context[analyzer.name] = analyzer.run(in_video, in_mata)
        return context

    def __repr__(self):
        analyzers = ', '.join(map(repr, self.analyzers))
        return "AnalyzerManager([{}])".format(analyzers)


class ContextRender:
    def __init__(self, context, analyzers_results):
        self.context = context
        self.analyzers_results = analyzers_results

    def render(self):
        context = copy(self.context)
        return TEMPLATE.render(**context)


def load_analyzers():
    listdir = os.listdir(ANALYZERS_DIR)
    analyzers = [Analyzer(os.path.join(ANALYZERS_DIR, x)) for x in listdir]
    return AnalyzerManager(analyzers)


def generate_meta_data(in_video):
    # generate json meta file in tmp
    m = os.path.join(os.path.dirname(__file__), 'm.json')
    with open(m, 'r', encoding='utf-8') as f:
        meta = json.loads(f.read())
    meta['path'] = 'm.webm'
    return m, meta


def write_result(out, content):
    with open(out, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Video analysis tool.')
    parser.add_argument('video', help='input video')
    parser.add_argument('--out', '-o', default='index.html',
                        help='output html result')

    args = parser.parse_args()
    in_video = args.video
    out = args.out

    in_mata, mata = generate_meta_data(in_video)
    analyzers = load_analyzers()
    analyzers_result_context = analyzers.run(in_video, in_mata)
    r = ContextRender(mata, analyzers_result_context)
    result = r.render()

    write_result(out, result)


if __name__ == '__main__':
    main()
