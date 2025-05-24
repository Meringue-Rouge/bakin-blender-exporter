bl_info = {
    "name": "Bakin Model Exporter",
    "author": "Meringue Rouge",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Bakin Model Exporter Tab",
    "description": (
        "BAKIN EN/JP: Exports Model files for RPG Developer Bakin. Scan textures detected, assign Bakin specific material flags, and generate Mask Maps and other maps from the Albedo file."
    ),
    "category": "3D View",
}

import bpy
import os
import unicodedata
import re

from bpy.types import Operator, Panel

# Define text for all languages
TEXT = {
    'en': {
        'model_name': "Model Name",
        'save_warning': "Please save the blend file to export!",
        'export_button': "Export FBX + DEF",
        'material_config': "Material Config",
        'scan_materials': "Scan Materials",
        'no_principled_bsdf': "No Principled BSDF shader found",
        'shader_label': "Export Shader",
        'emissive_blink': "Emissive Blink",
        'emissive_blink_speed': "Emissive Blink Speed",
        'emissive_link_building_light': "Emissive Link Building Light",
        'cast_shadow': "Cast Shadow",
        'receive_decal': "Receive Decal",
        'uscrollanim': "U Scroll Animation",
        'vscrollanim': "V Scroll Animation",
        'scrollanimspeed': "Scroll Animation Speed (U, V)",
        'draw_outline': "Draw Outline",
        'outline_width': "Outline Width",
        'outline_color': "Outline Color",
        'cull_mode': "Cull Mode",
        'cull_back': "Back Face Culling",
        'cull_front': "Front Face Culling",
        'cull_none': "Double Sided",
        'cull_double': "Invisible",
        'use_mask_map': "Use Mask Map",
        'invert_roughness': "Inv Rough",
        'invert_metallic': "Inv Met",
        'invert_emissive': "Inv Emis",
        'invert_specular': "Inv Spec",
        'sss_coeff': "SSS Coeff",
        'texture_base': "Base",
        'texture_norm': "Norm",
        'texture_met': "Met",
        'texture_rough': "Rough",
        'texture_emis': "Emis",
        'texture_spec': "Spec",
        'texture_sss': "SSS",
        'settings_toggle': "Settings",
        'discard_threshold': "Discard Threshold",
        'generate_texture': "Generate {texture_type} Texture",
        'generate_texture_prompt': "Generate a {texture_type} texture for material '{material_name}'?",
        'no_albedo_error': "Cannot generate texture: Albedo (Base Color) texture is missing!",
        'texture_save_error': "Failed to save texture: {error}",
        'invalid_input_error': "Cannot link texture: Input '{input_key}' not found on Principled BSDF node. Available inputs: {available_inputs}",
        'triangulation_warning': "Model is not fully triangulated! Bakin requires triangulated meshes.",
        'triangulate_button': "Triangulate Meshes"
    },
    'jp': {
        'model_name': "モデル名",
        'save_warning': "エクスポートするにはブレンドファイルを保存してください!",
        'export_button': "FBX + DEF エクスポート",
        'material_config': "マテリアル設定",
        'scan_materials': "マテリアルをスキャン",
        'no_principled_bsdf': "Principled BSDF シェーダーが見つかりません",
        'shader_label': "エクスポートシェーダー",
        'emissive_blink': "エミッシブ点滅",
        'emissive_blink_speed': "エミッシブ点滅速度",
        'emissive_link_building_light': "エミッシブリンクビルディングライト",
        'cast_shadow': "影を落とす",
        'receive_decal': "デカールを受け取る",
        'uscrollanim': "Uスクロールアニメーション",
        'vscrollanim': "Vスクロールアニメーション",
        'scrollanimspeed': "スクロールアニメーション速度 (U, V)",
        'draw_outline': "アウトラインを描く",
        'outline_width': "アウトライン幅",
        'outline_color': "アウトラインカラー",
        'cull_mode': "カリングモード",
        'cull_back': "裏面カリング",
        'cull_front': "表面カリング",
        'cull_none': "両面",
        'cull_double': "不可視",
        'use_mask_map': "マスクマップを使用",
        'invert_roughness': "ラフネス反転",
        'invert_metallic': "メタリック反転",
        'invert_emissive': "エミッシブ反転",
        'invert_specular': "スペキュラー反転",
        'sss_coeff': "SSS係数",
        'texture_base': "ベース",
        'texture_norm': "ノーマル",
        'texture_met': "メタリック",
        'texture_rough': "ラフネス",
        'texture_emis': "エミッシブ",
        'texture_spec': "スペキュラー",
        'texture_sss': "SSS",
        'settings_toggle': "設定",
        'discard_threshold': "ディスカード閾値",
        'generate_texture': "{texture_type} テクスチャを生成",
        'generate_texture_prompt': "マテリアル '{material_name}' の {texture_type} テクスチャを生成しますか？",
        'no_albedo_error': "テクスチャを生成できません：アルベド（ベースカラー）テクスチャがありません！",
        'texture_save_error': "テクスチャの保存に失敗しました：{error}",
        'invalid_input_error': "テクスチャをリンクできません：Principled BSDF ノードに '{input_key}' 入力が見つかりません。利用可能な入力：{available_inputs}",
        'triangulation_warning': "モデルが完全に三角形化されていません！Bakinでは三角形化されたメッシュが必要です。",
        'triangulate_button': "メッシュを三角形化"
    },
    'zh': {
        'model_name': "模型名称",
        'save_warning': "请保存blend文件以进行导出！",
        'export_button': "导出 FBX + DEF",
        'material_config': "材质配置",
        'scan_materials': "扫描材质",
        'no_principled_bsdf': "未找到 Principled BSDF 着色器",
        'shader_label': "导出着色器",
        'emissive_blink': "自发光闪烁",
        'emissive_blink_speed': "自发光闪烁速度",
        'emissive_link_building_light': "自发光链接建筑光",
        'cast_shadow': "投射阴影",
        'receive_decal': "接收贴花",
        'uscrollanim': "U滚动动画",
        'vscrollanim': "V滚动动画",
        'scrollanimspeed': "滚动动画速度 (U, V)",
        'draw_outline': "绘制轮廓",
        'outline_width': "轮廓宽度",
        'outline_color': "轮廓颜色",
        'cull_mode': "剔除模式",
        'cull_back': "背面剔除",
        'cull_front': "正面剔除",
        'cull_none': "双面",
        'cull_double': "不可见",
        'use_mask_map': "使用蒙版贴图",
        'invert_roughness': "反转粗糙",
        'invert_metallic': "反转金属",
        'invert_emissive': "反转自发光",
        'invert_specular': "反转高光",
        'sss_coeff': "SSS系数",
        'texture_base': "基础",
        'texture_norm': "法线",
        'texture_met': "金属",
        'texture_rough': "粗糙",
        'texture_emis': "自发光",
        'texture_spec': "高光",
        'texture_sss': "SSS",
        'settings_toggle': "设置",
        'discard_threshold': "丢弃阈值",
        'generate_texture': "生成{texture_type}贴图",
        'generate_texture_prompt': "为材质 '{material_name}' 生成{texture_type}贴图？",
        'no_albedo_error': "无法生成贴图：缺少反照率（基础颜色）贴图！",
        'texture_save_error': "保存贴图失败：{error}",
        'invalid_input_error': "无法链接贴图：Principled BSDF 节点上未找到输入 '{input_key}'。可用输入：{available_inputs}",
        'triangulation_warning': "模型未完全三角化！Bakin需要三角化的网格。",
        'triangulate_button': "三角化网格"
    }
}

