# bakin-blender-exporter
![image](https://github.com/user-attachments/assets/23f51664-bfe6-49ba-a63d-a09acf8ba78d)

**A Blender Addon that allows you to quickly export (in a single-click) FBX models and their material definitions (.def files) for RPG Developer BAKIN, letting you easily import your models into Bakin without having to manually import every texture for every model!**

Version 2.0 is a major update that aims to make the Bakin Model Exporter handle a LOT more features than before, including a new UI, and more utility, hopefully making model importing much more reliable in RPG Developer Bakin.

> [!TIP]
> If you wish to import a VRM model from VRoid Studio in RPG Developer Bakin, use this Blender add-on instead: https://github.com/Meringue-Rouge/bakin-vrm-blender

### Features
- Makes your model import into RPG Developer Bakin without (hopefully) having to manually assign textures / properties!
  - Exports your model, textures, and a material definition file (.def) in a single folder.
- **_Triangulation Check & Fix:_** Detects if there are any meshes that are not triangulated, and will add a Triangulate modifier to the meshes. If the model looks untextured and broken in Bakin while popping error messages, press this button and export again.
- **_(BETA) Generate Missing Textures from Albedo:_** Each material has an indicator for each texture field that Bakin can use. If you press one of the texture fields that is in red, the addon will ask you if it should generate and assign that texture for the selected material. (Results might not be correct, hence beta for now)
- **_Bakin Material Properties:_** Several (but not all) of the properties that can be edited in Bakin, such as shader type, outline settings, receiving decals, and more, can be edited straight from the addon, per material, and Bakin will immediately apply the correct settings upon importing.
- **Generates Mask Maps** according to BAKIN's specifications from the model's Shader Node textures: Roughness, Metallic, Emissive and Specular.
- Language support for English, Japanese (AI-translated) and Simplified Chinese (AI-translated).

> [!CAUTION]
> Due to the nature of 3D Models and especially Materials, the add-on won't guarantee your model will import in RPG Developer Bakin without issues. Always check your shader nodes in Blender (especially if you're downloading models off the internet), textures, filenames, and try again.

### Usage
- Install the blender add-on by going to Edit -> Preferences, going to Add-ons, and selecting in the top-right the Install from Disk option (hidden in a small square on 4.2+)
  - On older versions of Blender, make sure to tick the box to enable the add-on.
- You'll find the Add-on on the right menu, which can be opened by pressing N, or clicking on the little arrow.
- Make sure your model uses Principled BSDF shader nodes (PBR), and save the blend file project.
- Make sure your texture nodes in the shader nodes connect to the standard inputs.
- Define a model name in the addon. This will define the folder name, model filename, and def filename, and will be saved in the folder where your blend file is.
- Press "Export FBX+DEF".
- Import the model into RPG Developer BAKIN.

### Credits
- Models shown are from Blenderkit (https://www.blenderkit.com/)
- Code was (mostly) generated through ChatGPT (with a lot of troubleshooting and fixing), and Grok for version 2.
