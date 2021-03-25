import argparse
from os import listdir
from os.path import join

_PREAMBLE = """
<script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

<script>
function updateAr() {
    document.getElementById("ar_element").src = "models/" + document.getElementById("dropDown").value + ".gltf";
    document.getElementById("ar_element").iosSrc = "models/" + document.getElementById("dropDown").value + ".usdz";
}
</script>

<div align="center">
	Rug:
    <select id="dropDown" onChange="updateAr()">
"""

_POSTAMBLE = """
    </select>
</div>


<model-viewer
    id="ar_element"
    src="models/{}.gltf"
    ios-src="models/{}.usdz"
    camera-controls
    shadow-intensity="1"
    ar-modes="scene-viewer webxr quick-look"
    ar
    ar-scale="auto"
    style="width:100%; height:100%">
</model-viewer>
"""

def main():
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--input_models', metavar='path', required=True,
                        help='Path to models directory')
    parser.add_argument('--output_html', metavar='path', required=True,
                        help='Path to the output HTML file')
    args = parser.parse_args()

    model_ids = [f.removesuffix('.gltf') for f in listdir(args.input_models) if join(args.input_models, f).endswith('.gltf')]
    if len(model_ids) < 1:
    	print("ERROR: could not find any GLTF files in {}".format(args.input_models))
    	return

    select_lines = ["""<option value="{}">{}</option><br />\n""".format(f, f) for f in model_ids]

    with open(args.output_html, "w") as file1:
        # Writing data to a file
        file1.write(_PREAMBLE)
        file1.writelines(select_lines)
        file1.write(_POSTAMBLE.format(model_ids[0], model_ids[0]))

    print("Wrote {} models to {}".format(len(model_ids), args.output_html))

if __name__ == "__main__":
    main()