texture_dict = {
    'Base Color': "AMap",
    'Normal': "NMap",
    'LitMap': "LitMap",
    'ShadeMap': "ShadeMap",
    'NormalMap': "NormalMap",
    'EmiMap': "EmiMap",
    'MCMap': "MCMap",
    'outlineWeight': "outlineWeight",
    'Subsurface': "SSSMap"
}

# Shader options for the dropdown
SHADER_OPTIONS = [
    ('a_n_rm 542d323fb6604f468eb8fd99b29502d8', "A_N_RM", "Default shader"),
    ('a_n_rm_discard 0d973c7e0eaf4bf2b1b8470c15571799', "A_N_RM_DISCARD", "Discard shader"),
    ('a_n_rm_sss_discard 5d7bee168e844ad0bcdca0ea7ff09996', "A_N_RM_SSS_DISCARD", "SSS Discard shader"),
    ('a_n 09ed65ad49b4492da5d217339562c62f', "A_N", "A_N shader"),
    ('a_n_discard 75433c209c1c46fa847e6f03c59e02cb', "A_N_DISCARD", "A_N Discard shader")
]

# Cull mode options for the dropdown
CULL_MODE_OPTIONS = [
    ('back', "Back Face Culling", "Cull back faces"),
    ('front', "Front Face Culling", "Cull front faces"),
    ('none', "Double Sided", "No culling, double-sided rendering"),
    ('double', "Invisible", "Invisible rendering")
]

def check_model_triangulation(context):
    """Check if all mesh objects in the scene are fully triangulated."""
    for obj in context.scene.objects:
        if obj.type == 'MESH' and obj.data.polygons:
            # Evaluate the mesh with modifiers applied
            depsgraph = context.evaluated_depsgraph_get()
            eval_obj = obj.evaluated_get(depsgraph)
            mesh = eval_obj.data
            # Check if any polygon is not a triangle (has != 3 vertices)
            for poly in mesh.polygons:
                if len(poly.vertices) != 3:
                    return False
    return True

class TriangulateMeshesOperator(Operator):
    bl_idname = "object.triangulate_meshes"
    bl_label = "Triangulate Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Iterate through all mesh objects
        for obj in context.scene.objects:
            if obj.type == 'MESH' and obj.data.polygons:
                # Check if a Triangulate Modifier already exists
                has_triangulate = any(mod.type == 'TRIANGULATE' for mod in obj.modifiers)
                if not has_triangulate:
                    # Add Triangulate Modifier with specific settings
                    mod = obj.modifiers.new(name="Triangulate", type='TRIANGULATE')
                    mod.keep_custom_normals = True
                    mod.quad_method = 'BEAUTY'

        # Update triangulation status
        context.scene.is_model_triangulated = check_model_triangulation(context)
        self.report({'INFO'}, "Triangulate Modifiers added to all meshes.")
        return {'FINISHED'}

class ExportFBXOperator(Operator):
    bl_idname = "object.export_fbx_def"
    bl_label = "Export FBX + DEF"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check if the blend file is saved
        if bpy.data.filepath == "":
            self.report({'WARNING'}, TEXT[context.scene.language]['save_warning'])
            return {'CANCELLED'}

        try:
            model_name = context.scene.model_name
            dirpath = bpy.path.abspath("//" + sanitize_filename(model_name))
            os.makedirs(dirpath, exist_ok=True)
            
            for image in bpy.data.images:
                if image.has_data and image.type == 'IMAGE':
                    new_image_name = sanitize_filename(image.name.replace(' ', '_'))
                    image.save_render(os.path.join(dirpath, new_image_name + ".png"))

            filepath = os.path.join(dirpath, model_name + ".fbx")
            bpy.ops.export_scene.fbx(
                filepath=filepath,
                use_selection=False,
                global_scale=0.01,
                use_tspace=True
            )

            def_filepath = os.path.join(dirpath, model_name + ".def")
            with open(def_filepath, 'w') as f:
                for obj in bpy.context.scene.objects:
                    if obj.type == 'MESH' and obj.data.materials:
                        for material in obj.data.materials:
                            if material:
                                material.name = sanitize_material_name(material.name)
                                # Find the corresponding DetectedMaterialItem
                                material_item = None
                                for item in context.scene.detected_materials:
                                    if item.material_name == material.name:
                                        material_item = item
                                        break
                                mask_map_path = None
                                sss_map_path = None
                                if material_item and material_item.use_mask_map:
                                    mask_map_path = generate_unity_mask_map(material, dirpath, material_item)
                                if material_item and material_item.shader_type == 'a_n_rm_sss_discard 5d7bee168e844ad0bcdca0ea7ff09996':
                                    sss_map_path = generate_sss_map(material, dirpath, material_item)
                                if mask_map_path or sss_map_path:
                                    filename = sanitize_filename(os.path.basename(mask_map_path)) if mask_map_path else None
                                    sss_filename = sanitize_filename(os.path.basename(sss_map_path)) if sss_map_path else None
                                    print(f"Generated mask map: {filename}" if mask_map_path else "")
                                    print(f"Generated SSS map: {sss_filename}" if sss_map_path else "")
                                    write_def_file(material, f, filename, sss_filename, material_item)
                                else:
                                    write_def_file(material, f, None, None, material_item)

        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

def find_texture_node(node, checked_nodes=None):
    """Recursively finds the first linked texture node, avoiding loops."""
    if checked_nodes is None:
        checked_nodes = set()
    
    if node in checked_nodes:
        return None  # Avoid infinite loops
    
    checked_nodes.add(node)

    if node and node.type == 'TEX_IMAGE':
        return node
    
    for input in node.inputs:
        if input.is_linked:
            for link in input.links:
                tex_node = find_texture_node(link.from_node, checked_nodes)
                if tex_node:
                    return tex_node
    return None

def create_dummy_image(name, width, height):
    dummy_image = bpy.data.images.new(name, width=width, height=height)
    dummy_image.generated_color = (0.0, 0.0, 0.0, 1.0)
    return dummy_image

