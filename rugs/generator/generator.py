import numpy as np
import pygltflib
from pygltflib import GLTF2, BufferFormat
from pygltflib.utils import ImageFormat, Image, Texture
from pygltflib.validator import validate, summary


class Rug:
	"""Rug data."""
	def __init__(self, id: str, length_m: float, width_m: float):
		self.id = id
		self.points = np.array(
		    [
		        [+width_m / 2, 0, +length_m / 2],
		        [+width_m / 2, 0, -length_m / 2],
		        [-width_m / 2, 0, -length_m / 2],
		        [-width_m / 2, 0, +length_m / 2],
		    ],
		    dtype="float32",
		)
		self.points_blob = self.points.tobytes()
		self.texture_coords = np.array(
			[
				[1, 1],
				[1, 0],
				[0, 0],
				[0, 1],
			],
		    dtype="float32",
		)
		self.texture_coords_blob = self.texture_coords.flatten().tobytes()
		self.triangles = np.array(
		    [
		        [0, 1, 2],
		        [2, 3, 0],
		    ],
		    dtype="uint8",
		)
		self.triangles_blob = self.triangles.flatten().tobytes()

rug = Rug('abc', 2.00, 1.40)
gltf = pygltflib.GLTF2(
    scene=0,
    scenes=[pygltflib.Scene(nodes=[0])],
    nodes=[pygltflib.Node(mesh=0)],
    meshes=[
        pygltflib.Mesh(
            primitives=[
                pygltflib.Primitive(
                    attributes=pygltflib.Attributes(
                    	POSITION=0,
                    	TEXCOORD_0=1),
                    indices=2,
                    material=0
                )
            ]
        )
    ],
    accessors=[
        # Points of the rug rectangle.
        pygltflib.Accessor(
            bufferView=0,
            componentType=pygltflib.FLOAT,
            count=len(rug.points),
            type=pygltflib.VEC3,
            max=rug.points.max(axis=0).tolist(),
            min=rug.points.min(axis=0).tolist(),
        ),
        # Texture coordinates
        pygltflib.Accessor(
            bufferView=1,
            componentType=pygltflib.FLOAT,
            count=len(rug.texture_coords),
            type=pygltflib.VEC2,
            max=rug.texture_coords.max(axis=0).tolist(),
            min=rug.texture_coords.min(axis=0).tolist(),
        ),
        # Triangle indices. We keep these at the end because unsigned bytes may not result in a length multiple of 4 bytes.
        pygltflib.Accessor(
            bufferView=2,
            componentType=pygltflib.UNSIGNED_BYTE,
            count=rug.triangles.size,
            type=pygltflib.SCALAR,
            max=[int(rug.triangles.max())],
            min=[int(rug.triangles.min())],
        ),
    ],
    bufferViews=[
        # Points of the rug rectangle.
        pygltflib.BufferView(
            buffer=0,
            byteOffset=0,
            byteLength=len(rug.points_blob),
            target=pygltflib.ARRAY_BUFFER,
        ),
        # Texture coordinates
        pygltflib.BufferView(
            buffer=0,
            byteOffset=len(rug.points_blob),
            byteLength=len(rug.texture_coords_blob),
            target=pygltflib.ARRAY_BUFFER,
        ),
        # Triangle indices. We keep these at the end because unsigned bytes may not result in a length multiple of 4 bytes.
        pygltflib.BufferView(
            buffer=0,
            byteOffset=len(rug.points_blob) + len(rug.texture_coords_blob),
            byteLength=len(rug.triangles_blob),
            target=pygltflib.ELEMENT_ARRAY_BUFFER,
        ),
    ],
    buffers=[
        pygltflib.Buffer(
            byteLength=len(rug.points_blob) + len(rug.texture_coords_blob) + len(rug.triangles_blob)
        )
    ],
    images=[pygltflib.Image(uri="../models/rug.png")],
    textures=[pygltflib.Texture(source=0)],
    materials=[pygltflib.Material(
        pbrMetallicRoughness=pygltflib.PbrMetallicRoughness(
            metallicFactor=0,
        	roughnessFactor=0.9,
        	baseColorTexture=pygltflib.TextureInfo(index=0),
      	),
      	doubleSided=True,
    )]
)

gltf.convert_images(ImageFormat.DATAURI)
gltf.set_binary_blob(rug.points_blob + rug.texture_coords_blob + rug.triangles_blob)
gltf.convert_buffers(BufferFormat.DATAURI)  # convert buffer URIs to data.

summary(gltf)  # will pretty print human readable summary of errors


#glb = b"".join(gltf.save_to_bytes())  # save_to_bytes returns an array of the components of a glb

#gltf_reloaded = pygltflib.GLTF2.load_from_bytes(glb)

gltf.save("../models/simple.gltf")