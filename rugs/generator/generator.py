import numpy as np
import pygltflib
from pygltflib import GLTF2, BufferFormat
from pygltflib.utils import ImageFormat, Image
from pygltflib.validator import validate, summary


class Rug:
	def __init__(self, id: str, width_cm: float, height_cm: float):
		self.id = id
		self.points = np.array(
		    [
		        [-width_cm / 2, 0, +height_cm / 2],
		        [-width_cm / 2, 0, -height_cm / 2],
		        [+width_cm / 2, 0, -height_cm / 2],
		        [+width_cm / 2, 0, +height_cm / 2]
		    ],
		    dtype="float32",
		)
		self.triangles = np.array(
		    [
		        [0, 1, 2],
		        [2, 3, 0]
		    ],
		    dtype="uint8",
		)

rug = Rug('abc', 200, 140)
triangles_binary_blob = rug.triangles.flatten().tobytes()
points_binary_blob = rug.points.tobytes()
image = Image()
image.uri = "../models/rug.png"
gltf = pygltflib.GLTF2(
    scene=0,
    scenes=[pygltflib.Scene(nodes=[0])],
    nodes=[pygltflib.Node(mesh=0)],
    meshes=[
        pygltflib.Mesh(
            primitives=[
                pygltflib.Primitive(
                    attributes=pygltflib.Attributes(POSITION=1), indices=0
                )
            ]
        )
    ],
    accessors=[
        pygltflib.Accessor(
            bufferView=0,
            componentType=pygltflib.UNSIGNED_BYTE,
            count=rug.triangles.size,
            type=pygltflib.SCALAR,
            max=[int(rug.triangles.max())],
            min=[int(rug.triangles.min())],
        ),
        pygltflib.Accessor(
            bufferView=1,
            componentType=pygltflib.FLOAT,
            count=len(rug.points),
            type=pygltflib.VEC3,
            max=rug.points.max(axis=0).tolist(),
            min=rug.points.min(axis=0).tolist(),
        ),
    ],
    bufferViews=[
        pygltflib.BufferView(
            buffer=0,
            byteLength=len(triangles_binary_blob),
            target=pygltflib.ELEMENT_ARRAY_BUFFER,
        ),
        pygltflib.BufferView(
            buffer=0,
            byteOffset=len(triangles_binary_blob),
            byteLength=len(points_binary_blob),
            target=pygltflib.ARRAY_BUFFER,
        ),
    ],
    buffers=[
        pygltflib.Buffer(
            byteLength=len(triangles_binary_blob) + len(points_binary_blob)
        )
    ],
    images=[image]
)

gltf.convert_images(ImageFormat.DATAURI)
gltf.set_binary_blob(triangles_binary_blob + points_binary_blob)
gltf.convert_buffers(BufferFormat.DATAURI)  # convert buffer URIs to data.

summary(gltf)  # will pretty print human readable summary of errors


#glb = b"".join(gltf.save_to_bytes())  # save_to_bytes returns an array of the components of a glb

#gltf_reloaded = pygltflib.GLTF2.load_from_bytes(glb)

gltf.save("simple.gltf")