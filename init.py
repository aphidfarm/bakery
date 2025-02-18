import bpy

C = bpy.context
D = bpy.data

bl_info = {
    "name": "Bakery",
    "description": "Bakery",
    "version": (0, 1),
    # "blender": (4, 32, 1),
    "category": "Material"
}

class bakePrep(bpy.types.Operator):
    """Prepare baking resources"""
    bl_idname = "material.bake_prep"
    bl_label = "Prep Bake Resources"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.image.new(
            name="Bake Texture",
            width=1024,
            height=1024,
            color=(0, 0, 0, 1),
            alpha=False,
            generated_type='BLANK',
            float=False,
            use_stereo_3d=False,
            tiled=False
        )

        for mat in D.materials:
            if mat.use_nodes == False:
                continue
            node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            node.location = (0, 0)
            node.name  = "Bake Texture"
            node.label = "Bake Texture"
            node.image = D.images["Bake Texture"]

        return {'FINISHED'}

class bakeClear(bpy.types.Operator):
    """Clear prepared baking resources"""
    bl_idname = "material.bake_clear"
    bl_label = "Clear Bake Resources"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for mat in D.materials:
            if mat.use_nodes == False:
                continue
            node = mat.node_tree.nodes.new("ShaderNodeTexImage")
            if node.name == "Bake Texture":
                mat.node_tree.nodes.remove(node)
        return {'FINISHED'}

def register():
    print("Bakery registered")
    bpy.utils.register_class(bakePrep);
    bpy.utils.register_class(bakeClear);

def unregister():
    print("Bakery unregistered")
    bpy.utils.unregister_class(bakePrep);
    bpy.utils.unregister_class(bakeClear);

if __name__ == "__main__":
    register()