def generate_unity_mask_map(material, output_path, material_item):
    if not material.use_nodes:
        print(f"Material '{material.name}' does not use nodes.")
        return None

    node_tree = material.node_tree
    nodes = node_tree.nodes

    # Find the Principled BSDF node
    principled_bsdf = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled_bsdf = node
            break

    if not principled_bsdf:
        print(f"No Principled BSDF shader found in material '{material.name}'.")
        return None

    # Function to safely get the image from a node
    def get_image_from_node(input_socket):
        if input_socket and input_socket.is_linked:
            link = input_socket.links[0]
            if link.from_node and link.from_node.type == 'TEX_IMAGE':
                return link.from_node.image
        return None

    # Get connected textures
    metallic_tex_image = get_image_from_node(principled_bsdf.inputs.get('Metallic', None))
    roughness_tex_image = get_image_from_node(principled_bsdf.inputs.get('Roughness', None))
    emissive_tex_image = get_image_from_node(principled_bsdf.inputs.get('Emission Color', None))
    specular_tex_image = get_image_from_node(principled_bsdf.inputs.get('Specular', None))
    
    if specular_tex_image is None:
        specular_tex_image = get_image_from_node(principled_bsdf.inputs.get('Specular IOR Level', None))

    # Check if any textures exist for the mask map
    if not any([metallic_tex_image, roughness_tex_image, emissive_tex_image, specular_tex_image]):
        print(f"No relevant textures found for mask map in material '{material.name}'.")
        return None

    # Default size if no textures are found (though we already checked)
    width, height = 1024, 1024
    if metallic_tex_image:
        width, height = metallic_tex_image.size
    elif roughness_tex_image:
        width, height = roughness_tex_image.size
    elif emissive_tex_image:
        width, height = emissive_tex_image.size
    elif specular_tex_image:
        width, height = specular_tex_image.size

    # Set up compositing
    comp_scene = bpy.context.scene
    comp_scene.use_nodes = True

    comp_tree = comp_scene.node_tree
    comp_nodes = comp_tree.nodes
    comp_links = comp_tree.links

    # Clear existing nodes
    for node in comp_nodes:
        comp_nodes.remove(node)

    # Add Image nodes
    metallic_node = comp_nodes.new(type='CompositorNodeImage')
    metallic_node.image = metallic_tex_image

    roughness_node = comp_nodes.new(type='CompositorNodeImage')
    roughness_node.image = roughness_tex_image

    emissive_node = comp_nodes.new(type='CompositorNodeImage')
    emissive_node.image = emissive_tex_image
    
    # Add Invert nodes
    invert_node_e = comp_nodes.new(type='CompositorNodeInvert')
    invert_node_m = comp_nodes.new(type='CompositorNodeInvert')
    invert_node_r = comp_nodes.new(type='CompositorNodeInvert')
    invert_node_s = comp_nodes.new(type='CompositorNodeInvert')

    specular_node = comp_nodes.new(type='CompositorNodeImage')
    specular_node.image = specular_tex_image

    # Add Combine RGBA node
    combine_node = comp_nodes.new(type='CompositorNodeCombRGBA')

    # Add Output File node
    output_filename = f"{sanitize_filename(bpy.context.scene.model_name)}_MaskMap"
    output_node = comp_nodes.new(type='CompositorNodeOutputFile')
    output_node.base_path = output_path
    output_node.file_slots[0].path = output_filename

    # Use material-specific invert settings
    if roughness_tex_image and material_item.invert_roughness:
        comp_links.new(roughness_node.outputs['Image'], invert_node_r.inputs['Color'])
        comp_links.new(invert_node_r.outputs['Color'], combine_node.inputs['G'])
    elif roughness_tex_image:
        comp_links.new(roughness_node.outputs['Image'], combine_node.inputs['G'])

    if metallic_tex_image and material_item.invert_metallic:
        comp_links.new(metallic_node.outputs['Image'], invert_node_m.inputs['Color'])
        comp_links.new(invert_node_m.outputs['Color'], combine_node.inputs['B'])
    elif metallic_tex_image:
        comp_links.new(metallic_node.outputs['Image'], combine_node.inputs['B'])

    if emissive_tex_image and material_item.invert_emissive:
        comp_links.new(emissive_node.outputs['Image'], invert_node_e.inputs['Color'])
        comp_links.new(invert_node_e.outputs['Color'], combine_node.inputs['R'])
    elif emissive_tex_image:
        comp_links.new(emissive_node.outputs['Image'], combine_node.inputs['R'])

    if specular_tex_image and material_item.invert_specular:
        comp_links.new(specular_node.outputs['Image'], invert_node_s.inputs['Color'])
        comp_links.new(invert_node_s.outputs['Color'], combine_node.inputs['A'])
    elif specular_tex_image:
        comp_links.new(specular_node.outputs['Image'], combine_node.inputs['A'])
    
    comp_links.new(combine_node.outputs['Image'], output_node.inputs['Image'])

    # Render the scene to create the image
    output_file_path = os.path.join(output_path, f"{output_filename}.png")
    bpy.context.scene.render.filepath = output_file_path
    bpy.ops.render.render(write_still=True)

    return output_filename

def generate_sss_map(material, output_path, material_item):
    if not material.use_nodes:
        print(f"Material '{material.name}' does not use nodes.")
        return None

    node_tree = material.node_tree
    nodes = node_tree.nodes

    # Find the Principled BSDF node
    principled_bsdf = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled_bsdf = node
            break

    if not principled_bsdf:
        print(f"No Principled BSDF shader found in material '{material.name}'.")
        return None

    # Function to safely get the image from a node
    def get_image_from_node(input_socket):
        if input_socket and input_socket.is_linked:
            link = input_socket.links[0]
            if link.from_node and link.from_node.type == 'TEX_IMAGE':
                return link.from_node.image
        return None

    # Get connected Base Color texture
    base_color_tex_image = get_image_from_node(principled_bsdf.inputs.get('Base Color', None))

    # If no Base Color texture, create a dummy image
    if not base_color_tex_image:
        width, height = 1024, 1024
        base_color_tex_image = create_dummy_image(f"{material.name}_SSS_dummy", width, height)

    # Set up compositing
    comp_scene = bpy.context.scene
    comp_scene.use_nodes = True

    comp_tree = comp_scene.node_tree
    comp_nodes = comp_tree.nodes
    comp_links = comp_tree.links

    # Clear existing nodes
    for node in comp_nodes:
        comp_nodes.remove(node)

    # Add Image node
    base_color_node = comp_nodes.new(type='CompositorNodeImage')
    base_color_node.image = base_color_tex_image

    # Add RGB to BW node to convert to grayscale
    rgb_to_bw_node = comp_nodes.new(type='CompositorNodeRGBToBW')

    # Add Output File node
    output_filename = f"{sanitize_filename(bpy.context.scene.model_name)}_SSSMap"
    output_node = comp_nodes.new(type='CompositorNodeOutputFile')
    output_node.base_path = output_path
    output_node.file_slots[0].path = output_filename

    # Connect nodes: Base Color -> RGB to BW -> Output
    comp_links.new(base_color_node.outputs['Image'], rgb_to_bw_node.inputs['Image'])
    comp_links.new(rgb_to_bw_node.outputs['Val'], output_node.inputs['Image'])

    # Render the scene to create the grayscale image
    output_file_path = os.path.join(output_path, f"{output_filename}0001.png")
    bpy.context.scene.render.filepath = output_file_path
    bpy.ops.render.render(write_still=True)

    return output_filename

def generate_texture(material, texture_type, output_path, context):
    """Generate a texture of the specified type based on the Albedo texture."""
    if not material.use_nodes or not material.node_tree:
        return None, "Material does not use nodes."

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Find Principled BSDF node
    principled_bsdf = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
    if not principled_bsdf:
        return None, "No Principled BSDF shader found."

    # Get Albedo (Base Color) texture
    base_color_input = principled_bsdf.inputs.get('Base Color')
    if not base_color_input or not base_color_input.is_linked:
        return None, TEXT[context.scene.language]['no_albedo_error']
    
    base_color_node = find_texture_node(base_color_input.links[0].from_node)
    if not base_color_node or not base_color_node.image:
        return None, TEXT[context.scene.language]['no_albedo_error']
    
    base_color_image = base_color_node.image
    width, height = base_color_image.size

    # Set up compositing
    comp_scene = context.scene
    comp_scene.use_nodes = True
    comp_tree = comp_scene.node_tree
    comp_nodes = comp_tree.nodes
    comp_links = comp_tree.links

    # Clear existing nodes
    for node in comp_nodes:
        comp_nodes.remove(node)

    # Add base image node
    base_node = comp_nodes.new(type='CompositorNodeImage')
    base_node.image = base_color_image

    # Output node
    output_filename = f"{sanitize_filename(material.name)}_{texture_type}"
    output_node = comp_nodes.new(type='CompositorNodeOutputFile')
    output_node.base_path = output_path
    output_node.file_slots[0].path = output_filename

    # Generate texture based on type
    if texture_type == "Normal":
        # Generate a basic normal map (neutral blue)
        rgb_node = comp_nodes.new(type='CompositorNodeRGB')
        rgb_node.outputs[0].default_value = (0.5, 0.5, 1.0, 1.0)  # Neutral normal (blue)
        comp_links.new(rgb_node.outputs['RGBA'], output_node.inputs['Image'])
    elif texture_type in ["Metallic", "Roughness", "Specular", "Subsurface"]:
        # Convert Albedo to grayscale for Metallic, Roughness, Specular, Subsurface
        rgb_to_bw_node = comp_nodes.new(type='CompositorNodeRGBToBW')
        comp_links.new(base_node.outputs['Image'], rgb_to_bw_node.inputs['Image'])
        if texture_type == "Roughness":
            # Invert for Roughness (white = rough)
            invert_node = comp_nodes.new(type='CompositorNodeInvert')
            comp_links.new(rgb_to_bw_node.outputs['Val'], invert_node.inputs['Color'])
            comp_links.new(invert_node.outputs['Color'], output_node.inputs['Image'])
        else:
            # Metallic, Specular, Subsurface (white = high effect)
            comp_links.new(rgb_to_bw_node.outputs['Val'], output_node.inputs['Image'])
    elif texture_type == "Emission":
        # Darken Albedo for Emission (only bright areas glow)
        brightness_node = comp_nodes.new(type='CompositorNodeBrightContrast')
        brightness_node.inputs['Bright'].default_value = -0.5
        brightness_node.inputs['Contrast'].default_value = 1.0
        comp_links.new(base_node.outputs['Image'], brightness_node.inputs['Image'])
        comp_links.new(brightness_node.outputs['Image'], output_node.inputs['Image'])

    # Render the texture
    output_file_path = os.path.join(output_path, f"{output_filename}0001.png")
    comp_scene.render.filepath = output_file_path
    try:
        bpy.ops.render.render(write_still=True)
    except Exception as e:
        return None, TEXT[context.scene.language]['texture_save_error'].format(error=str(e))

    # Verify the file exists
    if not os.path.exists(output_file_path):
        return None, TEXT[context.scene.language]['texture_save_error'].format(error=f"File not found: {output_file_path}")

    # Load the generated texture
    try:
        new_image = bpy.data.images.load(output_file_path)
        new_image.name = f"{material.name}_{texture_type}.png"
    except Exception as e:
        return None, TEXT[context.scene.language]['texture_save_error'].format(error=str(e))

    # Create and link texture node
    tex_node = nodes.new(type='ShaderNodeTexImage')
    tex_node.image = new_image
    tex_node.location = (principled_bsdf.location.x - 200, principled_bsdf.location.y - 200)

    if texture_type == "Normal":
        normal_map_node = nodes.new(type='ShaderNodeNormalMap')
        normal_map_node.location = (principled_bsdf.location.x - 100, principled_bsdf.location.y - 200)
        links.new(tex_node.outputs['Color'], normal_map_node.inputs['Color'])
        links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
    else:
        input_key = "Emission Color" if texture_type == "Emission" else texture_type
        if texture_type == "Subsurface":
            # Try 'Subsurface' first, then 'Subsurface Weight' for compatibility
            input_key = "Subsurface" if principled_bsdf.inputs.get("Subsurface") else "Subsurface Weight"
        elif texture_type == "Specular" and not principled_bsdf.inputs.get('Specular'):
            # Use 'Specular IOR Level' for Specular textures in newer Blender versions
            input_key = "Specular IOR Level"
        
        # Verify the input exists
        if not principled_bsdf.inputs.get(input_key):
            available_inputs = ", ".join(principled_bsdf.inputs.keys())
            return None, TEXT[context.scene.language]['invalid_input_error'].format(
                input_key=input_key, available_inputs=available_inputs)
        
        links.new(tex_node.outputs['Color'], principled_bsdf.inputs[input_key])

    # Update detected materials flags for this material
    for item in context.scene.detected_materials:
        if item.material_name == material.name:
            if texture_type == "Base Color":
                item.base_color_detected = True
            elif texture_type == "Normal":
                item.normal_detected = True
            elif texture_type == "Metallic":
                item.metallic_detected = True
            elif texture_type == "Roughness":
                item.roughness_detected = True
            elif texture_type == "Emission":
                item.emission_detected = True
            elif texture_type == "Specular":
                item.specular_detected = True
            elif texture_type == "Subsurface":
                item.sss_detected = True
            break

    # Refresh material detection to ensure UI updates
    bpy.ops.object.detect_materials()

    return output_file_path, None

class GenerateTextureOperator(Operator):
    bl_idname = "wm.generate_texture"
    bl_label = "Generate Texture"
    bl_options = {'REGISTER', 'UNDO'}

    material_index: bpy.props.IntProperty()
    texture_type: bpy.props.StringProperty()
    material_name: bpy.props.StringProperty()

    def invoke(self, context, event):
        # Show confirmation dialog
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.label(text=TEXT[context.scene.language]['generate_texture_prompt'].format(
            texture_type=self.texture_type, material_name=self.material_name))

    def execute(self, context):
        material = bpy.data.materials.get(self.material_name)
        if not material:
            self.report({'ERROR'}, f"Material '{self.material_name}' not found.")
            return {'CANCELLED'}

        # Determine output path
        model_name = context.scene.model_name
        dirpath = bpy.path.abspath("//" + sanitize_filename(model_name))
        os.makedirs(dirpath, exist_ok=True)

        # Generate texture
        output_path, error = generate_texture(material, self.texture_type, dirpath, context)
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}

        self.report({'INFO'}, f"Generated {self.texture_type} texture for {self.material_name}")
        return {'FINISHED'}

class SimpleOperatorPanel(Panel):
    bl_label = "Bakin Model Exporter"
    bl_idname = "OBJECT_PT_my_simple_operator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bakin Model Exporter"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add language buttons
        row = layout.row()
        row.operator("wm.switch_language", text="English").language = 'en'
        row.operator("wm.switch_language", text="日本語").language = 'jp'
        row.operator("wm.switch_language", text="中文").language = 'zh'
        layout.separator()

        # Display the model name property
        layout.label(text=TEXT[scene.language]['model_name'], icon="LINE_DATA")
        layout.prop(scene, "model_name")
        layout.separator()

        # Triangulation check
        if not scene.is_model_triangulated:
            layout.label(text=TEXT[scene.language]['triangulation_warning'], icon='ERROR')
            layout.operator("object.triangulate_meshes", text=TEXT[scene.language]['triangulate_button'], icon='MESH_DATA')
            layout.separator()
        
        # Material Config Section
        layout.label(text=TEXT[scene.language]['material_config'], icon="MATERIAL")
        layout.operator("object.detect_materials", text=TEXT[scene.language]['scan_materials'], icon="VIEWZOOM")

        if len(scene.detected_materials) > 0:
            box = layout.box()
            box.label(text="Detected Materials:", icon="MATERIAL")
            for i, item in enumerate(scene.detected_materials):
                # Create a sub-box for each material with a subtle background
                material_box = box.box()
                # Material name
                material_box.label(text=f"Material: {item.material_name}", icon='MATERIAL')
                # Texture detection buttons
                row = material_box.row(align=True)
                # Colored buttons for texture status
                for tex, detected in [
                    ('base', item.base_color_detected),
                    ('norm', item.normal_detected),
                    ('met', item.metallic_detected),
                    ('rough', item.roughness_detected),
                    ('emis', item.emission_detected),
                    ('spec', item.specular_detected),
                    ('sss', item.sss_detected)
                ]:
                    sub_row = row.row(align=True)
                    sub_row.alert = not detected  # Red if not detected
                    sub_row.enabled = True  # Always enabled to allow generating missing textures
                    sub_row.scale_x = 1.2  # Wider for rectangular button
                    sub_row.scale_y = 1.5  # Taller for rectangular button
                    if detected:
                        sub_row.operator("wm.dummy_operator", text=TEXT[scene.language][f'texture_{tex}'])
                    else:
                        texture_type_map = {
                            'base': 'Base Color',
                            'norm': 'Normal',
                            'met': 'Metallic',
                            'rough': 'Roughness',
                            'emis': 'Emission',
                            'spec': 'Specular',
                            'sss': 'Subsurface'
                        }
                        op = sub_row.operator("wm.generate_texture", text=TEXT[scene.language][f'texture_{tex}'])
                        op.material_index = i
                        op.texture_type = texture_type_map[tex]
                        op.material_name = item.material_name
                # Settings toggle button
                row = material_box.row()
                row.operator(
                    "wm.toggle_settings",
                    text=TEXT[scene.language]['settings_toggle'],
                    icon='TRIA_DOWN' if item.show_settings else 'TRIA_RIGHT',
                    emboss=True
                ).material_index = i
                if item.show_settings:
                    sub_box = material_box.box()
                    if not item.has_principled_bsdf:
                        row = sub_box.row()
                        row.alert = True
                        row.label(text=TEXT[scene.language]['no_principled_bsdf'], icon="ERROR")
                    # Shader selection dropdown
                    row = sub_box.row()
                    row.label(text=TEXT[scene.language]['shader_label'])
                    row.prop(item, "shader_type", text="")
                    # Material parameter checkboxes
                    sub_box.prop(item, "emissiveBlink", text=TEXT[scene.language]['emissive_blink'])
                    if item.emissiveBlink:
                        sub_box.prop(item, "emissiveBlinkSpeed", text=TEXT[scene.language]['emissive_blink_speed'])
                    sub_box.prop(item, "emissiveLinkBuildingLight", text=TEXT[scene.language]['emissive_link_building_light'])
                    sub_box.prop(item, "castshadow", text=TEXT[scene.language]['cast_shadow'])
                    sub_box.prop(item, "receivedecal", text=TEXT[scene.language]['receive_decal'])
                    sub_box.prop(item, "uscrollanim", text=TEXT[scene.language]['uscrollanim'])
                    sub_box.prop(item, "vscrollanim", text=TEXT[scene.language]['vscrollanim'])
                    if item.uscrollanim or item.vscrollanim:
                        sub_box.prop(item, "scrollanimspeed", text=TEXT[scene.language]['scrollanimspeed'])
                    sub_box.prop(item, "drawOutline", text=TEXT[scene.language]['draw_outline'])
                    # Conditional outline settings
                    if item.drawOutline:
                        sub_box.prop(item, "outlineWidth", text=TEXT[scene.language]['outline_width'])
                        sub_box.prop(item, "outlineColor", text=TEXT[scene.language]['outline_color'])
                    # Cull mode dropdown
                    row = sub_box.row()
                    row.label(text=TEXT[scene.language]['cull_mode'])
                    row.prop(item, "cull_mode", text="")
                    # Separator before Mask Map settings
                    sub_box.separator()
                    # Mask Map settings
                    sub_box.prop(item, "use_mask_map", text=TEXT[scene.language]['use_mask_map'])
                    if item.use_mask_map:
                        # Create a row for invert options similar to texture status
                        row = sub_box.row(align=True)
                        for prop, text_key in [
                            ('invert_emissive', 'invert_emissive'),
                            ('invert_metallic', 'invert_metallic'),
                            ('invert_roughness', 'invert_roughness'),
                            ('invert_specular', 'invert_specular')
                        ]:
                            sub_row = row.row(align=True)
                            sub_row.scale_x = 1.2  # Match texture status button width
                            sub_row.scale_y = 1.5  # Match texture status button height
                            sub_row.prop(item, prop, text=TEXT[scene.language][text_key], toggle=True)
                    # SSS settings for A_N_RM_SSS_DISCARD shader
                    if item.shader_type == 'a_n_rm_sss_discard 5d7bee168e844ad0bcdca0ea7ff09996':
                        sub_box.prop(item, "sss_coeff", text=TEXT[scene.language]['sss_coeff'])
                    # Discard threshold setting
                    sub_box.prop(item, "discard_threshold", text=TEXT[scene.language]['discard_threshold'])
                    sub_box.separator()
                # Add separator between materials (except for the last one)
                if i < len(scene.detected_materials) - 1:
                    box.separator()

        # Check if the blend file is saved and Material Config has been run
        is_file_saved = bpy.data.filepath != ""
        is_material_config_run = scene.material_config_run

        # Add Export button
        if not is_file_saved or not is_material_config_run:
            # Show warnings and disable the button
            if not is_file_saved:
                layout.label(text=TEXT[scene.language]['save_warning'], icon='ERROR')
            if not is_material_config_run:
                layout.label(text="Please run Material Config first!", icon='ERROR')
            row = layout.row()
            row.enabled = False  # Disable the row
            row.operator("object.export_fbx_def", text=TEXT[scene.language]['export_button'], icon='EXPORT')
        else:
            # Enable the button if conditions are met
            layout.operator("object.export_fbx_def", text=TEXT[scene.language]['export_button'], icon='EXPORT')

class SwitchLanguageOperator(Operator):
    bl_idname = "wm.switch_language"
    bl_label = "Switch Language"
    bl_options = {'REGISTER', 'UNDO'}

    language: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.language = self.language
        return {'FINISHED'}

class DummyOperator(Operator):
    bl_idname = "wm.dummy_operator"
    bl_label = ""
    bl_options = {'INTERNAL'}

    def execute(self, context):
        return {'FINISHED'}

class ToggleSettingsOperator(Operator):
    bl_idname = "wm.toggle_settings"
    bl_label = "Toggle Settings"
    bl_options = {'REGISTER', 'UNDO'}

    material_index: bpy.props.IntProperty()

    def execute(self, context):
        item = context.scene.detected_materials[self.material_index]
        item.show_settings = not item.show_settings
        return {'FINISHED'}

def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

def sanitize_material_name(name):
    return re.sub(r'\W+', '_', unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII'))

def write_def_file(material, f, mask_map_filename, sss_map_filename, material_item):
    sanitized_material_name = sanitize_material_name(material.name)
    f.write(f"mtl {sanitized_material_name}\n")
    # Use the material's bakin_shader_type, default to A_N_RM if not set
    shader = getattr(material, 'bakin_shader_type', SHADER_OPTIONS[0][0])
    f.write(f"shader {shader}\n")
    
    # Initialize default values for roughness, metallic, and specular
    roughness_value = 1.000000
    metallic_value = 1.000000
    specular_value = 1.000000
    sss_value = 1.000000
    
    # Find the corresponding DetectedMaterialItem for this material
    material_item = material_item or None
    for item in bpy.context.scene.detected_materials:
        if item.material_name == material.name:
            material_item = item
            break
    
    # Check for Principled BSDF node to get values
    if material.use_nodes and material.node_tree:
        nodes = material.node_tree.nodes
        principled_bsdf = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
        if principled_bsdf:
            # Roughness
            roughness_input = principled_bsdf.inputs.get('Roughness')
            if roughness_input and not roughness_input.is_linked:
                roughness_value = float(roughness_input.default_value)
            # Metallic
            metallic_input = principled_bsdf.inputs.get('Metallic')
            if metallic_input and not metallic_input.is_linked:
                metallic_value = float(metallic_input.default_value)
            # Specular (try Specular first, then Specular IOR Level)
            specular_input = principled_bsdf.inputs.get('Specular')
            if not specular_input or specular_input.is_linked:
                specular_input = principled_bsdf.inputs.get('Specular IOR Level')
            if specular_input and not specular_input.is_linked:
                specular_value = float(specular_input.default_value)
            # Subsurface
            sss_input = principled_bsdf.inputs.get('Subsurface')
            if sss_input and not sss_input.is_linked:
                sss_value = float(sss_input.default_value)

    # Write all lines after shader, using retrieved values
    f.write(f"emissiveBlink {str(material_item.emissiveBlink).lower()}\n" if material_item else "emissiveBlink false\n")
    f.write(f"emissiveBlinkSpeed {float(material_item.emissiveBlinkSpeed):.6f}\n" if material_item else "emissiveBlinkSpeed 0.000000\n")
    f.write(f"emissiveLinkBuildingLight {str(material_item.emissiveLinkBuildingLight).lower()}\n" if material_item else "emissiveLinkBuildingLight false\n")
    f.write(f"uscrollanim {str(material_item.uscrollanim).lower()}\n" if material_item else "uscrollanim false\n")
    f.write(f"vscrollanim {str(material_item.vscrollanim).lower()}\n" if material_item else "vscrollanim false\n")
    scrollanimspeed = material_item.scrollanimspeed if material_item else [0.0, 0.0]
    f.write(f"scrollanimspeed {float(scrollanimspeed[0]):.6f} {float(scrollanimspeed[1]):.6f}\n")
    f.write("uvstepanim false\n")
    f.write("uvstepanimparam 1 1 0 1.000000\n")
    f.write("uvstepanim_modeluvorigin false\n")
    f.write("sortindex 0\n")
    f.write(f"castshadow {str(material_item.castshadow).lower()}\n" if material_item else "castshadow true\n")
    f.write(f"receivedecal {str(material_item.receivedecal).lower()}\n" if material_item else "receivedecal false\n")
    f.write(f"cull {material_item.cull_mode}\n" if material_item else "cull back\n")
    f.write(f"drawOutline {str(material_item.drawOutline).lower()}\n" if material_item else "drawOutline false\n")
    # Use outlineWidth and outlineColor from material_item if available
    outline_width = material_item.outlineWidth if material_item else 0.0
    outline_color = material_item.outlineColor if material_item else [0.0, 0.0, 0.0, 1.0]
    f.write(f"outlineWidth {float(outline_width):.6f}\n")
    f.write(f"outlineColor {float(outline_color[0]):.6f} {float(outline_color[1]):.6f} {float(outline_color[2]):.6f} {float(outline_color[3]):.6f}\n")
    f.write("overrideOutlineSetting false\n")
    f.write("distanceFade false\n")
    f.write("uvofs 0.000000 0.000000\n")
    f.write("uvscl 1.000000 1.000000\n")
    f.write("color 1.000000 0.000000 0.000000\n")
    f.write("normalscl 1.000000\n")
    f.write(f"roughness {float(roughness_value):.6f}\n")
    f.write(f"metallic {float(metallic_value):.6f}\n")
    f.write(f"specular {float(specular_value):.6f}\n")
    f.write("emissive_color 1.000000 1.000000 1.000000\n")
    f.write("emissive_strength 0.000000\n")
    f.write("RenderingType Cutoff\n")
    if mask_map_filename:
        f.write(f"RMMap {mask_map_filename}0001.png\n")
    if sss_map_filename:
        f.write(f"SSSMap {sss_map_filename}0001.png\n")
        f.write(f"sss_coeff {float(material_item.sss_coeff):.6f}\n" if material_item else "sss_coeff 1.000000\n")
    f.write(f"discard_threshold {float(material_item.discard_threshold):.6f}\n" if material_item else "discard_threshold 0.900000\n")
    
    if material.use_nodes:
        for node in material.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                for input in node.inputs:
                    if input.is_linked:
                        for link in material.node_tree.links:
                            if link.to_socket == input:
                                texture_node = find_texture_node(link.from_node)
                                if texture_node and hasattr(texture_node, 'image') and texture_node.image:
                                    filename = sanitize_filename(texture_node.image.name.replace(' ', '_')) + ".png"
                                    if input.name in texture_dict:
                                        f.write(f"{texture_dict[input.name]} {filename}\n")
    
    # Handle LitColor with fallback
    diffuse_color = material.diffuse_color if hasattr(material, 'diffuse_color') else (1.0, 1.0, 1.0, 1.0)
    f.write(f"LitColor {float(diffuse_color[0]):.6f} {float(diffuse_color[1]):.6f} {float(diffuse_color[2]):.6f} 1.000000\n")
    f.write("ShadeColor 0.600000 0.600000 0.600000 1.000000\n")
    f.write("toony 0.900000\n")
    f.write("shift 0.000000\n")
    f.write("LitShaderMixTexMult 0.000000\n")
    f.write("lightColorAtt 0.000000\n")
    f.write("EmissionInt 1.000000\n")
    f.write("matCapScale 1.000000\n")
    f.write("Rim 0.000000 0.000000 0.000000\n")
    f.write("RimInt 1.000000\n")
    f.write("RimLightingMix 0.000000\n")
    f.write("RimFresnelPow 0.000000\n")
    f.write("RimLift 0.000000\n")
    f.write("cutOffThreshold 0.600000\n")
    f.write("outlineType World\n")
    f.write("outlineMaxScale 1.000000\n")
    f.write("outlineMixLighting 0.000000\n")
    f.write("UVRotateAnimation 0.000000\n")
    f.write("\n")

# Custom property group to store material details
def update_shader_type(self, context):
    """Update the material's bakin_shader_type when shader_type is changed."""
    material = bpy.data.materials.get(self.material_name)
    if material:
        material.bakin_shader_type = self.shader_type

class DetectedMaterialItem(bpy.types.PropertyGroup):
    material_name: bpy.props.StringProperty(name="Material Name")
    has_principled_bsdf: bpy.props.BoolProperty(name="Has Principled BSDF", default=False)
    base_color_detected: bpy.props.BoolProperty(name="Base Color Detected", default=False)
    normal_detected: bpy.props.BoolProperty(name="Normal Detected", default=False)
    metallic_detected: bpy.props.BoolProperty(name="Metallic Detected", default=False)
    roughness_detected: bpy.props.BoolProperty(name="Roughness Detected", default=False)
    emission_detected: bpy.props.BoolProperty(name="Emission Detected", default=False)
    specular_detected: bpy.props.BoolProperty(name="Specular Detected", default=False)
    sss_detected: bpy.props.BoolProperty(name="SSS Detected", default=False)
    shader_type: bpy.props.EnumProperty(
        name="Shader Type",
        description="Select the shader for export",
        items=SHADER_OPTIONS,
        default=SHADER_OPTIONS[0][0],
        update=update_shader_type
    )
    show_settings: bpy.props.BoolProperty(
        name="Show Settings",
        description="Toggle visibility of material settings",
        default=False
    )
    emissiveBlink: bpy.props.BoolProperty(
        name="Emissive Blink",
        description="Enable emissive blinking",
        default=False
    )
    emissiveBlinkSpeed: bpy.props.FloatProperty(
        name="Emissive Blink Speed",
        description="Speed of emissive blinking",
        default=0.0,
        min=0.0
    )
    emissiveLinkBuildingLight: bpy.props.BoolProperty(
        name="Emissive Link Building Light",
        description="Link emissive to building light",
        default=False
    )
    castshadow: bpy.props.BoolProperty(
        name="Cast Shadow",
        description="Enable shadow casting",
        default=True
    )
    receivedecal: bpy.props.BoolProperty(
        name="Receive Decal",
        description="Enable receiving decals",
        default=False
    )
    uscrollanim: bpy.props.BoolProperty(
        name="U Scroll Animation",
        description="Enable U-axis scroll animation",
        default=False
    )
    vscrollanim: bpy.props.BoolProperty(
        name="V Scroll Animation",
        description="Enable V-axis scroll animation",
        default=False
    )
    scrollanimspeed: bpy.props.FloatVectorProperty(
        name="Scroll Animation Speed",
        description="Speed of scroll animation for U and V axes",
        default=(0.0, 0.0),
        size=2
    )
    drawOutline: bpy.props.BoolProperty(
        name="Draw Outline",
        description="Enable drawing outline",
        default=False
    )
    outlineWidth: bpy.props.FloatProperty(
        name="Outline Width",
        description="Width of the outline",
        default=0.0,
        min=0.0
    )
    outlineColor: bpy.props.FloatVectorProperty(
        name="Outline Color",
        description="Color of the outline with alpha",
        subtype='COLOR',
        default=(0.0, 0.0, 0.0, 1.0),
        size=4,
        min=0.0,
        max=1.0
    )
    cull_mode: bpy.props.EnumProperty(
        name="Cull Mode",
        description="Select the culling mode",
        items=CULL_MODE_OPTIONS,
        default='back'
    )
    use_mask_map: bpy.props.BoolProperty(
        name="Use Mask Map",
        description="Generate a mask map for this material",
        default=True
    )
    invert_roughness: bpy.props.BoolProperty(
        name="Invert Roughness",
        description="Invert the Roughness texture",
        default=False
    )
    invert_metallic: bpy.props.BoolProperty(
        name="Invert Metallic",
        description="Invert the Metallic texture",
        default=False
    )
    invert_emissive: bpy.props.BoolProperty(
        name="Invert Emissive",
        description="Invert the Emissive texture",
        default=False
    )
    invert_specular: bpy.props.BoolProperty(
        name="Invert Specular",
        description="Invert the Specular texture",
        default=False
    )
    sss_coeff: bpy.props.FloatProperty(
        name="SSS Coeff",
        description="Subsurface scattering coefficient",
        default=1.0,
        min=0.0,
        max=2.0
    )
    discard_threshold: bpy.props.FloatProperty(
        name="Discard Threshold",
        description="Threshold for discarding pixels",
        default=0.9,
        min=0.0,
        max=1.0
    )

def get_texture_from_node(node, visited_nodes=None):
    """
    Recursively traverse node connections to find the first linked texture image.
    """
    if visited_nodes is None:
        visited_nodes = set()
    
    if node in visited_nodes:  # Prevent infinite loops
        return None
    visited_nodes.add(node)
    
    if node.type == 'TEX_IMAGE' and node.image:
        return node.image.name  # Found the texture
    
    # Check node inputs for connected nodes
    for input_socket in node.inputs:
        if input_socket.is_linked:
            from_node = input_socket.links[0].from_node
            found_texture = get_texture_from_node(from_node, visited_nodes)
            if found_texture:
                return found_texture  # Return the first found texture

    return None

def get_material_textures(material):
    """
    Find textures linked to the Principled BSDF node in a material.
    Returns texture presence and BSDF status.
    """
    texture_map = {
        "Base Color": False,
        "Normal": False,
        "Emission": False,
        "Specular": False,
        "Metallic": False,
        "Roughness": False,
        "Subsurface": False
    }
    has_principled_bsdf = False

    if material.use_nodes and material.node_tree:
        nodes = material.node_tree.nodes
        principled_bsdf = next((node for node in nodes if node.type == 'BSDF_PRINCIPLED'), None)
        if principled_bsdf:
            has_principled_bsdf = True
            for key in texture_map.keys():
                input_socket = principled_bsdf.inputs.get(key)
                if key == "Emission":
                    input_socket = principled_bsdf.inputs.get("Emission Color")
                if input_socket and input_socket.is_linked:
                    from_node = input_socket.links[0].from_node
                    if get_texture_from_node(from_node):
                        texture_map[key] = True
                # Special case for Specular (also check Specular IOR Level)
                if key == "Specular" and not texture_map[key]:
                    input_socket = principled_bsdf.inputs.get('Specular IOR Level')
                    if input_socket and input_socket.is_linked:
                        from_node = input_socket.links[0].from_node
                        if get_texture_from_node(from_node):
                            texture_map[key] = True
                # Special case for Subsurface (also check Subsurface Weight)
                if key == "Subsurface" and not texture_map[key]:
                    input_socket = principled_bsdf.inputs.get('Subsurface Weight')
                    if input_socket and input_socket.is_linked:
                        from_node = input_socket.links[0].from_node
                        if get_texture_from_node(from_node):
                            texture_map[key] = True

    return texture_map, has_principled_bsdf

class DetectMaterialsOperator(bpy.types.Operator):
    """Detect materials in the scene and update UI"""
    bl_idname = "object.detect_materials"
    bl_label = "Detect Materials"
    
    def execute(self, context):
        context.scene.detected_materials.clear()  # Clear previous results
        context.scene.material_config_run = True  # Mark Material Config as run
        
        # Collect all unique materials from scene objects
        materials = set()
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and obj.data.materials:
                for material in obj.data.materials:
                    if material:
                        materials.add(material)
        
        for material in materials:
            item = context.scene.detected_materials.add()
            item.material_name = material.name
            texture_map, has_principled_bsdf = get_material_textures(material)
            item.has_principled_bsdf = has_principled_bsdf
            item.base_color_detected = texture_map["Base Color"]
            item.normal_detected = texture_map["Normal"]
            item.metallic_detected = texture_map["Metallic"]
            item.roughness_detected = texture_map["Roughness"]
            item.emission_detected = texture_map["Emission"]
            item.specular_detected = texture_map["Specular"]
            item.sss_detected = texture_map["Subsurface"]
            # Sync shader_type with material's bakin_shader_type
            item.shader_type = getattr(material, 'bakin_shader_type', SHADER_OPTIONS[0][0])
            material.bakin_shader_type = item.shader_type

        # Update triangulation status
        context.scene.is_model_triangulated = check_model_triangulation(context)
        
        return {'FINISHED'}

def register():
    bpy.types.Scene.model_name = bpy.props.StringProperty(
        name="Model Name",
        description="Name of the model to be exported.",
        default="Model Name (Bakin)",
    )
    bpy.types.Scene.language = bpy.props.EnumProperty(
        name="Language",
        description="Choose the UI language.",
        items=[('en', "English", ""), ('jp', "Japanese", ""), ('zh', "Chinese", "")]
    )
    bpy.types.Scene.material_config_run = bpy.props.BoolProperty(
        name="Material Config Run",
        description="Tracks if Material Config has been run.",
        default=False
    )
    bpy.types.Scene.is_model_triangulated = bpy.props.BoolProperty(
        name="Is Model Triangulated",
        description="Tracks if all meshes in the scene are triangulated.",
        default=True
    )
    bpy.types.Material.bakin_shader_type = bpy.props.EnumProperty(
        name="Shader Type",
        description="Select the shader for export",
        items=SHADER_OPTIONS,
        default=SHADER_OPTIONS[0][0]
    )
    bpy.utils.register_class(SimpleOperatorPanel)
    bpy.utils.register_class(ExportFBXOperator)
    bpy.utils.register_class(SwitchLanguageOperator)
    bpy.utils.register_class(DummyOperator)
    bpy.utils.register_class(ToggleSettingsOperator)
    bpy.utils.register_class(DetectedMaterialItem)
    bpy.types.Scene.detected_materials = bpy.props.CollectionProperty(type=DetectedMaterialItem)
    bpy.utils.register_class(DetectMaterialsOperator)
    bpy.utils.register_class(GenerateTextureOperator)
    bpy.utils.register_class(TriangulateMeshesOperator)

def unregister():
    del bpy.types.Scene.model_name
    del bpy.types.Scene.language
    del bpy.types.Scene.material_config_run
    del bpy.types.Scene.is_model_triangulated
    del bpy.types.Material.bakin_shader_type
    del bpy.types.Scene.detected_materials
    bpy.utils.unregister_class(DetectedMaterialItem)
    bpy.utils.unregister_class(DetectMaterialsOperator)
    bpy.utils.unregister_class(GenerateTextureOperator)
    bpy.utils.unregister_class(TriangulateMeshesOperator)
    bpy.utils.unregister_class(ToggleSettingsOperator)
    bpy.utils.unregister_class(DummyOperator)
    bpy.utils.unregister_class(SimpleOperatorPanel)
    bpy.utils.unregister_class(ExportFBXOperator)
    bpy.utils.unregister_class(SwitchLanguageOperator)

if __name__ == "__main__":
    register()
